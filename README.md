Project : A Simple Flask-App Deployment On AWS ECS(EC2 Launch type)
This project deploys a containerized microservice application on AWS ECS using the EC2 launch type. Container images are stored in Amazon ECR. A custom VPC provides secure networking, while an Application Load Balancer distributes traffic across ECS tasks. DNS management via Route 53 enables domain-based access to the application

"### First Phase: Containarize the application using Docker

Build the flask-app app.py using the Dockerfile

docker build -t my-app .

Run the docker image for testing

docker run -d -p 5000:5000 --name my-flask-app my-app

Access the app via http://localhost:5000

"### Second Phase : Store Docker Image In Amazon Elastic Container Registry

Create ECR repository

aws ecr create-repository \
  --repository-name your-microservice-name \
  --image-tag-mutability IMMUTABLE \
  --image-scanning-configuration scanOnPush=true

Authenticate Docker to the ECR registry

aws ecr get-login-password --region your-aws-region | \
docker login --username AWS --password-stdin your-aws-account-id.dkr.ecr.your-aws-region.amazonaws.com

change the region
your-aws-account-id.dkr.ecr.your-aws-region.amazonaws.com  -- this is private ECR registy URI change it as per the URI

Tag the docker image

Before pushing image tag the docker build with ECR repository addrress

docker tag your-microservice-name:latest your-aws-account-id.dkr.ecr.your-aws-region.amazonaws.com/your-microservice-name:latest

Push to ECR

Upload the image to ECR

docker push your-aws-account-id.dkr.ecr.your-aws-region.amazonaws.com/your-microservice-name:latest

After pushing check the image in the ECR

"### Third Phase : Deploy and manage using ECR (EC2 Launch type)

Create ECS cluster with EC2 instances

Create VPC ans Subnets(2 - az) before this or use default one
Create ALB Security group with opening allow all traffic inbound traffic for http and https for ALB sg
Create Securit group for EC2 instance allowing ssh and all traffic from ALB security group

Go to AWS Management COnsole -> ECS
Cluster -> Create Cluster
Cluster name : eg., your-ecs-cluster

Infrastructure -> Select EC2
EC2 configuration:
AMI : Amazon Linux 2 (Alredy selected in the console)
Instance type : t2.micro
Desired Capacity : No. of Instance (Select rqiured minimum and maximum)
EC2 instance role: ecsInstanceRole will usually created it need AmazonEc2ContainerServiceforEc2Role pilicy
Networking: Choose/create VPC and select subnet
Securit group fo EC2 instance : Select Security group created for EC2 instance allowing all traffic from ALB security group

Click -> Create

#Create IAM Role for  ECS Task Definition

IAM-> Role -> Create role
trusted entity type : AWS service
Use case : Elastic Container Service -> Elastic Container Service Task -> Next
Permission Policy : Select AmazonECSTaskExecuitionRolePolicy
Role name :ECSTaskRole
Create Role

#Create ECS Task Definition

In ECS go to Task definition -> Create new task definition
Task definition family : give a name
infrastructure requirement
Launch type : EC2
Network mode : bridge
Task role : ECSTaskRole created earlier
Task Execution role : select/create ecsTaskExecutionRole(attached with AmazonECSTaskExecuitionRolePolicy Policy )
Task Size : 0.5 vCPU 0.5 GB (if you give t2.micro can't handle)
Container definition: Add Container

Container name :
Image URI : Copy the URI from ECR
Port Mapping:
 Container port: 5000
 Host Port : 0

Click Add then Create

#Create Application Load balance(ALB)
 EC2 -> Load Balancres -> Create Load Balancer
 Load Balancer type: Application Load balancer

 Basic Configuration
 Load Balance name:
 Scheme: Internet facing
 IP address type: IPv4

 Network mapping:
 VPC : Select same VPC selected for ECS
 Mappings : Select 2 AZ

 Securit group : Already create for ALB at beginning

Listners and routing:

Listner : Protocol HTTP, Port 80
Deafault action : Forwardrd to.. -> Create target group

target type : Instances
target name:
Protocol: HTTP
VPC : Select Same VPC
Next -> Create target group

Back in ALB creation Select newly created target group

#Create ECS Service

 Go back to ECS cluster

 Under Services tab click Create
 
 Deployment Configuration:
 Launch Type:EC2
 Application type: Service
 Task Definition:
  Family : Select the family name
  Revison : Latest

Service name: give a name
Desired tasks :2
Deployment option : Rolling update

Load balancing:
 Load balancer type: Application Load Balancer
 Select created ALB
 Container to load balance: Choose your container
 production listner port : HTTP:80
 Target group name : select created target group

Click Create

Fourth Phase: Verify Deployment

Go to ALB and find DNS name
Access DNS name on browser

CLeanup

To avoid charges, delete aws resources created
ECS Service
ECS Cluster
ALB
Target Group
ECR repo
IAM Roles


