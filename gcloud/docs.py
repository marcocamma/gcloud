
from .common import services as SERVICES
from . import gdrive as GDRIVE
from pathlib import Path
from os import path
from googleapiclient.errors import HttpError

def _add_location(request,location):
    if location == "end":
        request['endOfSegmentLocation'] =  {}
    elif location == "beginning":
        request['location'] = { 'index': 1}
    else:
        request['location'] = { 'index': location}
    return request

def new_page():
    return '<hr class=" pb">'

def new_line():
    return "\n"

class Document:
    def __init__(self,document):
        document_id = document["id"] if isinstance(document,dict) else document
        self._id = document_id
        self._doc_resources = SERVICES.docs.documents()
        self.requests = []

    def update(self):
        body = {'requests': self.requests}
        result = self._doc_resources.batchUpdate(documentId=self._id, body=body).execute()
        # empty buffer
        self.requests = []
        return result

    def new_page(self,location="end",execute=True):
        page_break = {}
        page_break = _add_location(page_break,location)
        request = {'insertPageBreak' : page_break }
        self.requests.append(request)
        if execute:
            return self.update()
        else:
            return requests

    def add_text(self,text,location="end",prepend_newline=True,execute=True):
        if prepend_newline: text = new_line() + text
        insert_text = { 'text': text } 
        insert_text = _add_location(insert_text,location)
        request = {'insert_text': insert_text }
        self.requests.append(request)
        if execute:
            return self.update()
        else:
            return requests

    def add_image(self,img, location="end",height_cm=1, width_cm=1):
        if path.isfile(img):
            img = GDRIVE.upload(img)
            GDRIVE.share(img,type="anyone")
            url = img['webContentLink']
            uploaded = True
        else:
            upload = False
            url = img
        cm_to_pt = 72/2.54
        height_pt = int(height_cm*cm_to_pt)
        width_pt = int(width_cm*cm_to_pt)
        insert_image = {
            'uri': url,
            'objectSize': {
                'height': { 'magnitude': height_pt, 'unit': 'PT' },
                'width': { 'magnitude': width_pt, 'unit': 'PT' },
            }
        }
        insert_image = _add_location(insert_image,location)
        request = { 'insertInlineImage': insert_image } 
        self.requests.append(request)
        print(self.requests)
        response = self.update()
        if uploaded:
            GDRIVE.share(img,type="user")
        return response



class Gdocs_ESRF:
    def __init__(self):
        self.docs_service = SERVICES.docs

    def get_document(self,doc_id):
        return Document(doc_id)

gdocs = Gdocs_ESRF()
