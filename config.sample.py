class Config:
    # These are both for the app that belongs to the handler's account
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    # Generate these tokens by running get_oauth_token.py
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    EBOOKS_COMMAND = 'ebooks gen /home/vikas/shakti_ebooks/model/shakti_shetty.model'

    BOT_NAME = 'shakti_ebooks'
    HANDLER_NAME = 'vikasgorur'

    RUN_AT = [(11, 15), (0, 0)] # Times of day at which to send DMs (hh, mm)
