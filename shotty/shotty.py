import boto3
import click

session = boto3.Session(profile_name='identity')
ec2 = session.resource('ec2')

@click.group()
def instances():
        """Commands for instances"""

@instances.command('list')
@click.option('--purpose', default=None, help="Only instances for this purpose (tag purpose:<name>)")

def list_instances(purpose):
    "List EC2 instances"
    instances = []

    if purpose:
        filters = [{'Name':'tag:purpose', 'Values': [purpose]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                tags.get('purpose', '<no tag>'))))

    return

@instances.command('stop')
@click.option('--purpose', default=None, help="Only instances for this purpose (tag purpose:<name>)")
def stop_instances(purpose):
    "Stop EC2 instances"
    instances = []

    if purpose:
        filters = [{'Name':'tag:purpose', 'Values': [purpose]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return

if __name__ == '__main__':
    
    instances()
        