#!/usr/bin/env python3

import subprocess
import tweepy

from config import Config

def main():
    """This is a script to get the oauth tokens for the bot"""

    auth = tweepy.OAuthHandler(Config.CONSUMER_KEY, Config.CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()

    try:
        subprocess.check_call(['open', auth_url])
    except Exception as e:
        print('Could not open browser.\nPlease go to {0} and authorize '
              'the application enter the PIN provided by Twitter to complete '
              'the token generation process'.format(auth['auth_url']))

    print('PIN: ', end='')
    pin = input()
    if not pin.isdigit():
        print("PIN must be a number")
        exit(1)

    (access_token, access_token_secret) = auth.get_access_token(pin)

    print('OAUTH_TOKEN = \'{0}\''.format(access_token))
    print('OAUTH_TOKEN_SECRET = \'{0}\''.format(access_token_secret))

if __name__ == '__main__':
    main()
