# easyboto
manage redshift using boto

# Save the file easyboto.py in the same directory from where you are running python.

# import module
from easyboto import myboto

# initialize the class with login credentials
x = myboto('xxx', 'yyy')

# a new connection object called x is created that can be used now...
 
# Describe the current running cluster
x.showCluster()

# start a new cluster based on the latest snapshot
x.startCluster()

# This does not actually delete the cluster for security reasons. 
# It shows the command to do so :)
x.deleteCluster()
 
# show all backup snapshots 
x.SnapshotShow() 

# create a snapshot of the current cluster
snapshotCreate()

# delete a given snapshot
snapshotDelete()

# Download snapshot data in csv format 
x.SnapshotDown('/var/www/html/new_email360_panel/abcx121xxx.csv')

# Execute any query
x.runQuery('select * from school1_oct_sending limit 10')

