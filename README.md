# Assignment4


Below is a short description of different files:
1. .github/workflows/workflow.yaml : This is a github workflow file. This file runs when a push is happened on dev branch or pull request on main branch.
2. deploy_scripts/stack_deploy.py : This file creates a cloudformation stack using templates/rds-deploy.yaml file. If the stack is already present then it will update the stack(if any updates are there to perform).
3. templates/rds-deploy.yaml : Cloudformation template file. This creates 1 RDS, 2 Security groups, 2 lambda functions, IAM Role, S3 Bucket and Api gateway.
4. main.py : This file orchestrate everything. This file contains cloudformation template parameter values and other variables. This file will call stack_deploy.py for creating or updating the stack. Then adds api gateway endpoint in index.html file, uploads this file in hosting S3 bucket and then trigger the rds-initial lambda which will create and insert data in the tables.
5. upload.sh : This file zips the lambda function code and upload it in code bucket.
6. retrive_vpc_info.py : This file fetch the vpc id and related subnets.
7. upload_file : This will add the API Gateway endpoint in index.html file and upload it to S3 bucket.
8. webpage/index.html : Static webpage which will be hosted on S3.
9. lambdas/lambda-function.py : Lambda function code which will fetch the sum of transactions made by a customer based on customer id.
10. lambdas/rds-initial.py : Lambda function code which will create tables in database and insert some data in it.
