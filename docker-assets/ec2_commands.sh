sudo su
apt update
apt install -y awscli docker.io
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 111263457661.dkr.ecr.us-east-1.amazonaws.com
docker pull 111263457661.dkr.ecr.us-east-1.amazonaws.com/demo:latest
docker run --rm -p 100:100 -p 5000:5000 -p 5432:5432 111263457661.dkr.ecr.us-east-1.amazonaws.com/demo:latest