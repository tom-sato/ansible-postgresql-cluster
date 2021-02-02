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
  (1..num_nodes).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.hostname = "node-#{i}.example.com"
      node.vm.network "private_network", type: "dhcp"
      if playbook == "pacemaker-drbd"
        node.vm.provider "virtualbox" do |vb|
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
        end
      end
    end
  end
end
