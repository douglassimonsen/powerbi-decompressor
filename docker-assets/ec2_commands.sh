{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "cloudtrail:LookupEvents"           
            ],
            "Resource": "*"
        }
    ]
}

#! /bin/sh
apt update

apt install -y awscli docker.io

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 111263457661.dkr.ecr.us-east-1.amazonaws.com

docker pull 111263457661.dkr.ecr.us-east-1.amazonaws.com/powerbi-parser2-dockerrepo-4gugvr04nlft:latest
docker run --rm -p 100:100 -p 5000:5000 -p 5432:5432 111263457661.dkr.ecr.us-east-1.amazonaws.com/powerbi-parser2-dockerrepo-4gugvr04nlft:latest