# CLU
Command Line Utility to use the OSC platform

This is a command line interface that can be used to perform the following operations with OSC:
- contribute datasets
- query datasets
- update datasets

Requirements:
python version > 3.6.10 (tested)
yaml


Install the required dependencies:
with sudo access: pip3 install -r requirements.txt

without sudo access: pip3 install -r requirements.txt --user


Usage:
python client.py --help

python client.py --action contribute --value template.yaml --token <token>

python client.py --action update --value <osc-id>.yaml --token <token>

python client.py --action query --value <osc-id>

User can get the "token" by logging into the portal and copy the token string under My OSC->Profile. The token value passed in the command line takes precedence over the one present in the "template" file. The token is valid for 10 days.

An example template.yaml file is provided. Please follow the directions with the template to include / exclude datasets. Since the interface expects an yaml file for the contribute operation, care must be taken to follow appropriate syntax such as indentation, use of '-' and so on.

For updating datasets, first query for the dataset. A copy of the data from your query is stored as a yaml file which should be used to update / modify the contributed dataset. Note that you have to be the contributor of the dataset to update it.
