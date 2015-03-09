# easyboto
manage redshift using boto

Save the file easyboto.py in the same directory from where you are running python.

1) import module
from easyboto import myboto

2) initialize the class with login credentials
x = myboto('xxx', 'yyy')

3) a new connection object called x is created that can be used now...
 
4) Describe the current running cluster
x.showCluster()

5) start a new cluster based on the latest snapshot
x.startCluster()

6) This does not actually delete the cluster for security reasons. It shows the command to do so :)
x.deleteCluster()
 
7) show all backup snapshots 
x.SnapshotShow() 

8) create a snapshot of the current cluster
x.snapshotCreate()

9) delete a given snapshot
x.snapshotDelete()

10) Download snapshot data in csv format 
x.SnapshotDown('/var/www/html/new_email360_panel/abcx121xxx.csv')

11) Execute any query
x.runQuery('select * from school1_oct_sending limit 10')

