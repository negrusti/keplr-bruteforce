= PREPARATIONS:

Download CRX file for Keplr:
1. Go to Chrome web store for Keplr ID: dmkamcknogkgcdfhhbddcghachkejeap
2. Switch to https://robwu.nl/crxviewer/ and insert full URL:
    https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap
3. Click "Open in this viewer" button -> "Download" (top right corner) for download CRX file

Make vars:
In vars.py file you need to set up some variables.
Set up Wallet name, Password, path to CRX file and 11(!) existing words

Install requirements:
In terminal execute "pip install -r requirements.txt" in files directory


= RUN:
Execute command "python recovery.py" in files directory
Available flags: '--all' for run All inputs in input block
                 '--first' for run only first input
                 '--last' for run only last input

= RESULTS:
All results are written to the file - "results.txt".
Format inside:  recovery words: list
                all not zero coins: list


= ADDITIONAL SETTINGS:
You can change Input position in recovery inputs block by change var CURRENT_POSITION in var.py
Available numbers from 0 to 12 (int)!

All recovery words are saved to "words" var in vars.py.

Additional CSS Selector are saved in the end of the file vars.py.