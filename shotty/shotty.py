import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{"Name":"tag:Project", "Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Command to operate on instances"""

@instances.command("list")
@click.option('--project', default=None, help="Only instances for project (tag Project: <Name>)")
def list_instances(project):

    for i in filter_instances(project):
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            i.public_ip_address
        )))

@instances.command("stop")
@click.option('--project', default=None, help="Stop only instances that belong to specific project")
def stop_instances(project):

    for i in filter_instances(project):
        print('Stopping {0} '.format(i.id))
        i.stop()

@instances.command("start")
@click.option('--project', default=None, help="Stop only instances that belong to specific project")
def stop_instances(project):

    for i in filter_instances(project):
        print('Starting {0} '.format(i.id))
        i.start()

if __name__ == '__main__':
    instances()
