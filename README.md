Ansible Playbooks for PostgreSQL Clusters
=========================================

Ansible playbooks that set up various [PostgreSQL](https://www.postgresql.org/) clusters for testing, such as streaming replication, Pgpool-II, Pacemaker and DRBD.

Requirements
------------

The requirements are as follow:

* VirtualBox 6.0.x
* Vagrant 2.2.x
* Vagrant box [centos/8](https://app.vagrantup.com/centos/boxes/8) or [centos/7](https://app.vagrantup.com/centos/boxes/7)
* Ansible 2.9.x

Usage
-----

For example, when setting up a PostgreSQL cluster with Pgpool-II, the usage is as follows:

```ShellSession
$ git clone https://github.com/tom-sato/ansible-postgresql-cluster.git
$ cd ansible-postgresql-cluster
$ PLAYBOOK=pgpool2 vagrant up --provision
(snip)
PLAY RECAP *********************************************************************
node-1                     : ok=64   changed=47   unreachable=0    failed=0    skipped=28   rescued=0    ignored=0
node-2                     : ok=61   changed=44   unreachable=0    failed=0    skipped=31   rescued=0    ignored=0
node-3                     : ok=61   changed=44   unreachable=0    failed=0    skipped=31   rescued=0    ignored=0

$ PLAYBOOK=pgpool2 vagrant ssh node-1
$ sudo su - postgres
$ psql -c "SHOW pool_nodes" -h vip-1 -p 9999
 node_id | hostname | port | status | lb_weight |  role   | select_cnt | load_balance_node | replication_delay | replication_state | replication_sync_state | last_status_change
---------+----------+------+--------+-----------+---------+------------+-------------------+-------------------+-------------------+------------------------+---------------------
 0       | node-1   | 5432 | up     | 0.333333  | primary | 0          | true              | 0                 |                   |                        | 2021-02-02 23:56:16
 1       | node-2   | 5432 | up     | 0.333333  | standby | 0          | false             | 0                 | streaming         | async                  | 2021-02-02 23:56:16
 2       | node-3   | 5432 | up     | 0.333333  | standby | 0          | false             | 0                 | streaming         | async                  | 2021-02-02 23:56:16
(3 rows)

```

Environment Variables
---------------------

The `Vagrantfile` file receives the following environment variables:

* `PLAYBOOK` - Specifies the playbook name. The default is `postgresql`. See [here](#user-content-playbooks) for available playbooks.
* `NUM_NODES` - Specifies the number of nodes. The default is `3` for not using DRBD, and `2` otherwise.
* `BOX` - Specifies the box name. The default is `centos/8`.
* `PROXY` - Specifies the proxy to set for the virtual machine. The default is an empty string. The [vagrant-proxyconf](https://github.com/tmatilai/vagrant-proxyconf) plugin should be installed in advance.

Playbooks
---------

The following playbooks are available:

* `postgresql.yml` - Sets up a PostgreSQL cluster with streaming replication.
* `pgpool2.yml` - Sets up a PostgreSQL cluster with [Pgpool-II](https://www.pgpool.net/).
* `pacemaker-drbd.yml` - Sets up a PostgreSQL cluster with [Pacemaker](https://clusterlabs.org/pacemaker/) and [DRBD](https://www.linbit.com/drbd/).
* `pacemaker-replication.yml` - Sets up a PostgreSQL cluster with Pacemaker and streaming replication.
* `pacemaker-paf.yml` - Sets up a PostgreSQL cluster with Pacemaker and streaming replication using [PAF](https://clusterlabs.github.io/PAF/).
* `repmgr.yml` - Sets up a PostgreSQL cluster with [repmgr](https://repmgr.org/). (experimental)

Roles
-----

Each playbook calls the following roles. Some playbooks overwrite role variables as needed.

### `locale`

Configures locale settings.

* `locale` - Specifies the locale. The default is `ja_JP.UTF-8`.
* `keymap` - Specifies the keymap. The default is `jp`.
* `x11_keymap_layout` - Specifies the X11 keymap layout. The default is `jp`.
* `x11_keymap_model` - Specifies the X11 keymap model. The default is `jp106`.
* `timezone` - Specifies the timezone. The default is `Asia/Tokyo`.

### `hosts`

Configures the `/etc/hosts` file.

* `public_interface` - Specifies the device name of the public interface. The default is `eth1`.

### `postgresql`

Sets up PostgreSQL servers.

* `postgresql_version` - Specifies the PostgreSQL version. The default is `13`.
* `postgresql_data_directory` - Specifies the data directory path. The default is `/var/lib/pgsql/{{ postgresql_version }}/data`.
* `postgresql_syslog_facility` - Specifies the syslog facility. The default is `LOCAL0`.
* `postgresql_syslog_file` - Specifies the syslog file path. The default is `/var/log/postgresql-{{ postgresql_version }}`.
* `postgresql_port` - Specifies the port number. The default is `5432`.
* `postgresql_password` - Specifies the password for the `postgres` user. The default is `postgres`.
* `postgresql_auth_method` - Specifies the authentication method for local connections in `pg_hba.conf`. The default is `scram-sha-256` for PostgreSQL 10 or later, and `md5` otherwise.
* `postgresql_extra_initdb_options` - Specifies extra options for the `initdb` command. The default is `-E UTF8 --locale=C`.
* `postgresql_extra_config_parameters` - Specifies extra parameters in `postgresql.conf`. The default is an empty string.
* `postgresql_extra_hba_records` - Specifies extra records in `pg_hba.conf`. The default is to use the authentication method specified by `postgresql_auth_method` for connections from the same network.
* `postgresql_control_as_service` - Specifies whether to control as a service. The default is `yes`.
* `postgresql_setup_stage` - Specifies which stage to set up. `install` installs PostgreSQL, `initdb` creates a database cluster, `basebackup` takes a base backup, `write_recovery_conf` writes settings for the standby server. The default is `write_recovery_conf`.
* `postgresql_primary_hostname` - Specifies the host name of the primary server. The default is the host name of the first node of all.
* `postgresql_extra_recovery_config_parameters` - Specifies extra parameters for the standby server in `postgresql.auto.conf` for PostgreSQL 12 or later, and in `recovery.conf` otherwise. The default is an empty string.
* `postgresql_use_rewind` - Specifies whether to use the `pg_rewind` command when following the primary server with Pgpool-II. The default is `no`.
* `postgresql_use_replication_slot` - Specifies whether to use the replication slot. The default is `yes`.

### `pgpool2`

Sets up Pgpool-II servers.

* `pgpool2_version` - Specifies the Pgpool-II version. The default is `4.2`.
* `pgpool2_syslog_facility` - Specifies the syslog facility. The default is `LOCAL1`.
* `pgpool2_syslog_file` - Specifies the syslog file path. The default is `/var/log/pgpool2`.
* `pgpool2_delegate_ip` - Specifies the virtual IP address. The default is an unused IP address in all nodes.
* `pgpool2_delegate_hostname` - Specifies the host name of the virtual IP address. The default is `vip-1`.
* `pgpool2_pcp_port` - Specifies the PCP port number. The default is `9898`.
* `pgpool2_pcp_username` - Specifies the PCP user name. The default is `postgres`.
* `pgpool2_pcp_password` - Specifies the PCP password. The default is `postgres`.
* `pgpool2_backend_clustering_mode` - Specifies the backend clustering mode. Valid values are `streaming_replication` (the default), `native_replication`, `snapshot_isolation` (for Pgpool-II 4.2 or later), and `raw`. `logical_replication` and `slony` are not supported.
* `pgpool2_port` - Specifies the port number. The default is `9999`.
* `pgpool2_trusted_servers` - Specifies trusted servers separated by commas. The default is the IP address of the default gateway.
* `pgpool2_wd_port` - Specifies the watchdog port number. The default is `9000`.
* `pgpool2_heartbeat_port` - Specifies the heartbeat port umber. The default is `9694`.
* `pgpool2_extra_config_parameters` - Specifies extra parameters in `pgpool.conf`. The default is an empty string.
* `pgpool2_extra_hba_records` - Specifies extra records in `pool_hba.conf`. The default is to use the authentication method specified by `postgresql_auth_method` for connections from the same network.
* `pgpool2_encryption_key` - Specifies the encryption key stored in the `~/.pgpoolkey` file. The default is `postgres`.

### `drbd`

Sets up a DRBD filesystem.

* `drbd_version` - Specifies the DRBD version. The default is `9.0`.
* `drbd_disk` - Specifies the disk device path. The default is `/dev/sdb1`.
* `drbd_resource_name` - Specifies the resource name. The default is `my_resource`.
* `drbd_device` - Specifies the DRBD device path. The default is `/dev/drbd0`.
* `drbd_port` - Specifies the port number. The default is `7789`.
* `drbd_control_as_service` - Specifies whether to control as a service. The default is `no`.
* `drbd_mount_directory` - Specifies the mount directory path. The default is `/mnt/mirror`.
* `drbd_fstype` - Specifies the filesystem type. The default is `xfs`.
* `drbd_primary_hostname` - Specifies the host name of the primary server. The default is the host name of the first node of all.

### `pacemaker`

Sets up a Pacemaker cluster.

* `pacemaker_password` - Specifies the password for the `hacluster` user. The default is `hacluster`.
* `pacemaker_cluster_name` - Specifies the cluster name. The default is `my_cluster`.
* `pacemaker_migration_threshold` - Specifies the value of the `migration-threshold` attribute. The default is `2`. See the [Resource Meta-Attributes](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/2.0/html/Pacemaker_Explained/s-resource-options.html#_resource_meta_attributes) in the Pacemaker Explained for details.
* `pacemaker_failure_timeout` - Specifies the value of the `failure-timeout` attribute. The default is `60s`. See the [Resource Meta-Attributes](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/2.0/html/Pacemaker_Explained/s-resource-options.html#_resource_meta_attributes) in the Pacemaker Explained for details.
* `pacemaker_no_quorum_policy` - Specifies the value of the `no-quorum-policy` options. The default is `stop`, and `ignore` for 2 nodes. See the [Cluster Options](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/2.0/html/Pacemaker_Explained/s-cluster-options.html#s-cluster-options) in the Pacemaker Explained for details.
* `pacemaker_use_softdog` - Specifies whether to use the software watchdog. The default is `no`.

### `pacemaker-*`

Creates resources on the Pacemaker cluster.

* `pacemaker_resource_prefix` - Specifies the prefix to be added to the beginning of the resource name. The default is `my_`.
* `pacemaker_virtual_ip` - Specifies the virtual IP address. The default is an unused IP address in all nodes.
* `pacemaker_virtual_hostname` - Specifies the host name of the virtual IP address. The default is `vip-1`.
* `pacemaker_pgsql_rep_mode` - Specifies the replication mode in the `pacemaker-replication` role. Valid values are `async` (the default), `sync`, and `slave`.
* `pacemaker_pgsql_replication_slot_name` - Specifies the slot name when using the replication slot in the `pacemaker-replication` role. The default is `{{ pacemaker_resource_prefix + 'slot' }}`.

### `repmgr`

Sets up repmgr servers.

* `repmgr_syslog_facility` - Specifies the syslog facility. The default is `LOCAL1`.
* `repmgr_syslog_file` - Specifies the syslog file path. The default is `/var/log/repmgr{{ postgresql_version | regex_replace('\.') }}`.

License
-------

BSD

Author Information
------------------

Tomoaki Sato
