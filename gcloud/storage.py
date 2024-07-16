from .common import services as SERVICES
from pathlib import Path

from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload


class Gstorage_ESRF:
    def __init__(self):
        self.storage_service = SERVICES.storage

    def upload(self,fname, name_in_gstorage = None):
        """
            if name_in_gstorage is None, fname is used
        """
        if name_in_gstorage is None:
            name_in_gstorage = Path(fname).name
  
        try:
            bucket = self.storage_service.bucket("upload_bucket")
            blob = bucket.blob("image_for_gdocs.png")
            blob.upload_from_filename(fname)
            print(f"Uploaded {fname}")
        except HttpError as error:
            print(f"An error occurred: {error}")
 
        return blob

gstorage = Gstorage_ESRF()
