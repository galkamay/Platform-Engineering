import argparse
import boto3
from botocore.exceptions import ClientError

# Function to create a Hosted Zone
def create_route53_zone(domain_name):
    route53 = boto3.client('route53')

    response = route53.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(hash(domain_name)),
        HostedZoneConfig={
            'Comment': 'Created by CLI',
            'PrivateZone': False  # Option for a public zone
        }
    )

    zone_id = response['HostedZone']['Id']
    print(f"Hosted zone created for domain {domain_name} with ID: {zone_id}")
    return zone_id

# Function to add a DNS record
def add_dns_record(zone_id, record_name, record_value, ttl=300):
    route53 = boto3.client('route53')

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }
    )
    print(f"DNS record {record_name} created with value {record_value}.")

# Function to update a DNS record
def update_dns_record(zone_id, record_name, record_value, ttl=300):
    route53 = boto3.client('route53')

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }
    )
    print(f"DNS record {record_name} updated to value {record_value}.")

# Function to delete a DNS record
def delete_dns_record(zone_id, record_name, record_value, ttl=300):
    route53 = boto3.client('route53')

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }
    )
    print(f"DNS record {record_name} deleted.")

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for AWS Route53 management")

    subparsers = parser.add_subparsers(dest='command')

    # Create Route53 hosted zone command
    route53_create_parser = subparsers.add_parser('create-zone', help="Create a new Route53 hosted zone")
    route53_create_parser.add_argument('--domain', type=str, required=True, help="Domain name for the hosted zone")

    # Add DNS record command
    dns_add_parser = subparsers.add_parser('add-record', help="Add a DNS record")
    dns_add_parser.add_argument('--zone-id', type=str, required=True, help="ID of the hosted zone")
    dns_add_parser.add_argument('--record-name', type=str, required=True, help="DNS record name")
    dns_add_parser.add_argument('--record-value', type=str, required=True, help="DNS record value")

    # Update DNS record command
    dns_update_parser = subparsers.add_parser('update-record', help="Update a DNS record")
    dns_update_parser.add_argument('--zone-id', type=str, required=True, help="ID of the hosted zone")
    dns_update_parser.add_argument('--record-name', type=str, required=True, help="DNS record name")
    dns_update_parser.add_argument('--record-value', type=str, required=True, help="DNS record value")

    # Delete DNS record command
    dns_delete_parser = subparsers.add_parser('delete-record', help="Delete a DNS record")
    dns_delete_parser.add_argument('--zone-id', type=str, required=True, help="ID of the hosted zone")
    dns_delete_parser.add_argument('--record-name', type=str, required=True, help="DNS record name")
    dns_delete_parser.add_argument('--record-value', type=str, required=True, help="DNS record value")

    args = parser.parse_args()

    if args.command == 'create-zone':
        create_route53_zone(args.domain)
    elif args.command == 'add-record':
        add_dns_record(args.zone_id, args.record_name, args.record_value)
    elif args.command == 'update-record':
        update_dns_record(args.zone_id, args.record_name, args.record_value)
    elif args.command == 'delete-record':
        delete_dns_record(args.zone_id, args.record_name, args.record_value)


if __name__ == "__main__":
    main()
