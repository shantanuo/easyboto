class connect:
    '''Managing AWS using boto made easy'''
    def __init__(self, access, secret):
        self.ac = access
        self.se = secret
        self.placement='us-east-1a'
        self.key='dec15a'
        import boto
        self.red_conn = boto.connect_redshift(aws_access_key_id=self.ac, aws_secret_access_key=self.se)
        from boto.s3.connection import OrdinaryCallingFormat
        self.s3_conn = boto.connect_s3(aws_access_key_id=self.ac, aws_secret_access_key=self.se,calling_format=OrdinaryCallingFormat())
        self.buckets = self.s3_conn.get_all_buckets()
        self.ec2_conn = boto.connect_ec2(aws_access_key_id=self.ac, aws_secret_access_key=self.se)
               
    def _showSnap(self):
        self.mydict=self.red_conn.describe_clusters()
        self.my_add=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['Endpoint']['Address']
        self.my_db='mydb'
        self.my_user='root'
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
        import datetime
        mymonth = datetime.datetime.now().strftime("%b").lower()
        myday = datetime.datetime.now().strftime("%d")
        self.myvar = mymonth+myday+'company'
        
        
##### cluster management #####

    def showCluster(self):
        ''' show details of the cluster currently active '''
        self._showSnap()
        from pprint import pprint
        pprint(self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'])
        return self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters']
        
    def startCluster(self):
        '''start a new cluster if no cluster is active'''
        self._showSnap()
        try:
            myidentifier=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['ClusterIdentifier']
            print "cluster already running"
        except IndexError:
            self.red_conn.restore_from_cluster_snapshot('company', mysnapidentifier, availability_zone='us-east-1a')

    def deleteCluster(self):
        self._showSnap()
        self.myidentifier=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['ClusterIdentifier']
        print "this does not actually delete the cluster. Run the following command on your own risk :)\n"
        print "import boto"
        print "conn = boto.connect_redshift(aws_access_key_id='%s', aws_secret_access_key='%s')" % (self.ac, self.se)
        print "conn.delete_cluster('%s', skip_final_cluster_snapshot=False, final_cluster_snapshot_identifier='%s')"%(self.myidentifier, self.myvar)
        
##### Snapshots Management #####

    def showSnapshot(self):
        '''show all snapshots '''
        self._showSnap()
        return self.newdf
        
    def startSnapshot(self):
        self._showSnap()
        myidentifier=self.mydict['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]['ClusterIdentifier']
        self.red_conn.create_cluster_snapshot(self.myvar, myidentifier)        
    
    def deleteSnapshot(self, snapshot_identifier_todelete):
        self.red_conn.delete_cluster_snapshot(snapshot_identifier_todelete)
        
##### Query Management #####

    def runQuery(self, my_query):
        self._showSnap()
        import psycopg2
        pconn = psycopg2.connect("host='"+self.my_add+"' port='5439' dbname='"+self.my_db+"' user='"+self.my_user+"' password='"+self.my_pas+"'")
        cur = pconn.cursor()            
        cur.execute(my_query)
        mydict = cur.fetchall()
        import pandas as pd
        df = pd.DataFrame(mydict)
        print df
        return df

##### s3 Management #####

    def showBucket(self, bucketname=''):
        if bucketname:
            mydict = list()
            mybucket = self.s3_conn.get_bucket(bucketname)
            for key in mybucket.list():
                mykey = mybucket.lookup(key)

                mydict.append((key.name.encode('utf-8'), int(mykey.size)//1000000, 'MB'))
                import pandas as pd
                df = pd.DataFrame(mydict)
                print key.name.encode('utf-8'), int(mykey.size)//1000000, 'MB'
            return df
        else:
            for item in self.buckets:
                print item.name
                
    def uploadFile(self, bucketname, filename='', path=''):
        from boto.s3.key import Key
        k = Key(bucketname)
        key_name =  filename.split('/')[-1]
        import os
        full_key_name = os.path.join(path, key_name)
        mybucket = self.s3_conn.get_bucket(bucketname)
        k = mybucket.new_key(full_key_name)
        k.set_contents_from_filename(filename)
                    
    def downloadFile(self, bucketname, filename):
        mybucket = self.s3_conn.get_bucket(bucketname)
        for b in mybucket:
            if b.name == filename:
                new_file = filename.split('/')[-1]
                b.get_contents_to_filename(new_file)

            
    def deleteFile(self, bucketname, filename):
        mybucket = self.s3_conn.get_bucket(bucketname)
        mybucket.delete_key(filename)
                
    def showBucketLifeCycle(self):
        for item in self.buckets:
            try:
                current = item.get_lifecycle_config()
                print item, current[0].transition
            except:
                pass

##### ec2 Management #####

    def showEc2(self):
        mylist=[]
        info=self.ec2_conn.get_only_instances()
        for reservation in info:
            mylist.append( (reservation , reservation.launch_time, reservation.instance_type, 
                            reservation.image_id,reservation.state, reservation.ip_address))
        import pandas as pd
        col_name=['instance_id', 'launch_time', 'instance_type', 'image_id', 'state', 'ip_address']
        try:
            df = pd.DataFrame(mylist, columns=col_name)
            return df
        except ValueError:
            pass
        

    def startEc2(self, ami, instance_type):
        #aid="image_id='%s', placement='us-east-1a', key_name='%s', instance_type='%s'" % (ami, key_name, instance_type)
        aid = {'image_id': ami, 'key_name': self.key, 'instance_type': instance_type, 'placement': self.placement}
        daid=dict(aid)
        rid=self.ec2_conn.run_instances(**daid)

        import time
        time.sleep(20)
        iid=self.ec2_conn.get_all_instances(filters={'reservation-id': rid.id})[0].instances[0]
        #address = self.ec2_conn.allocate_address()
        #self.ec2_conn.associate_address(iid.id, address.public_ip)
        print 'ssh -i ' + self.key+ '.pem ec2-user@'+str(iid.public_dns_name)



    def deleteEc2(self,  instance_id_to_delete, mylist=None):
        mylist=[]
        mylist.append(instance_id_to_delete)
        print mylist
        self.ec2_conn.terminate_instances(instance_ids=mylist)
 
    def deleteAllEc2(self):
        mylistDel=[]
        info=self.ec2_conn.get_only_instances()
        for reservation in info:
            mylistDel.append(reservation.id)
              
        print "this does not actually delete the ec2 instances. Run the following command on your own risk :)\n"
        print "import boto"
        print "ec2_conn = boto.connect_ec2(aws_access_key_id='%s', aws_secret_access_key='%s')" % (self.ac, self.se)
        print "ec2_conn.terminate_instances(instance_ids=%s)" % (mylistDel)      
        
                
    def showImages(self):
        mylist=[]
        i_list=self.ec2_conn.get_all_images(owners=['self'])
        for i in i_list:
            mylist.append((i.id, i.is_public, i.name, i.description,i.region))
        import pandas as pd
        col_name=['image_id', 'is_public', 'name', 'description', 'region']
        df = pd.DataFrame(mylist, columns=col_name)
        return df
