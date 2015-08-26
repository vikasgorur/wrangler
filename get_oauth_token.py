#!/usr/bin/env python3

import twython
import subprocess

from config import Config

def main():
    """This is a script to get the oauth tokens for the bot"""

    twitter = twython.Twython(Config.CONSUMER_KEY, Config.CONSUMER_SECRET)
    auth = twitter.get_authentication_tokens()

    try:
        subprocess.check_call(['open', auth['auth_url']])
    except Exception as e:
        print('Could not open browser.\nPlease go to {0} and authorize '
              'the application enter the PIN provided by Twitter to complete '
              'the token generation process')

    print('PIN: ', end='')
    pin = input()
    if not pin.isdigit():
        print("PIN must be a number")
        exit(1)

    twitter = twython.Twython(Config.CONSUMER_KEY, Config.CONSUMER_SECRET,
        auth['oauth_token'], auth['oauth_token_secret'])
    tokens = twitter.get_authorized_tokens(pin)

    print('OAUTH_TOKEN = \'{0}\''.format(tokens['oauth_token']))
    print('OAUTH_TOKEN_SECRET = \'{0}\''.format(tokens['oauth_token_secret']))

if __name__ == '__main__':
    main()
