Vagrant.configure("2") do |config|

    config.vm.define "controller" do |controller|
        controller.vm.box = "ubuntu/focal64"
	controller.vm.hostname = "controller"
        controller.vm.synced_folder "controller", "/data"
	controller.vm.network "private_network", ip: "192.168.60.10", netmask: "255.255.255.0"
	controller.vm.provision :shell, path: "provisionVM.sh"
    end

    config.vm.define "proxy" do |proxy|
        proxy.vm.box = "ubuntu/focal64"
	proxy.vm.hostname = "proxy"
        proxy.vm.synced_folder "proxy", "/data"
	proxy.vm.network "private_network", ip: "192.168.60.11", netmask: "255.255.255.0"
	proxy.vm.network "private_network", ip: "192.168.61.10", netmask: "255.255.255.0"
	proxy.vm.provision :shell, path: "provisionVM.sh"
    end

    config.vm.define "attacker" do |attacker|
        attacker.vm.box = "ubuntu/focal64"
	attacker.vm.hostname = "attacker"
        attacker.vm.synced_folder "attacker", "/data"
	attacker.vm.network "private_network", ip: "192.168.61.15", netmask: "255.255.255.0"
	attacker.vm.provision :shell, path: "provisionVM.sh"
    end
end
