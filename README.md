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

## Configuring slack-latex

`slack-latex` requires a Slack API token (for uploading/posting the rendered formulae).
It also expects you to provide a Slack slash command verification token, which allows
the server to verify that requests indeed came from Slack.

### Setup directories and files

Start by copying files to new places:

```bash
sudo cp slacklatex.py /usr/local/bin/
sudo cp config.ini.example /usr/local/etc/config.ini
sudo cp slacklatex.service /lib/systemd/system/
sudo mkdir -p /srv/slacklatex/
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

### Daemonize your slack LaTeX bot

Don't forget to register and enable the slacklatex service with systemd!

```bash
sudo systemctl daemon-reload
sudo systemctl enable slacklatex.service
```

### Start your bot!

```bash
sudo systemctl start slacklatex.service
```
