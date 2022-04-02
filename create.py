import boto3
import botocore

# Creates an S3
def create_bucket(session, bucket_name, tag_name, region, privacy):
	'''
	Create an S3
	:param credentials: Creds with xyz permission
	:param bucket_name: Name of the bucket to create
	:param region: Region to create bucket in
	:param privacy: true = private, false = public
	'''
	s3_client = session.client('s3')
	try:
		s3_client.create_bucket(Bucket=bucket_name,
			CreateBucketConfiguration={
			'LocationConstraint': region
			})
		print("[+] Created bucket: " + bucket_name)
		if(privacy):
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
		#the only reason this should fail is due to another bucket existing.
		print(e)
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