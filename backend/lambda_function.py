import json
import boto3
from datetime import datetime
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('BookOrders')

# Mock data store with sample orders
mock_orders = [
    {
        'order_id': 'sample-001',
        'customer_name': 'John Doe',
        'customer_email': 'john.doe@email.com',
        'book_title': 'Python Programming Fundamentals',
        'book_isbn': '978-0134444321',
        'quantity': 2,
        'price': '45.99',
        'total_amount': '91.98',
        'order_date': '2025-01-10T14:30:00.000000',
        'status': 'pending'
    },
    {
        'order_id': 'sample-002',
        'customer_name': 'Sarah Wilson',
        'customer_email': 'sarah.wilson@email.com',
        'book_title': 'AWS Cloud Architecture',
        'book_isbn': '978-1617294440',
        'quantity': 1,
        'price': '59.99',
        'total_amount': '59.99',
        'order_date': '2025-01-10T15:45:00.000000',
        'status': 'shipped'
    },
    {
        'order_id': 'sample-003',
        'customer_name': 'Mike Johnson',
        'customer_email': 'mike.johnson@email.com',
        'book_title': 'JavaScript: The Good Parts',
        'book_isbn': '978-0596517748',
        'quantity': 3,
        'price': '29.99',
        'total_amount': '89.97',
        'order_date': '2025-01-10T16:20:00.000000',
        'status': 'cancelled'
    }
]

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        if method == 'GET' and path == '/orders':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(mock_orders)
            }
        
        elif method == 'POST' and path == '/orders':
            data = json.loads(event['body'])
            order_id = str(uuid.uuid4())
            
            order = {
                'order_id': order_id,
                'customer_name': data['customer_name'],
                'customer_email': data['customer_email'],
                'book_title': data['book_title'],
                'book_isbn': data['book_isbn'],
                'quantity': data['quantity'],
                'price': str(data['price']),
                'total_amount': str(data['quantity'] * data['price']),
                'order_date': datetime.now().isoformat(),
                'status': 'pending'
            }
            
            mock_orders.append(order)
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps(order)
            }
        
        elif method == 'PUT' and '/orders/' in path:
            order_id = path.split('/')[-1]
            data = json.loads(event['body'])
            
            for order in mock_orders:
                if order['order_id'] == order_id:
                    if 'status' in data:
                        order['status'] = data['status']
                    if 'quantity' in data:
                        order['quantity'] = data['quantity']
                    if 'price' in data:
                        order['price'] = str(data['price'])
                    if 'total_amount' in data:
                        order['total_amount'] = str(data['total_amount'])
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'message': 'Order updated successfully'})
                    }
            
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Order not found'})
            }
        
        elif method == 'DELETE' and '/orders/' in path:
            order_id = path.split('/')[-1]
            
            for order in mock_orders:
                if order['order_id'] == order_id:
                    order['status'] = 'cancelled'
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'message': 'Order cancelled successfully'})
                    }
            
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Order not found'})
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }