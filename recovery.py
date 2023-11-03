import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import argparse
from selenium.common import NoSuchElementException, TimeoutException, NoAlertPresentException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import yaml

with open('allWords.txt', 'r') as words_file:
    words = words_file.read().splitlines()

with open('settings.yaml', 'r') as yaml_file:
    settings = yaml.load(yaml_file, Loader=yaml.FullLoader)

WALLET_NAME = settings.get('WALLET_NAME', '')
PASSWORD = settings.get('PASSWORD', '')
MY_WORDS = settings.get('MY_WORDS', [])
KEPLR = settings.get('KEPLR', '')
CURRENT_POSITION = settings.get('CURRENT_POSITION', 0)

# ELEMENTS (XPATH)
existing_wallet_button_x = '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[3]/div[3]/button'
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
chop.add_extension(KEPLR)
driver = webdriver.Chrome(options=chop)
driver.implicitly_wait(30)

driver.get("https://example.com")
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.get('chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/register.html#')


def recovery_script(input_position):
    driver.find_element(By.XPATH, existing_wallet_button_x).click()
    driver.find_element(By.XPATH, recovery_phrase_button_x).click()
    input_elements_block = driver.find_element(By.XPATH, input_block_x)
    input_elements = input_elements_block.find_elements(By.TAG_NAME, 'input')
    modify = MY_WORDS.copy()
    modify.insert(input_position, '')

    input_word_pairs = zip(input_elements, modify)
    for ele, w in input_word_pairs:
        ele.send_keys(Keys.CONTROL, 'a')
        ele.send_keys(Keys.DELETE)
        ele.send_keys(w)

    for word in words:
        try:
            input_elements[input_position].send_keys(Keys.CONTROL, 'a')
            input_elements[input_position].send_keys(Keys.DELETE)
            input_elements[input_position].send_keys(word)

            driver.find_element(By.XPATH, import_button_x).click()

            try:
                Alert(driver).accept()
                continue
            except NoAlertPresentException:
                user_data = driver.find_element(By.XPATH, input_user_data_x)
                if len(user_data.find_elements(By.TAG_NAME, 'input')) == 1:
                    driver.find_element(By.XPATH, input_wallet_name_solo_x).send_keys(WALLET_NAME)
                    driver.find_element(By.XPATH, next_button_solo_x).click()
                else:
                    driver.find_element(By.XPATH, input_wallet_name_x).send_keys(WALLET_NAME)
                    driver.find_element(By.XPATH, input_password_x).send_keys(PASSWORD)
                    driver.find_element(By.XPATH, input_confirm_x).send_keys(PASSWORD)
                    driver.find_element(By.XPATH, next_button_x).click()
                driver.find_element(By.XPATH, select_all_checkbox_x).click()
                results_usd = driver.find_element(By.XPATH, all_coins_block_x).text.split()
                non_zero_values = any(item.replace('.', '', 1).isdigit() and float(item) != 0 for item in results_usd)
                if non_zero_values:
                    modify[input_position] = word
                    print(*modify)
                    print(results_usd)
                    with open('results.txt', 'a') as file:
                        file.write(f'Words: {modify}\n')
                        file.write(f'Coins: {results_usd}\n')
                        file.write(50 * '-' + '\n')
                    print('Results written to file', '\n')
                driver.execute_script("window.open('about:blank', 'new_window')")
                driver.switch_to.window(driver.window_handles[1])
                driver.get('chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/register.html#')

                driver.find_element(By.XPATH, existing_wallet_button_x).click()
                driver.find_element(By.XPATH, recovery_phrase_button_x).click()
                input_elements_block = driver.find_element(By.XPATH, input_block_x)
                input_elements = input_elements_block.find_elements(By.TAG_NAME, 'input')

                input_word_pairs = zip(input_elements, modify)
                for ele, w in input_word_pairs:
                    ele.send_keys(Keys.CONTROL, 'a')
                    ele.send_keys(Keys.DELETE)
                    ele.send_keys(w)
        except NoSuchElementException as e:
            print(f'[ERROR] Stop on Word: {word}', e)
    return None


def recovery_short(input_position):
    driver.find_element(By.XPATH, existing_wallet_button_x).click()
    driver.find_element(By.XPATH, recovery_phrase_button_x).click()
    input_elements_block = driver.find_element(By.XPATH, input_block_x)
    input_elements = input_elements_block.find_elements(By.TAG_NAME, 'input')
    modify = MY_WORDS.copy()
    modify.insert(input_position, '')

    input_word_pairs = zip(input_elements, modify)
    for ele, w in input_word_pairs:
        ele.send_keys(Keys.CONTROL, 'a')
        ele.send_keys(Keys.DELETE)
        ele.send_keys(w)

    for word in words:
        try:
            input_elements[input_position].send_keys(Keys.CONTROL, 'a')
            input_elements[input_position].send_keys(Keys.DELETE)
            input_elements[input_position].send_keys(word)

            driver.find_element(By.XPATH, import_button_x).click()

            try:
                Alert(driver).accept()
                continue
            except NoAlertPresentException:
                modify[input_position] = word
                with open('results_short.txt', 'a') as file:
                    file.write(f'Words: {modify}\n')
                print('Results written to file', '\n')
                driver.find_element(By.XPATH, back_button_x).click()
        except NoSuchElementException as e:
            print(f'[ERROR] Stop on Word: {word}', e)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recovery Script')

    parser.add_argument('--deep', action='store_true', help='Run deep recovery')
    parser.add_argument('--short', action='store_true', help='Run short recovery')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true', help='Run for ALL inputs')
    group.add_argument('--first', action='store_true', help='Run only First input')
    group.add_argument('--last', action='store_true', help='Run only Last input')

    args = parser.parse_args()

    if args.deep:
        if args.all:
            for i in range(CURRENT_POSITION, 13):
                recovery_script(i)
        elif args.first:
            recovery_script(0)
        elif args.last:
            recovery_script(11)
    elif args.short:
        if args.all:
            for i in range(CURRENT_POSITION, 13):
                recovery_short(i)
        elif args.first:
            recovery_short(0)
        elif args.last:
            recovery_short(11)
    else:
        print('Please specify a valid flag: --deep or --short and --all, --first or --last ')
