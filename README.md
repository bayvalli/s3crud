# S3 CRUD

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) that supports Amazon S3 and DynamoDB with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.


## Installation
- Before begin, set the AWS config and credentials files into  `~/.aws/` directory.

    > ~/.aws/config
    [default]
    region=eu-west-3


    > ~/.aws/credentials
    [default]
    aws_access_key_id = XXXXXXXXXXXXXXXXXX 
    aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- Reconfigure config.py
    > DEBUG = False \
    TESTING = False \
    CSRF_ENABLED = True \
    SECRET_KEY = 'super-secret-random-key-here' \
    DYNAMODB_TABLENAME = 'metadata' \
    S3_BUCKET_NAME = 'blghomework1' \
    S3_BUCKET_URL = 'http://{}.s3.amazonaws.com'.format(S3_BUCKET_NAME)  \
    UPLOAD_FOLDER = 'data/' \
    THUMBNAIL_FOLDER = 'data/thumbnail/' \
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 \
    ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx', 'pdf', 'mp4']) \
    IGNORED_FILES = set(['.gitignore']) \


- Install system package. See the `system_package.txt` file. (*Unix)

- Create virtual enviroment (use `virtualenv`) and activate it.

- Then install python packages:  
```
$ pip install -r requirements.txt
```

- Run it:

```
$ python app.py
```

- Go to http://127.0.0.1:5000

