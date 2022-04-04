import argparse
import sys
import boto3
import random
import string

from create import *
from monitor import *

PHOINIX_HELP = \
'''
PHOINIX - AWS Controlled Access Monitoring
@ratiometric
'''

def main():

	parser = argparse.ArgumentParser(add_help=True, description=PHOINIX_HELP, 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('-c','--create', metavar='s3|cf', help='Create a full stack',
		default=None)
	parser.add_argument('-p','--payload', metavar='file.ext', help='File to upload to bucket',
		default=None)
	parser.add_argument('-m','--monitor', metavar='s3|cf', help='Monitor existing stack',
		default=None)
	parser.add_argument('-r','--region', help='Location for resources (defaults us-east-2)',
		default="us-east-2", type=str, action='store')

	parser.add_argument('-d','--delete', help='Prompt to delete S3/CF/CW assets with matching tag',
		default=None)

	# Required variables
	parser.add_argument('tag_name', help='Tag to target for this operation',
		default=None, type=str, action='store')
	parser.add_argument('bucket_name', help='Bucket to target for this operation',
		default=None, type=str, action='store')

	args = parser.parse_args()

	if not (args.create or args.monitor): 
		parser.print_help()
		sys.exit(1)
		return

	try:
		session = boto3.Session(profile_name="default")
		print("[+] Default credentials found.")
	except:
		print("[x] No credentials found in default profile.")
		return

	if(args.create):
		if (args.create.lower()) == "s3":
			bucket_name = args.bucket_name
			bucket_name_logs = args.bucket_name + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5,10)))
			# Create public bucket
			if(create_bucket(session, bucket_name, args.tag_name, args.region, False)):
				# Create private bucket for logging
				create_bucket(session, bucket_name_logs, args.tag_name, args.region, True)
			else:
				print("[x] Stack creation terminated. No assets have been created.")
				return
			# Enable logging of public bucket access to private bucket
			enable_bucket_logging(session, bucket_name, bucket_name_logs, args.create)
			# Enable CloudWatch for private bucket


		elif (args.create.lower()) == "cf":
			print("making cf")
		else:
			return

	if(args.monitor):
		print("monitor")
		return

if __name__ == "__main__":
	main()