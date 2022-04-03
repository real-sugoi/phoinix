<img src="./payloads/elmo.png" alt="elmo" width="675px" height="200px">

# PHOINIX - AWS Controlled Access Monitoring

Create, monitor, and delete S3/CF/CW instances that monitor access.

Useful for phishing campaigns and blind XSS payloads where you may need to serve a specific payload file. 

Note that this will always create two buckets, one with public ACL's enabled and one without.

e.g "my_bucket" and "my_bucket-[a-z0-9]{5,10}"

[a-z0-9]{5,10} is an attempt avoid any sort of automated enumeration of buckets that attempts to associate an S3 with an active campaign based on how this tool creates buckets.

# Installation
pip install -r requirements.txt

# Usage
phoinix.py -c s3 tagname bucketname
