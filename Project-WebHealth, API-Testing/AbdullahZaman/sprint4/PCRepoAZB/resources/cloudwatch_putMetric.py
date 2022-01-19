import boto3
import constants as constants

class CloudWatchPutMetric:
    
    def __init__(self):
        self.client = boto3.client("cloudwatch")
    
    # It will put the metric data on cloud watch. ==> webhealth_lambda.py Line 19
    def put_data(self, nameSpace, metricName, dimensions, value):
        response = self.client.put_metric_data(
            Namespace = nameSpace,
            MetricData = [{
                "MetricName": metricName,
                "Dimensions": dimensions,
                "Value": value,
                }],
            )

