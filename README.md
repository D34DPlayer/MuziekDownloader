# MuziekDownloader
[![Heroku App Status](http://heroku-shields.herokuapp.com/muziek-downloader)](https://muziek-downloader.herokuapp.com)

Muziek is a web application that allows you to download songs from YouTube and directly add the song's metadata.

## Usage
You can access the web application either from the [official website](https://muziek-downloader.herokuapp.com), in an environment [running locally](#local-setup) or even an environement hosted by yourself on [Heroku](#heroku-host).

Once at the website you can enter your song's URL, fill up the info and start downloading!

## Features
- Web server using Django, WSGI compatible.
- Production ready with Heroku setup and gunicorn.
- The download of the songs and the tag edition is done server-side.
- Search into the other entries submitted.
- Admin section to handle the database.
- REST API to trigger downloads, check status and download files locally.

## Local setup
MuziekDownloader requires on Python 3.5 or greater. It also relies on ffmpeg/libav:

- On linux, ffmpeg should be available in your package manager: `sudo apt install ffmpeg` or similar.
- On Windows, you can install ffmpeg via [chocolatey](https://chocolatey.org/packages/ffmpeg), or download it manually from [here](https://ffmpeg.org/download.html#build-windows).

Once ffmpeg is installed you can clone this repository, enter the project's folder, download the dependencies, set up the database and run the server.

*To run the server locally, debug mode needs to be enabled, you can do it manually in MuziekDownloader/settings.py or run the command below.*

```
# SETUP
# Clone the repository
git clone https://github.com/D34DPlayer/MuziekDownloader.git
# Enter the folder
cd MuziekDownloader
# Install the requirements, a virtual environnement is recommended.
pip install -r requirements.txt
# Enable debug mode, you can also just edit the file manually
sed 's/DEBUG = False/DEBUG = True/g' MuziekDownloader/settings.py > MuziekDownloader/settings.py
# Prepare the database
python manage.py migrate
```
```
# STARTUP
# Run the server with Django
python manage.py runserver
# Run the server with gunicorn
gunicorn MuziekDownloader.wsgi
```
For a local setup, the server used won't really matter, unless you expect high traffic on it.

## Heroku host

MuziekDownloader has been optimized to work on a Heroku environment, to the point that you can set up an environment in 1-click:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

If you prefer to install it yourself, for example to do local changes, it'll be really simple as well:
- Clone this repository.
- Do the changes you need to do.
- Create a heroku app, with the addons, buildpacks and config vars included in [app.json](https://github.com/D34DPlayer/MuziekDownloader/blob/main/app.json).
- Push the modified version.
- Profit!
