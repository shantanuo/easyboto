class myboto:
    def __init__(self, access, secret):
        self.ac = access
        self.se = secret
        import boto
        self.red_conn = boto.connect_redshift(aws_access_key_id=self.ac, aws_secret_access_key=self.se)
        
    def _showSnap(self):
        self.mydict=self.red_conn.describe_clusters()
        self.my_add=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['Endpoint']['Address']
        self.response = self.red_conn.describe_cluster_snapshots()
        self.snapshots = self.response['DescribeClusterSnapshotsResponse']['DescribeClusterSnapshotsResult']['Snapshots']
        self.snapshots.sort(key=lambda d: d['SnapshotCreateTime'])
        self.mysnapidentifier = self.snapshots[-1]['SnapshotIdentifier']
        import pandas as pd
        self.df=pd.DataFrame(self.snapshots)
        self.df['ClusterCreateDate'] = pd.to_datetime(self.df['ClusterCreateTime'],unit='s')
        self.df['SnapshotCreateDate'] = pd.to_datetime(self.df['SnapshotCreateTime'],unit='s')
        self.df['BackupSize'] = self.df['TotalBackupSizeInMegaBytes']
        self.df['IncrementSize'] = self.df['ActualIncrementalBackupSizeInMegaBytes']
        self.newdf=self.df[['SnapshotIdentifier','SnapshotCreateDate', 'BackupSize', 'ClusterIdentifier', 'ClusterCreateDate', 'IncrementSize', 'SnapshotType'] ]

##### cluster management #####

    def showCluster(self):
        ''' show details of the cluster currently active '''
        self._showSnap()
        from pprint import pprint
        pprint(self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'])
        
    def startCluster(self):
        '''start a new cluster if no cluster is active'''
        self._showSnap()
        try:
            myidentifier=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['ClusterIdentifier']
            print "cluster already running"
        except IndexError:
            self.red_conn.restore_from_cluster_snapshot('company', mysnapidentifier, availability_zone='us-east-1a')

    def deleteCluster(self):
        import datetime
        mymonth = datetime.datetime.now().strftime("%b").lower()
        myday = datetime.datetime.now().strftime("%d")
        self.myvar = mymonth+myday+'company-new'
        mydict=self.red_conn.describe_clusters()
        self.myidentifier=mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['ClusterIdentifier']
        print "this does not actually delete the cluster. Run the following command on your own risk :)\n"
        print "conn.delete_cluster(%s, skip_final_cluster_snapshot=False, final_cluster_snapshot_identifier=%s)"%(self.myidentifier, self.myvar)
        
##### Snapshots Management #####

    def snapshotShow(self):
        '''show all snapshots '''
        self._showSnap()
        print self.newdf

    def snapshotCreate(self):
        pass
        # red_conn.create_cluster_snapshot(self, snapshot_identifier, cluster_identifier)
        
    def snapshotDelete(self):
        pass

    def snapshotDown(self, path='/var/www/html/new_email360_panel/abcx.csv'):
        '''copy snapshot data to csv that can be downloaded from the path'''
        self._showSnap()
        self.newdf.to_csv(path)
       
        
##### Query Management #####

    def runQuery(self, my_query):
        self._showSnap()
        import psycopg2
        pconn = psycopg2.connect("host='"+self.my_add+"' port='5439' dbname='mydb' user='root' password='Root1234'")
        cur = pconn.cursor()            
        cur.execute(my_query)
        mydict = cur.fetchall()
        import pandas as pd
        df = pd.DataFrame(mydict)
        print df
        
