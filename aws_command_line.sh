# vi specification.json
    {
      "ImageId": "ami-009d6802948d06e52",
      "InstanceType": "c4.large",
      "SubnetId": "subnet-8bb550d1",
      "KeyName": "dec12a",
      "BlockDeviceMappings": [
        {
          "DeviceName": "/dev/xvda",
          "Ebs": {
            "DeleteOnTermination": true,
            "VolumeType": "standard",
            "VolumeSize": 500
          }
        }
      ]
    }


# aws ec2 request-spot-instances --spot-price "1.050" --instance-count 1 --type "one-time" --launch-specification file://specification.json
# "UserData":"`base64 -w 0 userdata.sh`",
# userdata should be replaced by the actual output of base64 command
