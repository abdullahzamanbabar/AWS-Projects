import boto3

def store_file(buck):
    s3= boto3.client('s3')
    try:
        s3.create_bucket(Bucket=buck, CreateBucketConfiguration={       # creating our s3 bucket and storing file
        'LocationConstraint': 'us-east-2'})
        s3.upload_file("resources/urls.txt", buck ,"urlsList.txt")
    except:
        s3.upload_file("resources/urls.txt", buck ,"urlsList.txt")
        

def read_file(buck, item):
    name_url = []
    s3 = boto3.resource('s3')
    obj = s3.Object(buck, item)
    for line in obj.get()['Body']._raw_stream.readline():       # reading from the file in s3 bucket
        name_url.append(line)
    return name_url