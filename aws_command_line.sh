#!/bin/sh
cat > userdata.sh << "here_doc"
#!/bin/bash -ex
yum install -y docker mysql git python-pip
sudo amazon-linux-extras install -y docker
pip install aws-ec2-assign-elastic-ip
aws-ec2-assign-elastic-ip --access-key {}, --secret-key {}  --valid-ips {}
service docker start
docker run -d -p 8887:8888 -v /tmp:/tmp shantanuo/notebook
here_doc


cat > specification.json << "here_doc"
    {
      "ImageId": "ami-009d6802948d06e52",
      "InstanceType": "c4.large",
      "SubnetId": "subnet-8bb550d1",
      "KeyName": "dec15a",
      "BlockDeviceMappings": [
        {
          "DeviceName": "/dev/xvda",
          "Ebs": {
            "DeleteOnTermination": true,
            "VolumeType": "standard",
            "VolumeSize": 500
          }
        }
      ],

here_doc

echo '"UserData": "'`base64 -w 0 userdata.sh`'"'>> specification.json

cat >> specification.json << "here_doc"
    }

here_doc
 
aws ec2 request-spot-instances --spot-price "1.050" --instance-count 1 --type "one-time" --launch-specification file://specification.json
