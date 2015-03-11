# easyboto
Managing AWS using boto made easy

Save the file easyboto.py in the same directory from where you are running python. Or the import statement will fail.

1) import module

from easyboto import myboto

2) initialize the class with login credentials. Access and Secret key of your AWS account is required.

x = myboto('xxx', 'yyy')



3) Describe the current running cluster

x.showCluster()

4) start a new cluster based on the latest snapshot

x.startCluster()

5) This does not actually delete the cluster for security reasons. It shows the command to do so :)

x.deleteCluster()



6) show all backup snapshots

x.showSnapshot()

7) create a snapshot of the current cluster

x.startSnapshot()

8) delete a given snapshot. Snapshot name is required.

x.deleteSnapshot('name_of_snap')

9) Download snapshot data in csv format

x.snapshotDown('/var/www/html/new_email360_panel/abcx121xxx.csv')



10) Execute any Redshift query

x.runQuery('select * from school1_oct_sending limit 10')



11) list all ec2 instances an images in default region (us-eash N. Virginia)

x.showEc2()

x.ShowImages()



12) List all buckets and their lifeCycle rules if any

x.showBucketLifeCycle()

x.showBucket()
