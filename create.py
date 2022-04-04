import boto3
import botocore
import copy
import json

# Creates an S3
def create_bucket(session, bucket_name, tag_name, region, private_bucket):
	s3_client = session.client('s3')
	try:
		s3_client.create_bucket(Bucket=bucket_name,
			CreateBucketConfiguration={
			'LocationConstraint': region
			})
		print("[+] Created bucket: " + bucket_name)
		if(private_bucket):
			s3_client.put_public_access_block(
					Bucket=bucket_name,
					PublicAccessBlockConfiguration={
						'BlockPublicAcls': True,
						'IgnorePublicAcls': True,
						'BlockPublicPolicy': True,
						'RestrictPublicBuckets': True
					},
				)
			print("[+] Bucket \"" + bucket_name + "\" has been made private.")

	except botocore.exceptions.ClientError as e:
		print("[-] Bucket \"" + bucket_name + "\" exists.")
		return False
	return True

# Enable logging to log storage bucket
def enable_bucket_logging(session, bucket_name_inbound, bucket_name_logstorage, log_type):
	s3_client = session.client('s3')

	bucket_policy = {
	"Version": "2012-10-17",
	"Statement": [{
		"Sid": "AllowLogstorage",
		"Effect": "Allow",
		"Principal": {
			"Service": "logging.s3.amazonaws.com"
		},
		"Action": ["s3:*"],
		"Resource": f"arn:aws:s3:::{bucket_name_logstorage}/*"
	}]
	}
	bucket_policy = json.dumps(bucket_policy)

	# Configure bucket to log to logstorage
	try:
		 s3_client.put_bucket_logging(
			Bucket = bucket_name_inbound,
			BucketLoggingStatus={
				'LoggingEnabled': {
					'TargetBucket': bucket_name_logstorage,
					'TargetGrants': [
					{
						'Grantee': {
							'Type': 'Group',
							'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery'
						},
						'Permission': 'READ' },
					{
						'Grantee': {
							'Type': 'Group',
							'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery'
						},
						'Permission': 'WRITE'

					},
					],
					'TargetPrefix': log_type + '-accesslogs/'
				}
			}
		)
		 print("[+] Enabled logging for " + bucket_name_inbound + " ---> " + bucket_name_logstorage)
	except botocore.exceptions.ClientError as e:
		print("[-] Error attempting to enable logging: " + e)
		return False

	# Push policy to bucket
	try:
		s3_client.put_bucket_policy(Bucket=bucket_name_logstorage, Policy=bucket_policy)
		print("[+] Put logging.s3.amazonaws.com write policy")
	except botocore.exceptions.ClientError as e:
		print("[-] Error attempting to enable logging: " + e)
		return False
	
	return True 

# Creates a CloudFront instance
def create_cloudfront():
	print("Creating cloudfront instance")
	return

# Creates a CloudWatch instance
def create_cloudwatch():
	print("Creating cloudwatch instance")
	return

def create_test():
	print("create_test")
	return