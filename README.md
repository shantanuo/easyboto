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

9) Download snapshot data in csv format

x.snapshotDown('/var/www/html/new_email360_panel/abcx121xxx.csv')

## Redshift Query management ##

10) Execute any Redshift query

x.runQuery('select * from school1_oct_sending limit 10')

## EC2 management ##

11) list all ec2 instances an images in default region (us-eash N. Virginia)

x.showEc2()

x.ShowImages()

12) Create an ec2 instance.

x.startEc2()

13) Terminate ec2 instance.

x.deleteEc2('instance_id')

14) Terminate all ec2 instances.

This does not actually delete all EC2 instances for security reasons. It shows the command to do so :)

x.deteleAllEc2()


## S3 management ##

12) List all buckets and their lifeCycle rules if any

x.showBucketLifeCycle()

x.showBucket()


# modules required are boto and pandas. Optionally import psycopg2 if you want to run redshift queries.

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

    from easyboto import myboto
    x = myboto('your_access_key', 'your_secret_key')
    x.showBucket()
