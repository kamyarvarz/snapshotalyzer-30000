import boto3
import botocore
import click

session = boto3.Session(profile_name='identity')
ec2 = session.resource('ec2')

def filter_instances(purpose):
     instances = []

     if purpose:
        filters = [{'Name':'tag:purpose', 'Values': [purpose]}]
        instances = ec2.instances.filter(Filters=filters)
     else:
        instances = ec2.instances.all()

     return instances


@click.group('')
def cli():
        """Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
        """Commands for snapshots"""

@cli.group('volumes')
def volumes():
        """Commands for volumes"""

@cli.group('instances')
def instances():
        """Commands for instances"""

@snapshots.command('list')
@click.option('--purpose', default=None, help="Only snapshots for this purpose (tag purpose:<name>)")
def list_snapshots(purpose):
    "List EC2 snapshots"
    
    instances = filter_instances(purpose)

    for i in instances:
            for v in i.volumes.all():
                    for s in v.snapshots.all():
                        print(', '.join((
                                s.id,
                                v.id,
                                i.id,
                                s.state,
                                s.progress,
                                s.start_time.strftime("%c")
                                )))

    return

@instances.command('snapshot',help="Create snapshots of all volumes")
@click.option('--purpose', default=None, help="Only instances for this purpose (tag purpose:<name>)")
def create_snapshots(purpose):
    "Create snapshots for EC2 instances"
    
    instances = filter_instances(purpose)
    for i in instances:
                print("Stopping {0}...".format(i.id))
                i.stop()
                i.wait_until_stopped()

                for v in i.volumes.all():
                        print("Creating snapshots of {0}".format(v.id))
                        v.create_snapshot(Description="Created by snapshotalyzer-30000")
                print("Restarting {0}...".format(i.id))
                i.start()
# we want ot restart one instnace at a time
                i.wait_until_running()
    print ("Job's done!")
    return



@instances.command('list')
@click.option('--purpose', default=None, help="Only instances for this purpose (tag purpose:<name>)")
def list_instances(purpose):
    "List EC2 instances"
    
    instances = filter_instances(purpose)

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
    
    instances = filter_instances(purpose)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:

                i.stop()
        except botocore.exceptions.ClientError as e:
                print(" Could not stop {0}. ".format(i.id) + str(e))
                continue        
    return

@instances.command('start')
@click.option('--purpose', default=None, help="Only instances for this purpose (tag purpose:<name>)")
def start_instances(purpose):
    "Start EC2 instances"
    
    instances = filter_instances(purpose)

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
                i.start()
        except botocore.exceptions.ClientError as e:
                print(" Could not start {0}. ".format(i.id) + str(e))
                continue
    return

@volumes.command('list')
@click.option('--purpose', default=None, help="Only volumes for this purpose (tag purpose:<name>)")
def list_volumes(purpose):
    "List EC2 volumes"
    
    instances = filter_instances(purpose)
         
    for i in instances:
        for v in i.volumes.all():
                print(', '.join((
                        v.id,
                        i.id,
                        v.state,
                        str(v.size) + "GiB",
                        v.encrypted and "Encrypted" or "Not Encrypted" )))

    return


if __name__ == '__main__':
    
    cli()
        