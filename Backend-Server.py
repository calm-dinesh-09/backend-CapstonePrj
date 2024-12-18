###########################
## Backend Server Code   ##
## Capstone Prject       ##
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

queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/346067777770/demo-queue'

#Specify the database details
host = 'database-1.cfioemrww3c1.ap-southeast-2.rds.amazonaws.com'
user = 'admin'
password = 'your password'
database='demo'

#Create a SQS Client
sqs = boto3.client('sqs')

#Connect to the RDS MySQL Instance
mydb = mysql.connector.connect(host=’host’, user=’admin’, password=’password’, database=database)
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
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"

mycursor.execute(sql, val)
mydb.commit()

print("Record inserted in the DB")
