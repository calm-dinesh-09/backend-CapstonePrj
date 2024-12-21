###########################
## Backend Server Code   ##
## Capstone Project      ##
## Name: Dinesh Punja    ##
## Date: 18-12-24        ##
###########################
# For backend:-
# 1. pip install mysql-connector-python
# 2. vi get_message.py
# 3. sudo nano .aws/config
# 4. Paste the below code:

import time
import boto3
import mysql.connector

# Que URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/083351570286/BackendTrafficQueue'

#Specify the database details
host = 'database09.clwg1yhjslce.us-east-1.rds.amazonaws.com'
user = 'admin'
password = 'Test123456#'
database='patientdb'

#Create a SQS Client
sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id='AKIARG2BEA5XDZPJQN53', aws_secret_access_key='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')

#Connect to the RDS MySQL Instance
mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
mycursor = mydb.cursor()

# Receive message from SQS queue
response = sqs.receive_message(QueueUrl=queue_url)
message = response['Messages'][0]

# Delete received message from queue
receipt_handle = message['ReceiptHandle']
sqs.delete_message(
QueueUrl=queue_url,
ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message["Body"])

#Get the customer name and address from the message

customerDetails = message["Body"]
customerDetailsList = customerDetails.split(',')
name = customerDetailsList[0]
address = customerDetailsList[1]

#Write the record to the database

val = (name, address)
sql = "INSERT INTO customers (name, patientissue) VALUES (%s, %s)"

mycursor.execute(sql, val)
mydb.commit()

print("Record inserted in the DB")
