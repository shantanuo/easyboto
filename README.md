# easyboto
Managing AWS using boto made easy

Save the file easyboto.py in the same directory from where you are running python. Or the import statement will fail.

1) import module

from easyboto import myboto

2) initialize the class with login credentials. Access and Secret key of your AWS account is required.

x = myboto('xxx', 'yyy')

## Redshift Cluster management ##

3) Describe the current running cluster

x.showCluster()

4) start a new cluster based on the latest snapshot

x.startCluster()

5) This does not actually delete the cluster for security reasons. It shows the command to do so :)

x.deleteCluster()

## Redshift Snapshot management ##

6) show all backup snapshots

x.showSnapshot()

7) create a snapshot of the current cluster

x.startSnapshot()

8) delete a given snapshot. Snapshot name is required.

x.deleteSnapshot('name_of_snap')

## Redshift Query management ##

9) Execute any Redshift query

x.runQuery('select * from school1_oct_sending limit 10')

## EC2 management ##

10) list all ec2 instances and all images in default region (us-eash N. Virginia)

x.showEc2()

x.ShowImages()

11) Create an ec2 instance.
    
    image id, region, key, type and security group needs to be changed in the source file.
    'ami-fc73d494', 'us-east-1a', 'april142015', 't1.micro', ['all port open']

x.startEc2()

12) Terminate ec2 instance.

x.deleteEc2('instance_id')

13) Terminate all ec2 instances.

This does not actually delete all EC2 instances for security reasons. It shows the command to do so :)

x.deteleAllEc2()


## S3 management ##

14) List all buckets or files from a bucket 

x.showBucket()

x.showBucket('bucket_name')

15) Upload file to a given bucket. Optionally specify S3 path

x.upload('bucket_name', '/new/path', '/path/to/file.csv')

16) Delete a file from given bucket

x.delete('bucket_name', 'file.csv')

17) List bucket lifeCycle if any:

x.showBucketLifeCycle()


## easyboto cheatsheet

a) show details of cluster, snapshot, buckets, files in bucket, bucket life Cycle, ec2 or images.

    showCluster
    showSnapshot
    showBucket
    showBucket('bucket_name')
    showBucketLifeCycle
    showEc2
    showImages

b) Start a new cluster based on latest snapshot, create a snapshot of running cluster or start an ec2 instance

    startCluster
    startSnapshot
    startEc2

c) delete a given ec2 instance or snapsshot. Statements are generated to delete all instances or to delete current cluster.

    deleteEc2('instance_id_to_delete')
    deleteAllEc2
    deleteCluster
    deleteSnapshot('snapshot_identifier_todelete')
    deleteFile('bucket_name', 'file_name')

d) run any Redshift query

    runQuery(my_query):

e) Upload a local file to S3 bucket

    upload('bucket_name', '/path/to/file.csv')
    

# How to use:

    modules required are boto and pandas. Optionally import psycopg2 if you want to run redshift queries.

    from easyboto import myboto
    x = myboto('your_access_key', 'your_secret_key')
    x.showBucket()
