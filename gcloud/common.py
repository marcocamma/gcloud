from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from google.cloud import storage

import mimetypes

mimetypes.init()

def _connect_to_service(service="drive"):
    services = "drive","docs","storage"
    if not service in services:
        raise ValueError(f"service must be one of {services}")
    try:
        creds = service_account.Credentials.from_service_account_file(
            'service_account_credentials.json',
            scopes=['https://www.googleapis.com/auth/drive',
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/drive.metadata',
            ]
        )
        if service == "drive":
            service = build('drive', 'v3', credentials=creds)
        if service == "docs":
            service = build('docs', 'v1', credentials=creds)
        if service == "storage":
            service = storage.Client(credentials=creds)

    except HttpError as error:
        print(f"An error occurred: {error}")
    return service

class GoogleServices:
    def __init__(self):
        self.drive = _connect_to_service("drive")
        self.docs = _connect_to_service("docs")
#        self.storage = _connect_to_service("storage")

def guess_mime(fname):
    mimetype = mimetypes.guess_type(fname)[0]


services = GoogleServices()
