class connect:
    def __init__(self, access=None, secret=None):
        self.region='ap-south-1'
        self.ac = access
        self.se = secret
        self.myaddress='52.14.29.127'
        self.key='dec15a'
        self.MAX_SPOT_BID='1.0' 
        self.security_groups = ['default']

        import time
        import boto
        import boto.ec2
        from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping
        self.ec2_conn = boto.ec2.connect_to_region(self.region, aws_access_key_id=self.ac, aws_secret_access_key=self.se)

        shell_script = """
        #!/bin/bash -ex
        yum install -y docker mysql git python-pip
        sudo amazon-linux-extras install -y docker
        pip install aws-ec2-assign-elastic-ip
        aws-ec2-assign-elastic-ip --access-key {}, --secret-key {}  --valid-ips {}
        service docker start
        docker run -d -p 8887:8888 -v /tmp:/tmp shantanuo/notebook
        
        """
        self.my_user_data=shell_script.format(self.ac,self.se, self.myaddress).encode()
    
        self.dev_sda1 = BlockDeviceType()
        self.bdm = BlockDeviceMapping()
        self.dev_sda1.size = 500
        self.bdm['/dev/xvda'] = self.dev_sda1

    def startEc2Spot(self, ami, instance_type):
        aid = {'image_id': ami, 'instance_type': instance_type, 'user_data': self.my_user_data , 'key_name': self.key, 
              'security_groups': self.security_groups, 'block_device_map' : self.bdm, 'price': self.MAX_SPOT_BID}
        daid=dict(aid)
        rid=self.ec2_conn.request_spot_instances(**daid)

        time.sleep(180)
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
        aid = { 'image_id': ami, 'instance_type': instance_type, 'user_data': self.my_user_data ,'key_name': self.key, 
                 'security_groups': self.security_groups, 'block_device_map' : self.bdm}
        daid=dict(aid)
        rid=self.ec2_conn.run_instances(**daid)

        time.sleep(120)
        iid=self.ec2_conn.get_all_instances(filters={'reservation-id': rid.id})[0].instances[0]
        if self.myaddress:
            self.ec2_conn.associate_address(iid.id, self.myaddress)
            print ('ssh -i ' + self.key+ '.pem ec2-user@'+self.myaddress)
        else:
            address = self.ec2_conn.allocate_address()
            self.ec2_conn.associate_address(iid.id, address.public_ip)
            print ('ssh -i ' + self.key+ '.pem ec2-user@'+str(address.public_ip))
                   
    def showEc2(self):
        mylist=[]
        info=self.ec2_conn.get_only_instances()
        for reservation in info:
            mylist.append( (reservation.kernel,
reservation.placement_tenancy,
reservation.placement_group,
reservation.placement,
reservation.image_id,
reservation.launch_time,
reservation.instance_type,
reservation.key_name,
reservation.previous_state_code,
reservation.previous_state,
reservation.state_code,
reservation.state,
reservation.private_dns_name,
reservation.public_dns_name,
reservation.groups,
reservation.id,
reservation.private_ip_address,
reservation.vpc_id,
reservation.subnet_id,
reservation.spot_instance_request_id,
reservation.monitoring_state,
reservation.monitored,
reservation.ami_launch_index,
reservation.product_codes,
reservation.virtualization_type,
reservation.hypervisor,
reservation.architecture,
reservation.ramdisk,
reservation.instance_profile,
reservation.ebs_optimized,
reservation.interfaces,
reservation.state_reason,
reservation.block_device_mapping,
reservation.root_device_type,
reservation.root_device_name,
reservation.platform,
reservation.ip_address))
        import pandas as pd
        mycolumns="""kernel 
placement_tenancy 
placement_group 
placement 
image_id 
launch_time 
instance_type 
key_name 
previous_state_code 
previous_state 
state_code 
state 
private_dns_name 
public_dns_name 
groups 
id 
private_ip_address 
vpc_id 
subnet_id 
spot_instance_request_id 
monitoring_state 
monitored 
ami_launch_index 
product_codes 
virtualization_type 
hypervisor 
architecture 
ramdisk 
instance_profile 
ebs_optimized 
interfaces 
state_reason 
block_device_mapping 
root_device_type 
root_device_name 
platform 
ip_address"""

        col_name=mycolumns.split()
        try:
            df = pd.DataFrame(mylist, columns=col_name)
            return df
        except ValueError:
            pass
            
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
#x.startEc2Spot('ami-009d6802948d06e52', 'm3.large')
#x.showEc2()
#x.deleteAllEc2()
#x.showImages()  
    """
    
