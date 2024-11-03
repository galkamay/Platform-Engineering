import argparse
import boto3

# הגדרת Subnet דיפולטיבי
DEFAULT_SUBNET_ID = 'subnet-02305e9ebc28f7414'

def create_ec2_instance(ami_id, instance_type, name, assign_public_ip):
    ec2 = boto3.resource('ec2')

    network_interfaces = [{
        'SubnetId': DEFAULT_SUBNET_ID,
        'AssociatePublicIpAddress': assign_public_ip,
        'DeviceIndex': 0
    }]

    instances = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=network_interfaces,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'CreatedBy', 'Value': 'CLI'},
                    {'Key': 'Name', 'Value': name}
                ]
            }
        ]
    )

    for instance in instances:
        print(f"Instance {instance.id} created successfully with name '{name}' and public IP: {assign_public_ip}")
    return instances


def list_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
            Filters=[{'Name': 'tag:CreatedBy', 'Values': ['CLI']}]
    )

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}, Name: {instance['Tags']}")


def manage_instance(instance_id, action):
    ec2 = boto3.client('ec2')

    if action == 'start':
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} started.")
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} stopped.")
    elif action == 'terminate':
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} terminated.")


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for AWS EC2 management")

    subparsers = parser.add_subparsers(dest='command')

    # Create instance command
    create_parser = subparsers.add_parser('create',
                                          help="Create a new EC2 instance")
    create_parser.add_argument('--ami', type=str, required=True,
                               help="AMI ID to use for the instance")
    create_parser.add_argument('--type', type=str, required=True,
                               choices=['t3.nano', 't4g.nano'],
                               help="Instance type (t3.nano or t4g.nano)")
    create_parser.add_argument('--name', type=str, required=True,
                               help="Name to assign to the EC2 instance")
    create_parser.add_argument('--public-ip', action='store_true',
                               help="Assign a public IP to the instance")

    # List instances command
    list_parser = subparsers.add_parser('list',
                                        help="List EC2 instances created by this CLI")

    # Manage instance command (start/stop/terminate)
    manage_parser = subparsers.add_parser('manage',
                                          help="Start, stop, or terminate an EC2 instance")
    manage_parser.add_argument('instance_id', type=str,
                               help="ID of the instance to manage")
    manage_parser.add_argument('action', type=str, choices=['start', 'stop', 'terminate'],
                               help="Action to perform on the instance")

    args = parser.parse_args()

    if args.command == 'create':
        create_ec2_instance(args.ami, args.type, args.name, args.public_ip)
    elif args.command == 'list':
        list_ec2_instances()
    elif args.command == 'manage':
        manage_instance(args.instance_id, args.action)


if __name__ == "__main__":
    main()
