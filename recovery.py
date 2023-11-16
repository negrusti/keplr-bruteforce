import yaml
import argparse
import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException, NoAlertPresentException, \
    ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from mnemonic import Mnemonic
import pyperclip

with open('allWords.txt', 'r') as words_file:
    words = words_file.read().splitlines()

with open('settings.yaml', 'r') as yaml_file:
    settings = yaml.load(yaml_file, Loader=yaml.FullLoader)

WALLET_NAME = settings.get('WALLET_NAME', '')
PASSWORD = settings.get('PASSWORD', '')
MY_WORDS = settings.get('MY_WORDS', [])
KEPLR_CRX_PATH = settings.get('KEPLR', '')
CURRENT_POSITION = settings.get('CURRENT_POSITION', 0)

# ELEMENTS (XPATH)
existing_wallet_button_x = "//button[.//div[text()='Import an existing wallet']]"
recovery_phrase_button_x = "//button[.//div[text()='Use recovery phrase or private key']]"
input_word_x = "//input[@type='password']"
import_button_x = "//button[@type='submit']"
input_wallet_name_x = "//input[contains(@placeholder, 'NFT Vault')]"
input_password_x = "//input[contains(@placeholder, 'characters in length')]"
next_button_x = "//button[.//div[text()='Next']]"
all_coins_block_x = "//div[starts-with(@class, 'simplebar')]"
select_all_checkbox_x = "//div[text()='Select All']/following::input[@type='checkbox'][1]"

# SCRIPT
chop = webdriver.ChromeOptions()
chop.add_experimental_option("detach", True)
chop.add_argument("--disable-usb-devices")
chop.add_extension(KEPLR_CRX_PATH)
driver = webdriver.Chrome(options=chop)
driver.implicitly_wait(10)

driver.get("https://example.com")
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.get('chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/register.html#')

mnemo = Mnemonic("english")

def bruteforce_at_position(input_position):
    count = 0

    for word in words:
        all_words = MY_WORDS.copy()
        all_words.insert(input_position, word)
        merged_words = ' '.join(all_words)
        if not mnemo.check(merged_words):
            continue
        print(merged_words + "\n")

        driver.refresh()
        driver.find_element(By.XPATH, existing_wallet_button_x).click()
        driver.find_element(By.XPATH, recovery_phrase_button_x).click()
        input_elements = driver.find_elements(By.XPATH, input_word_x)

        pyperclip.copy(merged_words)
        input_elements[0].send_keys(Keys.CONTROL, 'v')

        try:
            driver.find_element(By.XPATH, import_button_x).click()

            driver.find_element(By.XPATH, input_wallet_name_x).send_keys(WALLET_NAME)
            #if len(driver.find_elements(By.TAG_NAME, "input")) > 1:
            driver.implicitly_wait(0.2)
            password_fields = driver.find_elements(By.XPATH, input_password_x)
            for ele in password_fields:
                ele.send_keys(PASSWORD)
            driver.implicitly_wait(10)

            driver.find_element(By.XPATH, next_button_x).click()
            currencies = driver.find_elements(By.XPATH, "//div[@color='#FEFEFE']")
            #for cur in currencies:
            #    print(cur.text)
            results_usd = driver.find_element(By.XPATH, all_coins_block_x).text.split()
            non_zero_values = any(item.replace('.', '', 1).isdigit() and float(item) != 0 for item in results_usd)
            if non_zero_values:
                count += 1
                print(results_usd)
                with open('results.txt', 'a') as file:
                    file.write(f'Words: {merged_words}\n')
                    file.write(f'Coins: {results_usd}\n')
                print('Results written to file', '\n')

        except NoSuchElementException as e:
            with open('results.txt', 'a') as file:
                file.write(f'[ERROR] Stop on Word: {word}')
            print(f'[ERROR] Stop on Word: {word}', e)

    if count == 0:
        with open('results.txt', 'a') as file:
            file.write(f'No results found for any combination at {input_position} position.\n')
        print(f'No results found for any combination at {input_position} position.')
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recovery Script')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--first', action='store_true', help='Run only First input')
    group.add_argument('--last', action='store_true', help='Run only Last input')

    args = parser.parse_args()

    if args.first:
        bruteforce_at_position(0)
    elif args.last:
        bruteforce_at_position(11)
    else:
        for i in range(CURRENT_POSITION-1, 12):
            bruteforce_at_position(i)
