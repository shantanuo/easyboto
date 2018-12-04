class connect:
    '''Managing AWS using boto made easy'''
    def __init__(self, access=None, secret=None):
        self.ac = access
        self.se = secret
        self.placement='us-east-1b'
        self.key='dec15a'
        self.myaddress='18.208.241.12'
        self.MAX_SPOT_BID='1.0' 
        #self.myaddress=None

        import boto
        self.ec2_conn = boto.connect_ec2(aws_access_key_id=self.ac, aws_secret_access_key=self.se)
        self.mytest = b"""
        #!/bin/bash -ex

        yum install -y docker mysql git python-pip
        sudo amazon-linux-extras install -y docker
        pip install aws-ec2-assign-elastic-ip
        aws-ec2-assign-elastic-ip --access-key AKIAIY6BQUW4X665VS6A --secret-key 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  --valid-ips 18.208.241.12
        service docker start
        docker run -d -p 8888:8888 -v /tmp:/tmp continuumio/miniconda3 /bin/bash -c "/opt/conda/bin/conda install jupyter -y && cd /tmp/ && /opt/conda/bin/jupyter notebook --NotebookApp.token='india' --notebook-dir=/tmp --ip='0.0.0.0' --port=8888 --no-browser --allow-root"

        """
       
        self.bug=b"""
        from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping
        self.dev_sda1 = BlockDeviceType()
        self.bdm = BlockDeviceMapping()
        self.dev_sda1.size = 100
        self.bdm['/dev/xvda'] = self.dev_sda1
        #reservation = image.run(..., , ...)
        """

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
        
    def startEc2Spot(self, ami, instance_type):
        #aid="image_id='%s', placement='us-east-1a', key_name='%s', instance_type='%s'" % (ami, key_name, instance_type)

        aid = {'user_data': self.mytest , 'image_id': ami, 'key_name': self.key, 'instance_type': instance_type, 'placement': self.placement, 'price': self.MAX_SPOT_BID}
        daid=dict(aid)
        rid=self.ec2_conn.request_spot_instances(**daid)
        import time
        time.sleep(300)
        job_sir_id = rid[0].id # spot instance request = sir, job_ is the relevant aws item for this job
        reqs = self.ec2_conn.get_all_spot_instance_requests()
        for sir in reqs:
            if sir.id == job_sir_id:
                job_instance_id = sir.instance_id
                print ("job instance id: " + str(job_instance_id))

                if self.myaddress:
                    self.ec2_conn.associate_address(job_instance_id, self.myaddress)
                    print ('ssh -i ' + self.key+ '.pem ec2-user@'+self.myaddress)
                else:
                    address = self.ec2_conn.allocate_address()
                    self.ec2_conn.associate_address(job_instance_id, address.public_ip)
                    print ('ssh -i ' + self.key+ '.pem ec2-user@'+str(address.public_ip))

    def startEc2(self, ami, instance_type):
        #aid="image_id='%s', placement='us-east-1a', key_name='%s', instance_type='%s'" % (ami, key_name, instance_type)
        aid = {'user_data': self.mytest , 'image_id': ami, 'key_name': self.key, 'instance_type': instance_type, 'placement': self.placement}
        daid=dict(aid)
        rid=self.ec2_conn.run_instances(**daid)

        import time
        time.sleep(120)
        iid=self.ec2_conn.get_all_instances(filters={'reservation-id': rid.id})[0].instances[0]
        #address = self.ec2_conn.allocate_address()
        #self.ec2_conn.associate_address(iid.id, address.public_ip)
        if self.myaddress:
            self.ec2_conn.associate_address(iid.id, self.myaddress)
            print ('ssh -i ' + self.key+ '.pem ec2-user@'+self.myaddress)
        else:
            address = self.ec2_conn.allocate_address()
            self.ec2_conn.associate_address(iid.id, address.public_ip)
            print ('ssh -i ' + self.key+ '.pem ec2-user@'+str(address.public_ip))


    def deleteEc2(self,  instance_id_to_delete, mylist=None):
        mylist=[]
        mylist.append(instance_id_to_delete)
        print (mylist)
        self.ec2_conn.terminate_instances(instance_ids=mylist)
 
    def deleteAllEc2(self):
        mylistDel=[]
        info=self.ec2_conn.get_only_instances()
        for reservation in info:
            mylistDel.append(reservation.id)
              
        print ("this does not actually delete the ec2 instances. Run the following command on your own risk :)\n")
        print ("import boto")
        print ("ec2_conn = boto.connect_ec2(aws_access_key_id='%s', aws_secret_access_key='%s')" % (self.ac, self.se))
        print ("ec2_conn.terminate_instances(instance_ids=%s)" % (mylistDel))      
        
                
    def showImages(self):
        mylist=[]
        i_list=self.ec2_conn.get_all_images(owners=['self'])
        for i in i_list:
            mylist.append((i.id, i.is_public, i.name, i.description,i.region))
        import pandas as pd
        col_name=['image_id', 'is_public', 'name', 'description', 'region']
        df = pd.DataFrame(mylist, columns=col_name)
        return df
    
    """
#x = connect('xxx', 'xxx')
#x.startEc2Spot('ami-0a721ca7c0ae5cd2c', 't2.small')
#x.showEc2()
#x.deleteAllEc2()
#x.showImages()  
    """