import smtplib
import json
from email.mime.text import MIMEText

def get_account_info():
    ''' Need to pull password info from file which doesn't appear in git 
    repo
    This returns a python dictionary containing an e-mail and a password.
    The keys of this dictionary are "email" and "password".'''
    json_account_info = "account.json"
    with open(json_account_info) as account_json_file:
        json_decoded = json.load(account_json_file)
    return json_decoded

def get_number_seconds():
    ''' Need this function so that we can pull the number of seconds each 
    day
    from a persistent file.
    Returns an integer containing the number of seconds for that day.
    '''
    seconds_file = "number_seconds.txt"
    with open(seconds_file, 'r') as f:
        number_of_seconds = f.read()
    return int(number_of_seconds)

def change_number_seconds(seconds_today, increment):
    '''This function will actually iterate the file one second and save it.
    Returns no value.
    '''
    seconds_file = "number_seconds.txt"
    seconds_tomorrow = seconds_today + increment
    with open(seconds_file, 'w') as f:
        f.write(str(seconds_tomorrow))

def main():
    '''This is where the main logic for sending the email will reside.'''
    
    login_info = get_account_info()
    login_email = login_info['email']
    login_password = login_info['password']

    seconds_today = get_number_seconds()
    
    # Just setting some variables needed for the email
    subject_text = '''Plankin\' time! {seconds} seconds today.'''.format(
            seconds = seconds_today)
    recepients = ['hben592@gmail.com', 'etam22@gmail.com']
    body_text = '''
        You need to plank today!!
        To be da best, you have to plank for {seconds} seconds today.
        If you don\'t plank for that long you suck.
        '''.format(seconds = seconds_today)

    msg = MIMEText(body_text)
    msg['Subject'] = subject_text
    msg['From'] = login_email
    msg['To'] = ", ".join(recepients)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login_email, login_password)

    server.sendmail(login_email, recepients, msg.as_string())
    server.quit()
    change_number_seconds(seconds_today, 1)

main()
