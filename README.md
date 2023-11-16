= PREPARATIONS:
Download CRX file for Keplr:
1. Go to Chrome web store for Keplr ID: dmkamcknogkgcdfhhbddcghachkejeap
2. Switch to https://robwu.nl/crxviewer/ and insert full URL:
    https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap
3. Click "Open in this viewer" button -> "Download" (top right corner) for download CRX file

Copy settings.yaml.template file to settings.yaml

In settings.yaml file you need to set up some variables.
Set up Wallet name, Password, path to CRX file and 11(!) existing words

Install requirements:
In terminal execute "pip install -r requirements.txt" in files directory

= RUN:
Execute command "python recovery.py" in files directory
Available flags: '--first' for run only first input
                 '--last' for run only last input      

= RESULTS:
All results from script with entering wallet write to "results.txt".

= ADDITIONAL SETTINGS:
You can change Input position in recovery inputs block by change var CURRENT_POSITION in your settings.yaml
Available numbers from 1 to 12 (int)!