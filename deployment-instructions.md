# CloudFormation Deployment Instructions

## Quick Deployment

### 1. Deploy the Stack
```bash
aws cloudformation create-stack \
  --stack-name order-management-system \
  --template-body file://cloudformation-template.yaml \
  --parameters ParameterKey=BucketName,ParameterValue=my-order-system \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

### 2. Check Deployment Status
```bash
aws cloudformation describe-stacks \
  --stack-name order-management-system \
  --query 'Stacks[0].StackStatus'
```

### 3. Get Output URLs
```bash
aws cloudformation describe-stacks \
  --stack-name order-management-system \
  --query 'Stacks[0].Outputs'
```

### 4. Upload Frontend Files
```bash
# Get bucket name from stack outputs
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name order-management-system \
  --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
  --output text)

# Upload index.html
aws s3 cp frontend/index.html s3://$BUCKET_NAME/ --content-type "text/html"
```

### 5. Update API URL in Frontend
```bash
# Get API Gateway URL
API_URL=$(aws cloudformation describe-stacks \
  --stack-name order-management-system \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayURL`].OutputValue' \
  --output text)

# Update index.html with the correct API URL
sed -i "s|const API_BASE = '.*'|const API_BASE = '$API_URL'|" frontend/index.html

# Re-upload updated file
aws s3 cp frontend/index.html s3://$BUCKET_NAME/ --content-type "text/html"
```

## Manual Deployment via AWS Console

### 1. CloudFormation Console
1. Go to AWS CloudFormation Console
2. Click "Create stack" → "With new resources"
3. Upload `cloudformation-template.yaml`
4. Enter stack name: `order-management-system`
5. Set parameters:
   - BucketName: `my-order-system` (must be globally unique)
   - LambdaFunctionName: `OrderManagementAPI`
6. Check "I acknowledge that AWS CloudFormation might create IAM resources"
7. Click "Create stack"

### 2. Upload Frontend
1. Go to S3 Console
2. Find your bucket (name will include account ID)
3. Upload `frontend/index.html`
4. Set Content-Type to `text/html`

### 3. Update API URL
1. Copy API Gateway URL from CloudFormation Outputs
2. Edit `frontend/index.html`
3. Update `const API_BASE = 'YOUR_API_URL'`
4. Re-upload the file

## Stack Resources Created

- **S3 Bucket**: Static website hosting with public read policy
- **Lambda Function**: Order management API with sample data
- **API Gateway**: REST API with CORS enabled
- **IAM Role**: Lambda execution role with basic permissions

## Cleanup

```bash
# Delete the stack (this removes all resources)
aws cloudformation delete-stack --stack-name order-management-system

# Verify deletion
aws cloudformation describe-stacks --stack-name order-management-system
```

## Troubleshooting

### Common Issues

1. **Bucket name already exists**: Change the BucketName parameter to something unique
2. **Lambda function not responding**: Check CloudWatch logs for errors
3. **CORS errors**: Verify API Gateway CORS configuration in the template
4. **403 errors**: Check S3 bucket policy allows public read access

### Useful Commands

```bash
# Check stack events
aws cloudformation describe-stack-events --stack-name order-management-system

# View Lambda logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/OrderManagementAPI

# Test API endpoint
curl https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/orders
```