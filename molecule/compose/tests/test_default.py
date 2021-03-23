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


def test_docker_container_running(host):
    c = host.run('docker ps')
    assert c.rc == 0
    assert 'wordpress' in c.stdout
    assert 'db' in c.stdout
    assert 'seafile_instance' in c.stdout


def test_deployed_container(host):
    with host.sudo():
        c = host.run('curl -L http://localhost:8000')
        assert c.rc == 0
        assert 'Select a default language' in c.stdout


def test_exported_compose_definition(host):
    dcfile = host.file("/root/docker-composes/wordpress/docker-compose.yml")
    assert dcfile.exists


def test_exported_compose_definition_absent(host):
    dcfile = host.file("/root/docker-composes/wordpress2/docker-compose.yml")
    assert not dcfile.exists


def test_docker_container_not_running(host):
    c = host.run('docker ps')
    assert c.rc == 0
    assert 'wordpress2' not in c.stdout
