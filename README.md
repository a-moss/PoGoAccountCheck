# PoGoAccountCheck
PoGoAccountCheck is a python script which reads PTC accounts from a file and checks if they are banned. If they __are__ banned, the program will save them to a file, banned.txt.

# Installation
To Install PoGoAccountCheck run:

	git clone https://github.com/a-moss/PoGoAccountCheck.git

Then:

	cd PoGoAccountCheck
    
After you are in the directory, make sure to install all the requirements by running:

	pip install -r requirements.txt	

# Usage

To use the program run the following command:

	python banned.py file.txt

Where file.txt is the file of accounts to check. See "Formatting" to see how the file should be formatted.
ie:

	python banned.py accounts.txt


# Formatting
Your file of accounts should be structured as follows:

username1:password1
username2:password2
username3:password3

# Output
The program will display a message in the terminal if the account is banned. Additionally, it will output all banned accounts to a new file named banned.txt
