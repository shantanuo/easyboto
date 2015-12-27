# easyboto
Managing AWS using boto made easy

Save the file easyboto.py in the same directory from where you are running python. Or the import statement will fail.

1) import module

from easyboto import connect

2) initialize the class with login credentials. Access and Secret key of your AWS account is required.

x = connect('xxx', 'yyy')

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

x.startEc2()

12) Terminate ec2 instance.

x.deleteEc2('instance_id')

13) Terminate all ec2 instances.

This does not actually delete all EC2 instances for security reasons. It shows the command to do so :)

x.deleteAllEc2()


## S3 management ##

14) List all buckets or files from a bucket 

x.showBucket()

x.showBucket('bucket_name')

15) Upload file to a given bucket. Optionally specify S3 path

x.uploadFile('bucket_name', '/new/path', '/path/to/file.csv')

16) Download file 

x.downloadFile('bucket_name', 'file.csv')

17) Delete a file from the bucket

x.deleteFile('bucket_name', 'file.csv')

18) List bucket lifeCycle if any:

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

e) Upload or download a file to / from S3 bucket

    uploadFile('bucket_name', '/path/to/file.csv')
    downloadFile('bucket_name', 'file_name.csv')
    

# How to use:

modules required are boto and pandas. Optionally import psycopg2 if you want to run redshift queries.

    from easyboto import myboto
    x = myboto('your_access_key', 'your_secret_key')
    x.showBucket()

# How to install:

    pip install easyboto

# How to save:

easily save the output dict to mongodb test database, collection name: posts

    y=x.showCluster()[0]

    from pymongo import MongoClient
    client = MongoClient()
    db = client.test
    db.posts.insert_one(y)

    db.posts.find_one()

If the function returns dataframe then it is easy to copy the data from pandas to mongodb

    df=x.showSnapshot()
    db.posts.insert_many(df.to_dict('records'))

you may need to correct the data

    df["region"] = df["region"].map(lambda x: str(x).split(':')[-1:])


