import boto

AWS_ACCESS_KEY_ID = 'AKIAIROCAMP2AJ7ZOX2Q'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name = '311clusters'

conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
          AWS_SECRET_ACCESS_KEY)

bucket = conn.get_bucket('311clusters')

from boto.s3.key import Key
k = Key(bucket)
k.key = 'test.json'

string = 'nothing'

import sys
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

k.set_contents_from_string(string,
        cb=percent_cb, num_cb=10)
# f = open('clusters.json')
#
# conn.upload('clusters.json',f,'311clusters')