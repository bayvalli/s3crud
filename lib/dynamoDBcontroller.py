import boto3
import requests
import json
from config import Config
from decimal import Decimal

class dynamodbctrl():
    def __init__(self, items, tablename=Config.DYNAMODB_TABLENAME):
        self.tablename = tablename
        self.items = items
        self.key = "name"
        self.key2 = "md5"
        self.url = Config.API_GATEWAY_URL
        self.dynamodb = boto3.resource('dynamodb')

    def check_table(self):
        r = requests.get("{}/check/{}".format(self.url, self.tablename))
        if(r.status_code == 200):
            return True
        return False

    def create_table(self):
        url = "{}/create".format(self.url)
        body = { 'tablename': self.tablename }

        r = requests.post(url, data=json.dumps(body))
        print(r.content)
        self.dynamodb.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)


    def put_item(self):
        if(self.check_table() == False):
            self.create_table()

        url = "{}/add-item".format(self.url)
        body = { 'tablename': self.tablename, 'items': self.items }

        r = requests.post(url, data=json.dumps(body))
        print(r.content)
        

    def delete_item(self):
        if(self.check_table() == False):
            return None

        url = "{}/delete-item".format(self.url)
        body = { 'tablename': self.tablename, 'items': self.items }

        r = requests.post(url, data=json.dumps(body))
        print(r.content)

    def query_and_delete_item(self): # items dict includes only primary keys, function will query the item in all tables
        if(self.check_table() == False):
            return None
        
        url = "{}/query-item".format(self.url)
        body = {'items': self.items }
        r = requests.post(url, data=json.dumps(body))
        print("DEBUG", r.status_code, type(r.content))
        response_dict = eval(r.content)
        print(response_dict)
        for tablename, query in response_dict.items():
            print(tablename,query)
            if query["Items"] != []:
                self.tablename = tablename
                self.delete_item()
        
        return json.dumps(self.items + " is deleted")
