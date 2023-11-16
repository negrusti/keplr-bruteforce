import yaml
import argparse

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException, NoAlertPresentException, \
    ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from mnemonic import Mnemonic

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
recovery_phrase_button_x = '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[5]'
input_block_x = '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div'
import_button_x = '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[6]'
back_button_x = '//*[@id="app"]/div/div[1]/div[1]'
input_user_data_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div'
input_wallet_name_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[1]/div[2]/div/div/input'
input_wallet_name_solo_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[3]/div[2]/div/div/input'
input_password_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[3]/div[2]/div/div/input'
input_confirm_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[5]/div[2]/div/div/input'
next_button_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[7]/button'
next_button_solo_x = '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[5]/button'
all_coins_block_x = '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[5]'
select_all_checkbox_x = '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[7]'

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


def fill_input_elements(elements, values):
    for ele, value in zip(elements, values):
        ele.send_keys(Keys.CONTROL, 'a')
        ele.send_keys(Keys.DELETE)
        ele.send_keys(value)


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
        input_elements_block = driver.find_element(By.XPATH, input_block_x)
        input_elements = input_elements_block.find_elements(By.TAG_NAME, 'input')

        fill_input_elements(input_elements, all_words)

        try:
            driver.find_element(By.XPATH, import_button_x).click()

            user_data = driver.find_element(By.XPATH, input_user_data_x)
            if len(user_data.find_elements(By.TAG_NAME, 'input')) == 1:
                driver.find_element(By.XPATH, input_wallet_name_solo_x).send_keys(WALLET_NAME)
                driver.find_element(By.XPATH, next_button_solo_x).click()
            else:
                driver.find_element(By.XPATH, input_wallet_name_x).send_keys(WALLET_NAME)
                driver.find_element(By.XPATH, input_password_x).send_keys(PASSWORD)
                driver.find_element(By.XPATH, input_confirm_x).send_keys(PASSWORD)
                driver.find_element(By.XPATH, next_button_x).click()
            wait = WebDriverWait(driver, 10)
            element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, select_all_checkbox_x)))
            try:
                element.click()
            except ElementClickInterceptedException:
                print('[WARNING] Select all checkbox failed by click()')
                driver.execute_script("arguments[0].click();", element)
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
