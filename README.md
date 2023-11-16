## What is this thing

A Python script driving a Keplr Chrome extension via Selenium. If you are missing a single recovery word from your 12 words phrase, you can brute-force it using this tool.

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

Execute command "python recovery.py" in files directory

Available flags: '--first' for run only first input
                 '--last' for run only last input      

## Output

All results from script with entering wallet write to "results.txt".

## Additional settings

You can restart the process from a certain position by changing CURRENT_POSITION in your settings.yaml
Available numbers from 1 to 12
