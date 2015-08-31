# Wrangler
A daemon to control twitter_ebooks bots via DM.

This daemon lets you control your bot via DM. It periodically sends you a list of candidate tweets generated
by the bot and lets you pick the one you want it to post.

## Install

Make sure you have Python 3 installed.

```bash
$ git clone https://github.com/vikasgorur/wrangler
$ cd wrangler
$ pip3 install -r requirements.txt
```

## Setup

Copy the `model` and `corpus` directories created by [twitter_ebooks](https://github.com/mispy/twitter_ebooks) into the current directory. Verify that your bot works by running the following commands:

```bash
$ ebooks archive <bot name> corpus/<bot name>.json
$ ebooks consume corpus/<bot name>.json
$ ebooks gen model/<bot name>.model
```

Copy `config.sample.py` into `config.py` and edit it to suit your needs. To generate the `OAUTH_TOKEN` and `OAUTH_TOKEN_SECRET` for your bot, use the `gen_oauth_token.py` script:

```bash
$ python3 gen_oauth_token.py
```

When the script opens the browser and takes you to the OAuth screen, make sure that you grant it access to your bot's (something_ebooks) account, not your own.

## Run

Run the daemon with logging to a file:

```bash
$ python3 -m wrangler 2>&1 | tee -a my_ebooks.log
```
