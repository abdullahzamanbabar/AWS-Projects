import datetime
import urllib3

URL_TO_MONITOR = ["www.skipq.org", "www.youtube.com", "www.google.com", "www.linkedin.com"]

def lambda_handler(events, context):
	values = dict()
	for url in URL_TO_MONITOR:
	    avail = get_availability(url)
	    latency = get_latency(url)
	    values.update({"availability "+url:avail,"Latency "+url:latency})
	return values

def get_availability(url):
	http = urllib3.PoolManager()
	response = http.request("GET", url)
	if response.status==200:
		return 1.0
	else:
		return 0.0

def get_latency(url):
	http = urllib3.PoolManager()
	start = datetime.datetime.now()
	response = http.request("GET", url)
	end = datetime.datetime.now()
	delta = end - start
	latencySec = round(delta.microseconds * .000001, 6)
	return latencySec