class Config:
    # These are both for the app that belongs to the handler's account
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    # Generate these tokens by running get_oauth_token.py
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    # Make sure you have the twitter_ebooks 'model' and 'corpus' directories
    # inside the current directory.
    EBOOKS_UPDATE = [
        'ebooks archive shakti_shetty corpus/shakti_shetty.json',
        'ebooks consume corpus/shakti_shetty.json'
    ]
    EBOOKS_GENERATE = 'ebooks gen model/shakti_shetty.model'

    BOT_NAME = 'shakti_ebooks'
    HANDLER_NAME = 'vikasgorur'

    RUN_AT = [(11, 15), (0, 0)] # Times of day at which to send DMs (hh, mm)
