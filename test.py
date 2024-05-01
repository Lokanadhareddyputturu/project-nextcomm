import boto3
import pymysql
import os

# AWS credentials and configuration
bucket_name = 'your-s3-bucket-name'
region = 'your-aws-region'
access_key_id = 'your-access-key-id'
secret_access_key = 'your-secret-access-key'

# MySQL database connection details
host = 'your-rds-endpoint'
user = 'your-rds-username'
password = 'your-rds-password'
database = 'your-rds-database-name'

# Connect to MySQL database
conn = pymysql.connect(host=host, user=user, password=password, database=database)

# Upload employee photo to S3
def upload_to_s3(file_path, file_name):
    s3 = boto3.client('s3', region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    s3.upload_file(file_path, bucket_name, file_name)
    print("Uploaded file URL:", f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}")

# Add employee details to MySQL database
def add_employee_details(name, age, location, photo_file_name):
    with conn.cursor() as cursor:
        sql = "INSERT INTO employees (name, age, location, photo) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, age, location, photo_file_name))
        conn.commit()
        print("Employee details added to database successfully")

# Example usage: Add employee details and upload photo
name = "John Doe"
age = 30
location = "New York"
photo_file_path = "/path/to/employee-photo.jpg"
photo_file_name = "john_doe_photo.jpg"

# Upload photo to S3
upload_to_s3(photo_file_path, photo_file_name)

# Add employee details to database
add_employee_details(name, age, location, photo_file_name)

# Close MySQL connection
conn.close()