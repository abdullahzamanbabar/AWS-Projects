import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import CloudWatchPutMetric
import s3bucket
import sprint3_dynamo

def lambda_handler(events, context):
	
	URL_list = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")	# To read from bucket. s3bucket.py
	dynamo_sprint3_Url_list = sprint3_dynamo.getting_sprint3_dynamo_data()
	values = dict()
	cw = CloudWatchPutMetric() # It puts avail and latency metrics on cloud watch Line 19. imported from cloudwatch_putMetric.py
	
	for Url in dynamo_sprint3_Url_list:
		avail = get_availability(Url)	# Line 31
		dimensions = [
			{"Name": "URL", "Value": Url}
			]
		# Calls the put_data method from cloudwatch_putMetric.py Line 10
		cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Availability+"_"+Url, dimensions, avail)
		
		latency = get_latency(Url)		# Line 39
		dimensions = [
			{"Name": "URL", "Value": Url}
			]
		
		cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Latency+"_"+Url, dimensions, latency)
		
		values.update({"availability":avail,"Latency":latency})
	return values	# Returns dictionary with avail and latency values. Line 42 in stack

def get_availability(Url):
	http = urllib3.PoolManager()
	response = http.request("GET", Url)
	if response.status==200:
		return 1.0
	else:
		return 0.0

def get_latency(Url):		# Measures latency by difference of response time
	http = urllib3.PoolManager()
	start = datetime.datetime.now()
	response = http.request("GET", Url)
	end = datetime.datetime.now()
	delta = end - start
	latencySec = round(delta.microseconds * .000001, 6)
	return latencySec