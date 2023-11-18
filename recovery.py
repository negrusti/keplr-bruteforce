import yaml
import argparse
import pyperclip
import os
import requests

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from mnemonic import Mnemonic

with open('bip39words-en.txt', 'r') as words_file:
    words = words_file.read().splitlines()

with open('settings.yaml', 'r') as yaml_file:
    settings = yaml.load(yaml_file, Loader=yaml.FullLoader)

script_dir = os.path.dirname(os.path.realpath(__file__))
chrome_extension_id = "dmkamcknogkgcdfhhbddcghachkejeap"
max_retries = 5

WALLET_NAME = settings.get('WALLET_NAME', '')
PASSWORD = settings.get('PASSWORD', '')
MY_WORDS = settings.get('MY_WORDS', [])
KEPLR_CRX_PATH = os.path.join(script_dir, f"{chrome_extension_id}.crx")
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
setup_your_wallet_form_x = "//input[contains(@placeholder, 'NFT Vault')]/ancestor::form[1]"
currency_x = "//div[@color='#FEFEFE' and not(contains(text(), 'chain(s) selected'))]"

def download_url(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url, allow_redirects=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response to a file
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully: {filename}")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error occurred: {e}")

if not os.path.exists(KEPLR_CRX_PATH):
    print("Downloading Keplr extension CRX from Google...")
    download_url(f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=119.0.6045.124&acceptformat=crx2,crx3&x=id%3D{chrome_extension_id}%26uc",
        KEPLR_CRX_PATH)

# SCRIPT
chop = webdriver.ChromeOptions()
chop.add_experimental_option("detach", True)
chop.add_argument("--disable-usb-devices")
chop.add_extension(KEPLR_CRX_PATH)
driver = webdriver.Chrome(options=chop)
driver.implicitly_wait(10)


# Handling Selenium quirks with extensions
driver.get("https://example.com")
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.get(f'chrome-extension://{chrome_extension_id}/register.html#')

mnemo = Mnemonic("english")

def bruteforce_at_position(input_position):
    count = 0

    for word in words:
        
        retry_count = 0
        all_words = MY_WORDS.copy()
        all_words.insert(input_position, word)
        merged_words = ' '.join(all_words)
        if not mnemo.check(merged_words):
            continue
        
        while retry_count < max_retries:
            
            driver.refresh()
            print(f"Checking wallet for: {merged_words}")

            try:
                driver.find_element(By.XPATH, existing_wallet_button_x).click()
                driver.find_element(By.XPATH, recovery_phrase_button_x).click()
                input_elements = driver.find_elements(By.XPATH, input_word_x)

                pyperclip.copy(merged_words)
                input_elements[0].send_keys(Keys.CONTROL, 'v')

                driver.find_element(By.XPATH, import_button_x).click()

                setup_your_wallet_form = driver.find_element(By.XPATH, setup_your_wallet_form_x)

                driver.find_element(By.XPATH, input_wallet_name_x).send_keys(WALLET_NAME)

                if len(setup_your_wallet_form.find_elements(By.TAG_NAME, "input")) > 1:
                    password_fields = driver.find_elements(By.XPATH, input_password_x)
                    for ele in password_fields:
                        ele.send_keys(PASSWORD)

                driver.find_element(By.XPATH, next_button_x).click()

                WebDriverWait(driver, 10).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, select_all_checkbox_x)))

                currencies = driver.find_elements(By.XPATH, currency_x)
                results_cur = ', '.join(cur.text for cur in currencies if float(cur.text.split()[0]) > 0)

                if results_cur:
                    count += 1
                    with open('results.txt', 'a') as file:
                        file.write(f'Words: {merged_words}\n')
                        file.write(f'Coins: {results_cur}\n')
                    print('Results written to file', '\n')
                
                break

            except (NoSuchElementException, IndexError, TimeoutException) as e:
                retry_count += 1
                with open('results.txt', 'a') as file:
                    file.write(f'[ERROR] Word: {word} in position {input_position + 1}, attempt {retry_count}\n')
                print(f'[ERROR] Word: {word} in position {input_position + 1}, attempt {retry_count}', e)


    if count == 0:
        with open('results.txt', 'a') as file:
            file.write(f'No results found for any combination at {input_position + 1} position.\n')
        print(f'No results found for any combination at {input_position + 1} position.')
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recovery Script')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--position', type=int, choices=xrange(1, 24), help='Word position')

    args = parser.parse_args()

    if args.position:
        bruteforce_at_position(args.position)
    else:
        for i in range(CURRENT_POSITION - 1, 12):
            bruteforce_at_position(i)
