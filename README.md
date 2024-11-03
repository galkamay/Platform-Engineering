
# AWS Management CLI Tool

This CLI tool allows you to manage AWS resources: EC2 instances, S3 buckets, and Route 53 DNS records. It provides an easy way to create, list, and manage these resources directly from the command line.

## Prerequisites
- Python 3.x
- AWS credentials configured with `aws configure`
- Necessary permissions for EC2, S3, and Route53 resources.

## Installation
Clone the repository and install any required packages:
```bash
git clone (https://github.com/galkamay/Platform-Engineering.git)
pip install -r requirements.txt
```

## Usage

### EC2 Management
#### Create an Instance
```bash
python main.py --resource ec2 --action create --ami <ami-id> --instance-type <instance-type> --name <instance-name> [--public-ip]
```

#### List Instances
```bash
python main.py --resource ec2 --action list
```

#### Manage Instance (start, stop, terminate)
```bash
python main.py --resource ec2 --action manage --instance-id <instance-id> --action <start|stop|terminate>
```

### S3 Management
#### Create a Bucket
```bash
python main.py --resource s3 --action create --bucket-name <bucket-name> [--public]
```

#### Upload a File
```bash
python main.py --resource s3 --action upload --bucket-name <bucket-name> --file-path <file-path>
```

#### List Buckets
```bash
python main.py --resource s3 --action list
```

#### Delete a File from a Bucket
```bash
python main.py --resource s3 --action delete-file --bucket-name <bucket-name> --file-name <file-name>
```

#### Delete a Bucket
```bash
python main.py --resource s3 --action delete --bucket-name <bucket-name>
```

### Route 53 Management
#### Create a Hosted Zone
```bash
python main.py --resource route53 --action create --domain <domain-name>
```

#### Add a DNS Record
```bash
python main.py --resource route53 --action add-record --zone-id <zone-id> --record-name <record-name> --record-value <record-value>
```

#### Update a DNS Record
```bash
python main.py --resource route53 --action update-record --zone-id <zone-id> --record-name <record-name> --record-value <record-value>
```

#### Delete a DNS Record
```bash
python main.py --resource route53 --action delete-record --zone-id <zone-id> --record-name <record-name> --record-value <record-value>
```

## Dependencies
This project relies on the following dependencies:
- `boto3`: AWS SDK for Python
- `argparse`: Argument parsing for the command-line interface

## Notes
- Ensure you have appropriate permissions in AWS for the CLI commands to execute successfully.
- Handle sensitive AWS information (like `instance_id`, `zone_id`) securely.
  
## License
This project is licensed under the MIT License.
