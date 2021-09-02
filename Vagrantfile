# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  playbook = ENV["PLAYBOOK"] ? ENV["PLAYBOOK"] : "postgresql"
  num_nodes = (playbook == "pacemaker-drbd") ? 2 : (ENV["NUM_NODES"] ? [ENV["NUM_NODES"].to_i, 1].max : 3)
  box = ENV["BOX"] ? ENV["BOX"] : "centos/8"
  if Vagrant.has_plugin?("vagrant-proxyconf") && ENV["PROXY"]
    config.proxy.http = ENV["PROXY"]
    config.proxy.https = ENV["PROXY"]
    config.proxy.ftp = ENV["PROXY"]
    config.proxy.no_proxy = "localhost,127.0.0.1," + (1..num_nodes).map{|i| "node-%d" % i}.join(",")
  end
  config.vm.box = box
  # shared folder can't be used in WSL
  # see https://github.com/hashicorp/vagrant/issues/10576
  config.vm.synced_folder ".", "/vagrant", disabled: true
  (1..num_nodes).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.hostname = "node-#{i}.example.com"
      node.vm.network "private_network", type: "dhcp"
      #node.vm.network "private_network", ip: "172.28.128.#{100 + i}"
      node.vm.provider "virtualbox" do |vb|
        #vb.gui = true
        vb.memory = 1024
        #vb.cpu = 1
        if ["pacemaker-drbd", "lifekeeper-datakeeper"].include?(playbook)
          disk = "disk-#{i}.vmdk"
          unless File.exists?(disk)
            vb.customize ["createhd", "--filename", disk, "--size", 10 * 1024, "--format", "VMDK"]
          end
          vb.customize ["storageattach", :id, "--storagectl", "IDE", "--port", 1, "--device", 0, "--type", "hdd", "--medium", disk]
        end
      end
      if i == num_nodes
        node.vm.provision "ansible" do |ansible|
          ansible.playbook = "#{playbook}.yml"
          ansible.limit = "all"
          ansible.extra_vars = {
            #ansible_python_interpreter: "/usr/libexec/platform-python",
            #postgresql_version: "13",
            #postgresql_extra_config_parameters: <<~EOS,
            #  max_connections = 100
            #  shared_buffers = 128MB
            #EOS
            #postgresql_setup_stage: "write_recovery_conf",
            #pgpool2_version: "4.2",
            #pgpool2_delegate_ip: "172.28.128.201",
            #pgpool2_extra_config_parameters: <<~EOS,
            #  num_init_children = 32
            #  max_pool = 4
            #EOS
          }
        end
      end
    end
  end
end
