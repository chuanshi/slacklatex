FROM ubuntu:latest

# dependencies
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository main &&\
    add-apt-repository universe &&\
    apt-get update &&\
    apt-get install -y python3-flask python3-requests texlive imagemagick texlive-latex-extra

# make user to run server
RUN useradd -m -g users flask
WORKDIR /home/flask

ADD main.py main.py
ADD template.tex template.tex
ADD config.ini config.ini
RUN chown flask:users *

EXPOSE 5000

USER flask
CMD ["python3", "main.py"]
