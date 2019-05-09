import boto3
import click

session = boto3.Session(profile_name='identity')
ec2 = session.resource('ec2')

@click.command()
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

if __name__ == '__main__':
    
    list_instances()
        