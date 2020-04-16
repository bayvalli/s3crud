import boto3
from config import Config

class dynamodbctrl():
    def __init__(self, items, tablename=Config.DYNAMODB_TABLENAME):
        self.tablename = tablename
        self.items = items
        self.key = "name"
        self.key2 = "md5"
        self.ReadCapacityUnits = 5
        self.WriteCapacityUnits = 5
        self.dynamo = boto3.resource("dynamodb")

    def create_table(self):
        table = self.dynamo.create_table(
            TableName= self.tablename,
            KeySchema=[
                {
                    'AttributeName': self.key, 
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': self.key2, 
                    'KeyType': 'RANGE'
                }
            ], 
            AttributeDefinitions=[
                {
                    'AttributeName': self.key, 
                    'AttributeType': 'S'
                }, 
                {
                    'AttributeName': self.key2, 
                    'AttributeType': 'S'
                }, 
            ], 
            ProvisionedThroughput={
                'ReadCapacityUnits': self.ReadCapacityUnits, 
                'WriteCapacityUnits': self.WriteCapacityUnits
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)

    def put_item(self):
        if self.tablename in self.dynamo.meta.client.list_tables()['TableNames']:
            table = self.dynamo.Table(self.tablename)
            table.put_item(
                Item=self.items
            )
        else:
            self.create_table()
            self.put_item()

    def delete_item(self):
        if self.tablename in self.dynamo.meta.client.list_tables()['TableNames']:
            table = self.dynamo.Table(self.tablename)
            table.delete_item(
                Key={
                    self.key: self.items[self.key],
                    self.key2: self.items[self.key2]
                }
            )    