import smtplib
import json

def get_account_info():
''' Need to pull password info from file which doesn't appear in git repo
This returns a python dictionary containing an e-mail and a password.
'''
    json_account_info = "account.json"
    with open(json_account_info) as account_json_file:
        json_decoded = json.load(account_json_file)
    return json_decoded

def get_number_seconds():
''' Need this function so that we can pull the number of seconds each day
from a persistent file.
Returns an integer containing the number of seconds for that day.
'''
    seconds_file = "number_seconds.txt"
    with open(seconds_file, 'r') as f:
        number_of_seconds = f.read()
    return number_of_seconds

def change_number_seconds(number_today):
'''This function will actually iterate the file one second and save it.
Returns no value.
'''
    seconds_file = "number_seconds.txt"
    number_for_tomorrow = number_today + 1
    with open(seconds_file, 'w') as f:
        f.write(number_for_tomorrow)



def main():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("howiethebot@gmail.com", "a30S7*ODTgvMkjKvfF")

    msg = "Go plank!"
    server.sendmail("howiethebot@gmail.com", "hben592@gmail.com", msg)
    server.quit()
