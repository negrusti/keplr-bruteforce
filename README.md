## What is this thing

A Python script driving the Keplr Chrome extension via Selenium. If you are missing a single recovery word from your 12 words phrase, you can brute-force it using this tool. The script will find all valid recovery phrases and then "recover" the wallets given the name and password from the config file - they can be anything you like. It will then enter each wallet and check for non-zero currency values.

## Prerequisites:

Install Python

Optional: Download and verify the Keplr extension CRX file yourself (you can use any other methods):
1. Verify in Chrome web store the correct Keplr extension ID:
https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap
2. Switch to https://robwu.nl/crxviewer/ and insert full URL:
    https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap
3. Click "Open in this viewer" button -> "Download" (top right corner) for download CRX file
4. Copy the downloaded CRX file into the project directory
If you omit the download step then the script will try to download the extension automatically.

In the terminal execute "pip install -r requirements.txt" in the project directory

## Configuration

Copy settings.yaml.template file to settings.yaml

In the settings.yaml file you need to configure wallet name, password and 11 existing words

## Usage

From the command prompt execute the command "python recovery.py" in files directory. By default the script will try to find the missing word at any position in the recovery phrase.

Available switches:
* '--first' to brute-force only the first position
* '--last' to brute-force only the last position

## Output

All results are written to results.txt file in the project directory.

## Additional settings

You can restart the process from a certain position by changing CURRENT_POSITION in your settings.yaml
Valid values from 1 to 12
