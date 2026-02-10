
![logo](https://github.com/Abhi956967/student_performance_report/blob/main/student%20performance.png)

## End to End MAchine Learning Project

1. Docker Build checked
2. Github Workflow
3. Iam User In AWS

## Docker Setup In EC2 commands to be Executed

# optional

sudo apt-get update -y

sudo apt-get upgrade

# required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

## Configure EC2 as self-hosted runner:
Register a self-hosted runner in this repo and ensure it stays online during deployments.

## Fix "no space left on device" during deployment
If the self-hosted runner runs out of disk space while pulling the image, prune old Docker
images/containers/volumes before the pull step (the workflow now does this automatically):

```
docker system prune -af --volumes
```
## Setup github secrets:
Make sure the AWS region matches your ECR registry's region.

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = ap-south-1

AWS_ECR_LOGIN_URI = 566373416292.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = student_performance_report
