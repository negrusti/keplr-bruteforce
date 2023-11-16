## What is this thing

A Python script driving a Keplr Chrome extension via Selenium. If you are missing a single recovery word from your 12 words phrase, you can brute-force it using this tool. The script will find all valid recovery phrases and then "recover" the wallets given the name and password from the config file - they can be anything you like. It will then enter each wallet and check for non-zero currency values.

## Prerequisites:

Install Python

Download CRX file for Keplr:
1. Go to Chrome web store for Keplr ID: dmkamcknogkgcdfhhbddcghachkejeap
2. Switch to https://robwu.nl/crxviewer/ and insert full URL:
    https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap
3. Click "Open in this viewer" button -> "Download" (top right corner) for download CRX file

In the terminal execute "pip install -r requirements.txt" in the project directory

## Configuration

Copy settings.yaml.template file to settings.yaml

In settings.yaml file you need to set up some variables.
Set up Wallet name, Password, path to CRX file and 11(!) existing words

## Usage

Execute command "python recovery.py" in files directory. By default the script will try to find the missing word at any position in the recovery phrase.

Available flags:
* '--first' to bruteforce only the first position
* '--last' to bruteforce only the last position

## Output

All results are written to results.txt file in the project directory.

## Additional settings

You can restart the process from a certain position by changing CURRENT_POSITION in your settings.yaml
Valid values from 1 to 12
