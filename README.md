#slack-latex

This is a Slack bot that implements a `/latex` [slash command](https://api.slack.com/slash-commands).

Example usage from within Slack:

`/latex $ E = mc^2 $`

![Demo](https://cloud.githubusercontent.com/assets/1005545/13491495/8405756a-e0e7-11e5-8d22-d76b99ff7a36.gif)

## Installation

This server requires:

* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/en/master/)
* `pdflatex` from [TeXLive](https://www.tug.org/texlive/)
* `convert` from [imagemagick](http://www.imagemagick.org)

On a Ubuntu server, you can install all of these with the following command:

```bash
sudo apt-get install python3-flask python3-requests texlive imagemagick
```

### Optional: with Docker

Clone the repository, copy the `config.ini` and complete it as described 
below. Then, build the docker image:

```bash
docker build -t slacklatex .
```

And run it with port 5000 (or whatever port you like) exposed:

```bash
docker run -d -p 5000:5000 slacklatex
```

## Configuring slack-latex

`slack-latex` requires a Slack API token (for uploading/posting the rendered formulae).
It also expects you to provide a Slack slash command verification token, which allows
the server to verify that requests indeed came from Slack.

### Create a config file for slack-latex

Start by copying the example config file:

```bash
cp config.ini.example config.ini
```

### Create a bot user for your organization

Go to https://my.slack.com/services/new/bot and create a new bot.  Ours is named `latex-bot`.

Once you've created the bot, copy the `API Token` from the Integration Settings
into the `bot_user_api_token` field in your `config.ini`.

Feel free to configure your bot as you see fit (name, avatar, etc).

### Create a slash command for your organization

Go to https://my.slack.com/services/new/slash-commands and create a new slash
command.  We recommend `/latex`.

Set the URL to the url you plan to run this server from.  Make sure your
port matches the one in `main.py`.

Copy the verification token from Integration Settings -> Token into
`config.ini` as the `slash_command_verification_token` value.

### Launch the server

Start up your server:

```bash
python3 main.py
```

Then, try testing out your shiny new slash command.
