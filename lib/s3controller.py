import os
import hashlib
import boto3
import datetime

from lib.dynamoDBcontroller import dynamodbctrl
from config import Config

def md5(filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

class deletefile():
    def __init__(self, name):
        self.name = name
        self.s3 = boto3.resource('s3')
        
    def deleteUploaded(self):
        try: 
            obj = self.s3.Object(Config.S3_BUCKET_NAME, self.name)
            obj.delete()
            return True
        except:
            return False

class uploadfile():
    def __init__(self, name, type=None, size=None, not_allowed_msg='', dbtablename=Config.DYNAMODB_TABLENAME):
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "data/%s" % name
        self.thumbnail_url = "thumbnail/%s" % name
        self.delete_url = "delete/%s" % name
        self.delete_type = "DELETE"
        self.uploadtime = datetime.datetime.now().ctime()
        self.s3 = boto3.resource('s3')
        self.dynamodb_tablename = dbtablename

    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False

    def get_file(self):
        if self.type != None:
            # POST an image
            if self.type.startswith('image'):
                self.s3.meta.client.upload_file(self.url, Config.S3_BUCKET_NAME, self.name, ExtraArgs={
                                            "ACL": "public-read",
                                        })
                self.s3.meta.client.upload_file("data/{}".format(self.thumbnail_url), Config.S3_BUCKET_NAME, self.thumbnail_url, ExtraArgs={
                                            "ACL": "public-read",
                                        })    
                items = {"name": self.name,
                        "type": self.type,
                        "size": self.size, 
                        "url": "{}/{}".format(Config.S3_BUCKET_URL, self.name), 
                        "thumbnailUrl": "{}/{}".format(Config.S3_BUCKET_URL, self.thumbnail_url),
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,
                        "md5": md5(self.url),
                        "uploadtime": self.uploadtime} 

                meta = dynamodbctrl(items, self.dynamodb_tablename)        
                meta.put_item()
                return items
            
            # POST an normal file
            elif self.not_allowed_msg == '':
                self.s3.meta.client.upload_file(self.url, Config.S3_BUCKET_NAME, self.name, ExtraArgs={
                                            "ACL": "public-read",
                                        })
                items = {"name": self.name,
                        "type": self.type,
                        "size": self.size, 
                        "url": "{}/{}".format(Config.S3_BUCKET_URL, self.name),  
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,
                        "md5": md5(self.url),
                        "uploadtime": self.uploadtime}
                
                meta = dynamodbctrl(items, self.dynamodb_tablename)
                meta.put_item()        
                return items

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size,}

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": self.size, 
                    "url": self.url, 
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
        
        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size, 
                    "url": self.url, 
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
