import rumps, objc
import requests
import os, json, subprocess
from pathlib import Path

# ------------------------------------------------------------------------------
# ----------------------- Setiing up data n variables --------------------------

# Making a .volsbb file with json data for username and password
CONFIG_FILE = str(Path.home()) + '/.volsbb'
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        demo_credentials = {
            'username':'demo',
            'password':'demo_password'
        }
        json.dump(demo_credentials, f)
        f.close()

# Default Headers
HEADERS = {
    'origin': 'http://phc.prontonetworks.com',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'save-data': 'on',
    'user-agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    ),
    'accept': (
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    ),
    'dnt': '1',
    'referer': 'http://phc.prontonetworks.com/cgi-bin/authlogin?',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

# URLS and Payload
URL_LOGIN = 'http://phc.prontonetworks.com/cgi-bin/authlogin'
URL_LOGOUT = 'http://phc.prontonetworks.com/cgi-bin/authlogout'
PAYLOAD = {
    'Submit22': 'Login',
    'serviceName': 'ProntoAuthentication',
}

LOGGED_IN_RESPONSE = '<html>\n<body>\n<b> You are already logged in </b>\n</body>\n</html>\n\n\n'
NSDictionary = objc.lookUpClass('NSDictionary')

TITLES = {
    'error': 'Error ❗️',
    'already_connected': 'Alredy connected ✌🏼',
    'logged_in': 'Logged in ✅',
    'logged_out': 'Logged out ⎋',
}

def notify(title_type, msg):
    rumps.notification(TITLES[title_type], msg, '', data=NSDictionary())


# ------------------------------------------------------------------------------
# --------------------------- Main app setup -----------------------------------
class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__('VOLSBB')
        self.menu = ['Login', 'Logout', 'Config', 'About']

    @rumps.clicked('Login')
    def login(self, sender):
        my_payload = PAYLOAD.copy()
        with open(CONFIG_FILE) as f:
            credentials = json.load(f)

        if(credentials['username'] == 'demo' and credentials['password'] == 'demo_password'):
            rumps.alert('Enter your credentials in the following file.\nSave it. \nThen retry.')
            subprocess.call(['open', CONFIG_FILE])
            return

        username, password = credentials['username'], credentials['password']
        my_payload['userId'] = username
        my_payload['password'] = password
        print(my_payload)

        try:
            response = requests.request(
                'POST', URL_LOGIN,
                data=my_payload, headers=HEADERS, timeout=3,
            )
        except requests.RequestException:
            notify('error', 'Check if the wifi is on and connected to VIT wifi')

        if response.status_code == 200:
            if response.text == LOGGED_IN_RESPONSE:
                notify(
                    'already_connected',
                    'Bro, chill. You are already connected, just use it'
                )
            elif ((response.text).find('<title>Successful Pronto Authentication</title>') > 0):
                notify('logged_in', 'VOLSBB login sucessful :)')
            else:
                notify('error', 'Could not connect, check your credentials')
        else:
            notify('error', 'Could not connect to VIT wifi')

    @rumps.clicked('Logout')
    def logout(self, sender):
        try:
            response_logout = requests.request('GET', URL_LOGOUT, timeout=5)
        except requests.RequestException:
            notify('error', 'Could not logout, check your wifi connection')

        if response_logout.status_code == 200:
            notify('logged_out', 'VOLSBB logout sucessful')
        else:
            notify('error', 'Could not logout')

    @rumps.clicked('Config')
    def enter_credentials(self, sender):
        rumps.alert('Enter your credentials in the following file.\nSave it. \nThen retry.')
        subprocess.call(['open', CONFIG_FILE])

    @rumps.clicked('About')
    def open_about(self, sender):
        subprocess.call(['open', 'https://github.com/akigugale/volsbb'])


# --------------------------- Running the app ----------------------------------
if __name__ == '__main__':
    # rumps.debug_mode(True)
    StatusBarApp().run()
