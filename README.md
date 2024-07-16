# setup

1. create project
   - in https://console.cloud.google.com/apis/
   - do not forget to "confirm project" and "enable API" in ://console.cloud.google.com/apis/enableflow
   - add
     - google sheets API
     - google docs API
     - google drive API

2. Create service account and "new key".
   - saved as service_account_credentials.json

3. Share folder with service account

4. prepare default sharing account
   `echo 'DEFAULT_SHARE_ACCOUNT = "xxxxxxxxxxxxxxxxxxxx@gmail.com" > gcloud/default_sharing_account.py`

5. install
   - better create a virtual environment
     - python -m venv gcloud_venv
     - source gcloud_venv/bin/activate
     - pip install -r requirements

# Usage


## drive module (files, folders, sharing, etc.)
```py
 import gclould

gcloud.gdrive.create_folder(parent_folder=None,share=True) # share = True to share with default account

# get folders containing name 2024, by default sorted by creation time (newest first)
folders = gcloud.gdrive.get_folders(name="2024")

# get subfolder of first folder
sub_folders = gcloud.gdrive.get_folders(parent=folders[0])

# get list of files
files = gcloud.gdrive.get_files(name="blc",parent=folders[0]) 

# share (in write mode) with default account
gcloud.gdrive.share(files[0]) 

# share with the greater world (in read only mode)
shared = gcloud.gdrive.share(files[0],type='anyone',role="reader")
# note: shared['webViewLink'] is the sharable link
```

## doc module
```py

doc = gcloud.docs.Document(files[0])

# add some text
doc.add_text("this is my test",location="end") # by default append at the end

doc.new_page()

doc.add_image(url_or_existing_fname)
```

# references
- https://ericmjl.github.io/blog/2023/3/8/how-to-automate-the-creation-of-google-docs-with-python/
- https://medium.com/the-team-of-future-learning/integrating-google-drive-api-with-python-a-step-by-step-guide-7811fcd16c44
