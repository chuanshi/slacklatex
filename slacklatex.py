#!/usr/bin/env python3
from string import Template
import configparser
import os
import subprocess
import tempfile
import argparse

from flask import Flask, Response, request
import requests as py3reqs

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", dest='config_file', default='/usr/local/etc/slacklatex.conf', type=str)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config_file)
SLASH_COMMAND_TOKEN = config.get('Slack', 'slash_command_verification_token')
API_TOKEN = config.get('Slack', 'bot_user_api_token')
LISTEN_PORT = int(config.get('Slack', 'listen_port'))
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def render_latex():
    if request.form['token'] != SLASH_COMMAND_TOKEN:
        return Response("NOT AUTHORIZED" + str(request.values), 403)
    with tempfile.TemporaryDirectory() as work_dir:
        try:
            str2png(request.form['text'], work_dir)
        except Exception as e:
            print(e)
            return "Invalid LaTeX?"
        out_url = "https://slack.com/api/files.upload"
        payload = {}
        files = {'file':open(os.path.join(work_dir, 'out.png'), 'rb')}
        payload['token'] = API_TOKEN
        payload['filename'] = 'LaTeX.png'
        payload['initial_comment'] = request.form['text']
        payload['channels'] = [request.form['channel_id']]
        r = py3reqs.post(out_url, params=payload, files=files)
        r.raise_for_status()
    return ""


def str2png(input_string, work_dir):
    with open('template.tex','r') as f:
        s = Template(f.read())
    out_txt = s.substitute(my_text=input_string)

    with open(os.path.join(work_dir, 'out.tex'),'w') as f:
        f.write(out_txt)
    subprocess.check_call(['pdflatex', '-halt-on-error', 'out.tex'], cwd=work_dir, stdout=None, stderr=None)
    subprocess.check_call(['convert', '-density', '300', 'out.pdf', '-quality', '100', '-sharpen', '0x1.0', 'out.png'], cwd=work_dir, stdout=None, stderr=None)

if __name__=="__main__":
    app.run("127.0.0.1", port=LISTEN_PORT)
