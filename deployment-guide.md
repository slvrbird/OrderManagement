# Deployment Guide

## Quick Setup Commands

### 1. Create Lambda Function
```bash
# Create deployment package
cd backend
zip lambda-deployment.zip lambda_function.py

# Create Lambda function (replace role ARN with your execution role)
aws lambda create-function \
  --function-name OrderManagementAPI \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda-deployment.zip
```

### 2. Create API Gateway
```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api --name OrderManagementAPI --query 'id' --output text)

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

# Create /orders resource
ORDERS_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part orders --query 'id' --output text)

# Create methods
aws apigateway put-method --rest-api-id $API_ID --resource-id $ORDERS_ID --http-method GET --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $ORDERS_ID --http-method POST --authorization-type NONE

# Create {id} resource
ID_RESOURCE=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $ORDERS_ID --path-part "{id}" --query 'id' --output text)

aws apigateway put-method --rest-api-id $API_ID --resource-id $ID_RESOURCE --http-method PUT --authorization-type NONE
aws apigateway put-method --rest-api-id $API_ID --resource-id $ID_RESOURCE --http-method DELETE --authorization-type NONE

# Deploy API
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod
```

### 3. Create S3 Website
```bash
# Create bucket (replace with unique name)
aws s3 mb s3://your-order-mgmt-bucket

# Enable website hosting
aws s3 website s3://your-order-mgmt-bucket --index-document index.html

# Upload frontend
aws s3 cp frontend/index.html s3://your-order-mgmt-bucket/ --content-type "text/html"

# Set public read policy
aws s3api put-bucket-policy --bucket your-order-mgmt-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::your-order-mgmt-bucket/*"
  }]
}'
```

## Manual Setup via AWS Console

### Lambda Function
1. Go to AWS Lambda Console
2. Create function → Author from scratch
3. Function name: `OrderManagementAPI`
4. Runtime: Python 3.9
5. Upload `backend/lambda_function.py`

### API Gateway
1. Go to API Gateway Console
2. Create API → REST API
3. Create resources: `/orders` and `/orders/{id}`
4. Add methods: GET, POST, PUT, DELETE
5. Enable CORS on all methods
6. Deploy to `prod` stage

### S3 Website
1. Go to S3 Console
2. Create bucket with unique name
3. Enable static website hosting
4. Upload `frontend/index.html`
5. Set bucket policy for public read access
6. Update API_BASE URL in HTML file