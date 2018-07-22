import requests
import sys
from os import environ
from flask import Flask, request, Response, json

REFRESH_TOKEN = ""
CLIENT_ID = ""
CLIENT_SECRET = ""


def get_secrets():
    try:
        global REFRESH_TOKEN
        global CLIENT_ID
        global CLIENT_SECRET

        REFRESH_TOKEN = environ["REFRESH_TOKEN"]
        CLIENT_ID = environ["CLIENT_ID"]
        CLIENT_SECRET = environ["CLIENT_SECRET"]
    except KeyError:
        print("Missing Token")
        sys.exit(1)


def get_access_token():
    url = "https://www.googleapis.com/oauth2/v4/token"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }

    r = requests.post(url, headers=headers, data=data)

    access_token = r.json()['access_token']

    return access_token


app = Flask(__name__)


@app.route('/drive/list')
def listFiles():
    url = "https://www.googleapis.com/drive/v3/files"
    access_token = get_access_token()

    headers = {
        "authorization": f"Bearer {access_token}"
    }

    r = requests.get(url, headers=headers)

    fileNames = [f["name"] for f in r.json()["files"]]

    html = "<ul>" + "".join([f"<li>{fName}</li>" for fName in fileNames]) + "</ul>"

    return html


@app.route('/drive/upload', methods=["POST"])
def uploadFile():
    access_token = get_access_token()
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable"

    print(request.headers)
    print(request.files)
    for file in request.files.values():
        initial_headers = {
            "authorization": f"Bearer {access_token}",
            "content-type": "application/json; charset=UTF-8",
            "x-upload-content-type": file.mimetype,
        }
        metadata = {
            "name": file.filename
        }

        try:
            r = requests.post(url, json=metadata, headers=initial_headers)
            r.raise_for_status()

            location_uri = r.headers["Location"]
            headers = {
                "content-type": file.mimetype
            }

            r = requests.put(location_uri, data=file.read(), headers=headers)
            r.raise_for_status()

        except Exception as e:
            print(e)
            return Response("Can't upload", status=404)

    return Response("Uploaded", status=200)
