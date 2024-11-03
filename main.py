import argparse
from aws_resource_tool import create_ec2_instance, list_ec2_instances, manage_instance
from s3_resource_tool import create_s3_bucket, upload_file_to_s3, delete_file_from_s3, list_s3_buckets, delete_s3_bucket
from route53_tool import create_route53_zone, add_dns_record, update_dns_record, delete_dns_record

def parse_arguments():
    parser = argparse.ArgumentParser(description="AWS Management CLI Tool")

    # General resource and action arguments
    parser.add_argument("--resource", type=str, required=True, choices=["ec2", "s3", "route53"],
                        help="Resource to manage: ec2, s3, or route53", metavar="")
    parser.add_argument("--action", type=str, required=True,
                        help="Action to perform: create, upload, delete, list, manage, add-record, update-record, or delete-record", metavar="")

    # EC2 specific arguments
    parser.add_argument("--ami", type=str, help="AMI ID for EC2 instance creation", metavar="")
    parser.add_argument("--instance-type", type=str, choices=["t3.nano", "t4g.nano"], help="Type of EC2 instance", metavar="")
    parser.add_argument("--name", type=str, help="Name for the instance or bucket", metavar="")
    parser.add_argument("--instance-id", type=str, help="ID of the EC2 instance", metavar="")
    parser.add_argument("--public-ip", action="store_true", help="Assign public IP for EC2 instance")

    # S3 specific arguments
    parser.add_argument("--bucket-name", type=str, help="S3 bucket name", metavar="")
    parser.add_argument("--public", action="store_true", help="Make S3 bucket public")
    parser.add_argument("--file-path", type=str, help="Path to file for S3 upload", metavar="")
    parser.add_argument("--file-name", type=str, help="File name for deletion in S3 bucket", metavar="")

    # Route 53 specific arguments
    parser.add_argument("--zone-id", type=str, help="ID of the Route53 hosted zone", metavar="")
    parser.add_argument("--domain", type=str, help="Domain name for Route53 hosted zone", metavar="")
    parser.add_argument("--record-name", type=str, help="DNS record name", metavar="")
    parser.add_argument("--record-value", type=str, help="DNS record value", metavar="")

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.resource == "ec2":
        if args.action == "create":
            create_ec2_instance(args.ami, args.instance_type, args.name, args.public_ip)
        elif args.action == "list":
            list_ec2_instances()
        elif args.action == "manage" and args.instance_id:
            manage_instance(args.instance_id, args.action)
        else:
            print("Invalid EC2 action or missing parameters.")

    elif args.resource == "s3":
        if args.action == "create" and args.bucket_name:
            create_s3_bucket(args.bucket_name, args.public)
        elif args.action == "upload" and args.bucket_name and args.file_path:
            upload_file_to_s3(args.bucket_name, args.file_path)
        elif args.action == "delete-file" and args.bucket_name and args.file_name:
            delete_file_from_s3(args.bucket_name, args.file_name)
        elif args.action == "list":
            list_s3_buckets()
        elif args.action == "delete" and args.bucket_name:
            delete_s3_bucket(args.bucket_name)
        else:
            print("Invalid S3 action or missing parameters.")

    elif args.resource == "route53":
        if args.action == "create" and args.domain:
            create_route53_zone(args.domain)
        elif args.action == "add-record" and args.zone_id and args.record_name and args.record_value:
            add_dns_record(args.zone_id, args.record_name, args.record_value)
        elif args.action == "update-record" and args.zone_id and args.record_name and args.record_value:
            update_dns_record(args.zone_id, args.record_name, args.record_value)
        elif args.action == "delete-record" and args.zone_id and args.record_name and args.record_value:
            delete_dns_record(args.zone_id, args.record_name, args.record_value)
        else:
            print("Invalid Route53 action or missing parameters.")

if __name__ == "__main__":
    main()
