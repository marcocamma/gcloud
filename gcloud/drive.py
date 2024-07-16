
from .common import guess_mime
from .common import services as SERVICES
from pathlib import Path

from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload

from .default_sharing_account import DEFAULT_SHARE_ACCOUNT

class Gdrive_ESRF:
    def __init__(self,default_account=DEFAULT_SHARE_ACCOUNT):
        """
        if default_account is None, by default new uploaded files will not be shared, else provide valid google account """
        self.drive_service = SERVICES.drive
        self.default_account = default_account

    def share(self,file, share_with_account = "default", role="writer", type="user"):
        if share_with_account == "default": share_with_account = self.default_account

        file_id = file["id"] if isinstance(file,dict) else file

        types = "user","anyone"
        if not type in types:
            raise ValueError(f"can share with {types}")

        if type == "user":
            permission = {
                'type': type,
                'role': role, #This role grants the user edit permissions to the file
                'emailAddress': share_with_account,
            }
        elif type == "anyone":
            permission = {
                'type': type,
                'role': role, #This role grants the user edit permissions to the file
            }
        try:
            self.drive_service.permissions().create(fileId=file_id, body=permission, sendNotificationEmail=None).execute()
            print(f"Shared {file} with {share_with_account} (role {role})")
        except HttpError as error:
            print(f"An error occurred: {error}")
        file_info = self.drive_service.files().get(fileId=file_id,fields='id, webViewLink, webContentLink, parents').execute()
        return file_info

    def get(self, what="folders", name=None, sort=True, parent=None):
        """
        if sort is True
          return list sorted by oldest to newest (i.e. most recently created one is [-1])
        """
        if what == "folders":
            query ="mimeType='application/vnd.google-apps.folder'"
        elif what == "files":
            query =""
       
        if name is not None:
            query += f" and name contains '{name}'"
        if parent is not None:
            if isinstance(parent,dict):
                parent_id = parent["id"]
            else:
                parent_id = parent
            query += f" and '{parent_id}' in parents"
 
        if query.startswith(" and"): query = query[4:]
        page_token = None
 
        data = []
        while True:
          response = (
              self.drive_service.files()
              .list(
                  q=query,
                  spaces="drive",
                  fields="nextPageToken, files(id, mimeType, kind, modifiedTime, createdTime, name)",
                  pageToken=page_token,
              )
              .execute()
          )
          
          data.extend( response.get("files", []) )
          page_token = response.get("nextPageToken", None)
          if page_token is None:
              break
        if sort:
            data = sorted(data, key=lambda d: d['createdTime'],reverse= True)
        return data

    def get_files(self,  name=None, sort=True, parent=None):
        return self.get(what="files",name=name,parent=parent, sort=sort)

    def get_folders(self, name=None, sort=True, parent=None):
        return self.get(what="folders",name=name, sort=sort, parent=parent)

    def create_folder(self,folder_name,parent_folder=None,share=True):
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder is not None:
            parent_folder_id = parent_folder if isinstance(parent_folder,str) else parent_folder.get("id")
            file_metadata["parents"] = [parent_folder_id]
        
        try:
            folder = self.drive_service.files().create(body=file_metadata, fields="id").execute()
            print(f'Folder ID: "{folder.get("id")}".')
 
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
 
        if share:
            self.share(folder)
 
        return folder.get("id")


    def upload(self,fname, name_in_gdocs = None, mimetype=None,share=True,folder=None):
        """
            if name_in_gdocs is None, fname is used
            if mimetype is None, autodetect based on extension
        """
        if name_in_gdocs is None:
            name_in_gdocs = Path(fname).name
  
        file_metadata = { 'name': name_in_gdocs }
        if folder is not None:
            folder_id = folder if isinstance(str) else folder.get("id")
            file_metadata["parents"] = [folder_id]
 
        if mimetype is None:
            mimetype = guess_mime(fname)
 
        try:
            media = MediaFileUpload(fname, mimetype=mimetype)
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink, webContentLink, parents').execute()
            print(f"Uploaded {file}")
        except HttpError as error:
            print(f"An error occurred: {error}")
 
        if share:
            self.share(file)
        
        return file

gdrive = Gdrive_ESRF()
