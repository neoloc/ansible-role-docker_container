import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_is_running(host):
    cmd = host.service('docker')
    assert cmd.is_running
    assert cmd.is_enabled


def test_docker_daemon_connection(host):
    c = host.run('docker ps')
    assert c.rc == 0


def test_docker_containers_running(host):
    c = host.run('docker ps')
    assert c.rc == 0
    assert 'nginx_instance_1' in c.stdout
    assert 'nginx_instance_2' in c.stdout


def test_deployed_containers(host):
    with host.sudo():
        c1 = host.run('curl http://localhost:3080')
        c2 = host.run('curl http://localhost:3081')
        assert c1.rc == 0
        assert 'Welcome to nginx!' in c1.stdout
        assert c2.rc == 0
        assert 'Welcome to nginx!' in c2.stdout
