import smtplib
import json
from email.mime.text import MIMEText
from random import choice

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

def convert_seconds_to_mins(num_seconds):
    '''Returns a dictionary containing keys 'mins' and 'secs' '''

    if num_seconds < 0:
        time_dict = {'secs': num_seconds, 'mins': 0}
    else:
        # minutes is sure to be an integer because of integer division
        minutes = num_seconds // 60
        # seconds could be non-int e.g., num_seconds = 60.4
        seconds = num_seconds % 60
        seconds = round(seconds)

        time_dict = {'secs': seconds, 'mins': minutes}
    return time_dict

def convert_seconds_to_string(num_seconds):
    '''This function takes an integer and converts it into a formatted 
    string with units. This assumes we will never plank for more than
    59 minutes and 59 seconds.'''
    one_hour = 60
    time_dict = convert_seconds_to_mins(num_seconds)
    minutes = time_dict['mins']
    seconds = time_dict['secs']

    # Need to pluralize units
    if minutes == 1:
        min_unit = "minute"
    else:
        min_unit = "minutes"
    if seconds == 1:
        sec_unit = "second"
    else:
        sec_unit = "seconds"

    # Form string based off interval
    if seconds < 0:
        formatted_string = "ERROR: Less than 0 seconds."
    elif minutes == 0 and seconds < 60:
        formatted_string = """{sec} {s_unit} (0:{sec:02})""".format(
                sec = seconds,
                s_unit = sec_unit)
    elif minutes >= 1 and minutes < one_hour:
        # Did this so I wouldn't have to post-process
        raw_string = ("{mints!s} {m_unit} and "
                      "{sec!s} {s_unit} "
                      "({mints:02}:{sec:02})")
        formatted_string = raw_string.format(
                sec = seconds, 
                mints = minutes,
                m_unit = min_unit,
                s_unit = sec_unit)
    else:
        formatted_string = str(num_seconds) + " seconds ERROR"

    return formatted_string


def increment_number_seconds(seconds_today, increment):
    '''This function will actually iterate the file one second and save it.
    Returns no value.
    '''
    seconds_file = "number_seconds.txt"
    seconds_tomorrow = seconds_today + increment
    with open(seconds_file, 'w') as f:
        f.write(str(seconds_tomorrow))

def get_thinspo_quote():
    '''This function returns a random quote pulled from the thinspo file. This
    function assumes that each quote is separated by a newline character.'''
    thinspo_filename = 'thinspo.txt'
    with open(thinspo_filename, 'r') as f:
        full_text = f.read()

    quote_list = full_text.split('\n')
    if quote_list[-1] == '':
        quote_list = quote_list[:-1]

    todays_quote = choice(quote_list)
    return todays_quote 

def main():
    '''This is where the main logic for sending the email will reside.'''
    
    login_info = get_account_info()
    login_email = login_info['email']
    login_password = login_info['password']
    thinspo_quote = get_thinspo_quote()

    seconds_today = get_number_seconds()
    time_string = convert_seconds_to_string(seconds_today)
    
    # Just setting some variables needed for the email
    subject_text = '''Plankin\' time! {time} today.'''.format(
            time = time_string)
    recepients = ['hben592@gmail.com', 'etam22@gmail.com']
    body_text = """\
    You need to plank today!!
    To be da best, you have to plank for {time} today.
    If you don\'t plank for that long you suck.
    Your motivational quote for today is:

    {quote}
    """.format(time=time_string, quote = thinspo_quote)

    msg = MIMEText(body_text)
    msg['Subject'] = subject_text
    msg['From'] = login_email
    msg['To'] = ", ".join(recepients)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(0)
    server.starttls()
    server.login(login_email, login_password)

    server.sendmail(login_email, recepients, msg.as_string())
    server.quit()
    increment_number_seconds(seconds_today, 1)

main()
