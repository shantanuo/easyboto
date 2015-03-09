# easyboto
manage redshift using boto

Save the file easyboto.py in the same directory from where you are running python.

1) import module

from easyboto import myboto

2) initialize the class with login credentials

x = myboto('xxx', 'yyy')

3) Describe the current running cluster

x.showCluster()

4) start a new cluster based on the latest snapshot

x.startCluster()

5) This does not actually delete the cluster for security reasons. It shows the command to do so :)

x.deleteCluster()
 
6) show all backup snapshots 

x.SnapshotShow() 

7) create a snapshot of the current cluster

x.snapshotCreate()

8) delete a given snapshot

x.snapshotDelete()

9) Download snapshot data in csv format 

x.SnapshotDown('/var/www/html/new_email360_panel/abcx121xxx.csv')

10) Execute any query

x.runQuery('select * from school1_oct_sending limit 10')
