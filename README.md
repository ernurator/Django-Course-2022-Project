# E.Bank - banking system backend

![Some E-Banking logo from the Internet](https://www.absradiotv.com/wp-content/uploads/2019/02/e-banking.jpg)

Written on Python, created using `django`, `djangorestframework` and `djangorestframework-jwt`. 

Available functionality:

- Create user account (as a customer, or as a merchant)
- Upload document photo
- Open bank account
- Open debit card
- Open deposit account
- Take loan
- Make payments by loan (from bank account or deposit)
- Different types of money transfers:
  - Account -> account
  - Account -> deposit
  - Deposit -> account
  - Card -> account
- Some basic CRUD operations with accounts, deposits, cards, loans
- For admins (superusers):
  - Charge interests on deposit (once a day)
  - Charge interests on loan (once a day)

[Here](./BF%20Django%20Project%20%5BSpring%202022%5D.postman_collection.json) you can find structured package for Postman with requests to all existing API endpoints.

## How to run locally

```bash
# Cloning the repository
git clone https://github.com/ernurator/Django-Course-2022-Project
cd Django-Course-2022-Project

# Skip if virtualenv is installed
python3 -m pip install virtualenv

# Create virtual env
python3 -m virtualenv .venv
source .venv/bin/activate  # for Linux & MacOS

# Install all required libraries
pip install -r requirements.txt

# Run the web app
./manage.py runserver 8000
# Then open http://127.0.0.1:8000 in browser
```
