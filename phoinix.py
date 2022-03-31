import boto3
import os
from operator import attrgetter
# gzip for cloudfront logging
# import gzip
try:
	os.mkdir("./output")
except:
    pass

# hardcoded stuff so i remember what features to add, very lazy. very cool. :)
log_type = "bucket"
bucket_name = "my_bucket"
canary = "my_canary"

print("[+] Using default credentials.")
session = boto3.Session(profile_name='default')
s3_session = session.resource('s3')
s3_bucket = s3_session.Bucket(bucket_name)
s3_bucket_sorted_objects = sorted(s3_bucket.objects.all(), key=attrgetter('last_modified'))

print("[+] Identified " + str(len(s3_bucket_sorted_objects)) + " log files from: " + bucket_name)
# hardcoded number of files to return, very lazy. very cool. :)
print("[+] Reading last [5] log file written")

# ignoring cloudfront logs that were in the same logging bucket used for testing, very lazy. very cool. :)
for s3_bucket_object in s3_bucket_sorted_objects[-5:]:
	if '.gz' in s3_bucket_object.key:
		continue
	print("[+] Downloading: " + s3_bucket_object.key)

	# Just in case we're dropping inside a directory
	s3_bucket.download_file(s3_bucket_object.key, './output/' + ''.join(char for char in s3_bucket_object.key if char.isalnum()))

results_file = open(os.path.join("results.txt"), "w+")
log_files = os.listdir("./output")
for log in log_files:
	openfile = open(os.path.join("./output", log), 'rb')
	for line in openfile:
		if canary in line.decode("utf-8"):
			results_file.write(line.decode("utf-8"))
	openfile.close()
results_file.close()