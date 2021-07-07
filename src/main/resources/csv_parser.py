import boto3
import csv
import db_util as db

def lambda_handler(event, context):
	region = 'us-east-1'
	recList = []
	try:
		s3 = boto3.client('s3')
		obj_key = event['Records'][0]['s3']['object']['key']
		dyndb = boto3.client('dynamodb', region_name=region)
		source = event['Records'][0]['s3']['bucket']['name']
		filesource=s3.get_object(Bucket=source, Key=obj_key)
		recList = filesource['Body'].read().decode().split('\r\n')
		firstRecord = True
		csv_reader = csv.reader(recList, delimiter=',',quotechar='"')
		for row in csv_reader:
			if(firstRecord):
				firstRecord = False
				continue
			student_id = row[0]
			name = row[1]
			stream = row[2]
			marks = row[3]
			grade = row[4]
			item={}
			item['student_id'] = {'S':student_id}
			item['name'] = {'S' : name}
			item['stream'] = {'S' : stream}
			item['marks'] = {'S': marks}
			item['grade'] = {'S':grade}
			response = db.db_util(item, 'student',region)
		print('Put succeeded')
	except Exception as e:
		print(str(e))