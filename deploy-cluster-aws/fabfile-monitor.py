from fabric.api import sudo, env
from fabric.api import task
from fabric.operations import put, run

# Ignore known_hosts
# http://docs.fabfile.org/en/1.10/usage/env.html#disable-known-hosts
env.disable_known_hosts = True

env.user = 'ubuntu'
env.key_filename = 'pem/bigchaindb.pem'


@task
def install_docker_engine():
    """Install docker on an ec2 ubuntu 14.04 instance

    Example:
        fab --fabfile=fabfile-monitor.py \
            --hosts=ec2-52-58-106-17.eu-central-1.compute.amazonaws.com \
            install_docker
    """

    # install prerequisites
    sudo('apt-get update')
    sudo('apt-get -y install apt-transport-https ca-certificates linux-image-extra-$(uname -r) apparmor')

    # install docker repositories
    sudo('apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 \
          --recv-keys 58118E89F3A912897C070ADBF76221572C52609D')
    sudo("echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' | \
          sudo tee /etc/apt/sources.list.d/docker.list")

    # install docker engine
    sudo('apt-get update')
    sudo('apt-get -y install docker-engine')

    # add ubuntu user to the docker group
    sudo('usermod -aG docker ubuntu')


@task
def install_docker_compose():
    sudo('curl -L https://github.com/docker/compose/releases/download/1.7.0/docker-compose-`uname \
         -s`-`uname -m` > /usr/local/bin/docker-compose')
    sudo('chmod +x /usr/local/bin/docker-compose')


@task
def run_monitor():
    # copy docker-compose-monitor to the ec2 instance
    put('../docker-compose-monitor.yml')
    run('docker-compose -f docker-compose-monitor.yml up -d')
