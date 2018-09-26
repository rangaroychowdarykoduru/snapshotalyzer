import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

#Common function to get instances
def filter_instances(project):
    instances = []

    if project:
        filters = [{"Name":"tag:Project", "Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

#Main group
@click.group()
def cli():
    """Shotty for managing snapshots"""

#Snapshots group of commands
@cli.group('snapshots')
def snapshots():
    """Comman to operate on snapshots"""

#Get list of volumes
@snapshots.command("list")
@click.option('--project', default=None, help="Only instances for project (tag Project: <Name>)")
def list_snapshots(project):

    for i in filter_instances(project):
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c')
                )))
    return

#Volumes group of commands
@cli.group('volumes')
def volumes():
    """Comman to operate on volumes"""

#Get list of volumes
@volumes.command("list")
@click.option('--project', default=None, help="Only instances for project (tag Project: <Name>)")
def list_volumes(project):

    for i in filter_instances(project):
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + " GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

# Instances group of commands
@cli.group('instances')
def instances():
    """Command to operate on instances"""

#Create snapshot for instances
@instances.command("create-snapshots")
@click.option('--project', default=None, help="Only instances for project (tag Project: <Name>)")
def create_snapshot(project):

    for i in filter_instances(project):
        print("Stopping {0}".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0} from {1}".format(v.id, i.id))
            v.create_snapshot(Description="Creating snapshot from snapshotalyzer of {0} from {1}".format(v.id, i.id))

        print('Starting {0}'.format(i.id))

        i.start()
        i.wait_until_running()
    return

#Get list of instances
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
            i.public_ip_address or ''
        )))
    return

# Stop instances
@instances.command("stop")
@click.option('--project', default=None, help="Stop only instances that belong to specific project")
def stop_instances(project):

    for i in filter_instances(project):
        print('Stopping {0} '.format(i.id))
        i.stop()
    return

#Start instances
@instances.command("start")
@click.option('--project', default=None, help="Stop only instances that belong to specific project")
def stop_instances(project):

    for i in filter_instances(project):
        print('Starting {0} '.format(i.id))
        i.start()

    return

#Main function
if __name__ == '__main__':
    cli()
