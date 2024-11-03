import argparse
import boto3
import json
from botocore.exceptions import ClientError

# Function to create an S3 bucket
def create_s3_bucket(bucket_name, public):
    s3 = boto3.client('s3')

    s3.create_bucket(Bucket=bucket_name)

    # Add a tag indicating the bucket was created via CLI
    s3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={'TagSet': [{'Key': 'CreatedBy', 'Value': 'CLI'}]}
    )

    if public:
        confirm = input("Are you sure you want to create a public bucket? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Bucket creation cancelled.")
            return

        # Add public policy instead of ACL
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(public_policy))
        print(f"S3 Bucket {bucket_name} created with public access.")

    else:
        print(f"S3 Bucket {bucket_name} created with private access.")


# Function to list S3 buckets created via CLI
def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("Buckets created by CLI:")
    for bucket in response['Buckets']:
        try:
            tags = s3.get_bucket_tagging(Bucket=bucket['Name'])
            cli_bucket = any(tag['Key'] == 'CreatedBy' and tag['Value'] == 'CLI' for tag in tags['TagSet'])

            if cli_bucket:
                print(bucket['Name'])

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchTagSet':
                # Skip bucket if it has no tags
                continue
            elif error_code == 'AccessDenied':
                # Skip bucket if access is denied
                print(f"Access denied for bucket: {bucket['Name']}")
                continue
            else:
                raise e  # Raise other errors


# Function to delete an S3 bucket
def delete_s3_bucket(bucket_name):
    s3 = boto3.client('s3')

    # Check if the bucket was created via CLI
    try:
        tags = s3.get_bucket_tagging(Bucket=bucket_name)
        cli_bucket = any(tag['Key'] == 'CreatedBy' and tag['Value'] == 'CLI' for tag in tags['TagSet'])

        if not cli_bucket:
            print(f"Bucket {bucket_name} was not created by the CLI. Deletion not allowed.")
            return

        # Delete all objects in the bucket before deleting the bucket itself
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        print(f"S3 Bucket {bucket_name} deleted successfully.")

    except ClientError as e:
        print(f"Error deleting bucket: {e}")


# Function to upload a file to an S3 bucket
def upload_file_to_s3(bucket_name, file_path):
    s3 = boto3.client('s3')

    # Check if the bucket was created via CLI
    try:
        tags = s3.get_bucket_tagging(Bucket=bucket_name)
        cli_bucket = any(
                tag['Key'] == 'CreatedBy' and tag['Value'] == 'CLI' for tag in
                tags['TagSet'])

        if not cli_bucket:
            print(f"Bucket {bucket_name} was not created by the CLI. Upload not allowed.")
            return

        s3.upload_file(file_path, bucket_name, file_path.split('/')[-1])
        print(f"File {file_path} uploaded to bucket {bucket_name}.")

    except ClientError as e:
        print(f"Error uploading file: {e}")


# Function to delete a file from an S3 bucket
def delete_file_from_s3(bucket_name, file_name):
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"File {file_name} deleted from bucket {bucket_name}.")

    except ClientError as e:
        print(f"Error deleting file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for AWS S3 management")

    subparsers = parser.add_subparsers(dest='command')

    # Create S3 bucket command
    s3_create_parser = subparsers.add_parser('create-s3', help="Create a new S3 bucket")
    s3_create_parser.add_argument('--bucket-name', type=str, required=True, help="S3 bucket name")
    s3_create_parser.add_argument('--public', action='store_true', help="Make bucket public")

    # Upload file to S3 bucket command
    s3_upload_parser = subparsers.add_parser('upload-file', help="Upload a file to an S3 bucket")
    s3_upload_parser.add_argument('--bucket-name', type=str, required=True, help="S3 bucket name")
    s3_upload_parser.add_argument('--file-path', type=str, required=True, help="Path to the file to upload")

    # Delete file from S3 bucket command
    s3_delete_file_parser = subparsers.add_parser('delete-file', help="Delete a file from an S3 bucket")
    s3_delete_file_parser.add_argument('--bucket-name', type=str, required=True, help="S3 bucket name")
    s3_delete_file_parser.add_argument('--file-name', type=str, required=True, help="Name of the file to delete")

    # List S3 buckets command
    s3_list_parser = subparsers.add_parser('list-s3', help="List S3 buckets created by CLI")

    # Delete S3 bucket command
    s3_delete_parser = subparsers.add_parser('delete-s3', help="Delete an S3 bucket")
    s3_delete_parser.add_argument('--bucket-name', type=str, required=True, help="S3 bucket name")

    args = parser.parse_args()

    if args.command == 'create-s3':
        create_s3_bucket(args.bucket_name, args.public)
    elif args.command == 'upload-file':
        upload_file_to_s3(args.bucket_name, args.file_path)
    elif args.command == 'delete-file':
        delete_file_from_s3(args.bucket_name, args.file_name)
    elif args.command == 'list-s3':
        list_s3_buckets()
    elif args.command == 'delete-s3':
        delete_s3_bucket(args.bucket_name)


if __name__ == "__main__":
    main()
