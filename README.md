# hello world using lambda and api gateway
This project is to generate a hello world web page using aws lambda and api gateway (gw) 

### setup instructions
* need an aws account - free tier preferably

### Create simple lambda function
* open the code at src\main\resources\hello_world.py and copy it in your clipboard
* Open aws cnosole -> services -> aws lambda - > functions -> create  function (in orange color)  ->  author from scratch -> 
  * function name: hello_world
  * function runtime : python 3.8
  * leave everything else at defaults and click on 'create function' in orange at bottom right of page
* Then click on the function just created and below you will see a ui with lambda_function.py in left nav- double click it to open its code- overwrite it with the clipboard code from above github location at src\main\resources\hello_world.py
* Click on 'deploy' 
* Click on dropdown for 'test' in orange and 'configure test event' and give the event a name 'mytestevent'
  *   add or replace with below text 
  *   {
      "key1": "Hello, Lambda ",
      "key2": "value2",
      "key3": "value3"
   }
   * Now click on test (this is like a local lambda unit test)- you should see response in response section as 'Hello Lambda'
 
### Create API Gateway (GW) and tie it with the above lambda function
* click on aws services (in aws console)  -> lambda
* select the function created above and then click on 'add trigger'
  * select 'API gateway'
  * select create an API
  * Select REST API (you can try HTTP api also)
  * Security keep it as "Open" - not ideal except for demo
  * you can click additional settings for the API name etc.
  * Click ADD orange button at bottom
  * Now in lambda -> function -> hello_world -> configuration section you will see the API gateway (with its name) 
  * click on details
  * Click on the API link hyper text which is the actual endpiont of the api gw
  * You should see a screen 'hello from lambda'
  * Now for fun change the text in your hello_world.py and deploy it and refresh the end point and see what happens :)

This concludes our simple hello world with api gw in aws.

Next section below is working with lambda, s3 triggers and dynamodb tables - have fun below !


-------------------------------------------------------
# lambda-s3-uploader-
This project is a demo project to learn how to use lambda to read an incoming s3 bucket object, unzip it to another bucket, then read the txt fiels and load them into dynamodb files the readme.md has to be followed carefully for the setup- Ashwin

### details of what we doing ->

we upload a zip file which has csv files in the zip into s3 bucket 1
the first lambda function watches s3 bucket 1 unzips the same and copies it to s3 bucket 2
the second lambda watches s3 bucket 2 and extracts the csv, and uploads it into dynamdb tables (no sql db) 



### setup instructions
* download the  git project 
* install java and maven (optional if you plan to use java client to upload s3 files- else you can upload directly using aws ui s3)
* All aws objects are created in the us-east-1 area (North Virginia)- if you want to change that change the configs in the py files mainly and any other places you see them.
* create source and destionation s3 bucket as below in same region as lambda function you going to create below
* source: source_s3_<yourname> # can be any name actually which you need to tie up wtih your lambda function
* destionation : extract-file-destination-<yourname> # eg extract-file-destination-ashwin
* change src\main\resources\zip_extractor.py  to your destination bucket from extract-file-destination to extract-file-destination-<yourname>
* change src\main\resources\csv_parser.py - change the region name to your preferred aws region which you creating buckets in - eg us-east-1	
* now create the 2 py funcions in src\main\resources in aws lambda

### configure source s3 bucket and lambda association
* go to lambda-> zip_extractor_function (whcih you created above)-> triggers-> add trigger -> s3 -> see below)
* select the s3 source bucket(eg ource_s3_<yourname>)  as the event source, then 'all object create events' , then tick on recursive acknowlegement and click on add orange button
  
### configure destination s3 bucket and lambda association
* then go to lambda-> csv_parser (whcih you created above)-> triggers-> add trigger -> s3 -> see below)
* select the s3 destination  bucket(eg extract-file-destination-<yourname>)  as the event source, then 'all object create events' , then tick on recursive acknowlegement and click on add orange button

### create the dynamo db tables
* go to aws services ->  dynamodb service and click create table for below 2 tables
** file-meta-data with primary partition key
** student table wtih primary partition key  student_id   

### add the db function layer and map it to the lambda function
* upload the zip file at src\main\resources\layer1-d8d55ad3-8fcf-4ca1-b8d8-73640d1aee65.zip to aws lambda by going to lambda-> layers-> create layer etc
* Next  go to both the lambda function one by one -> click on layers in the diagram -> add a layer-> custom layers-> select the above layer name you gave and version and click add

  
### now lets give the lambda services permission to read write from s3 and dynamodb
* go to   Lambda -> Functions -> zip_extractor -> Edit basic settings -> Existing role -> view the role on iam console -> attach policies  -> s3 full access , AmazonDynamoDBFullAccess
* go to   Lambda -> Functions -> csv_parser -> Edit basic settings -> Existing role -> view the role on iam console -> attach policies  -> s3 full access , AmazonDynamoDBFullAccess

### lets execute the test case
* upload the file at src\main\resources\student.zip into the source s3 bucket you created above
* check the lambda logs by cliking on lambda-> functino-> monitor -> cloudwatch logs in case you want to see wahts going on 
* you should the student_CSE.csv and student_ME.csv in the destination s3 bucket created above.
* you should see the dynamo db tables populated namely file-meta-data and student
  

#### ref https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
  
