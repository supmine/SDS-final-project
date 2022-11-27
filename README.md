# SDS-final-project - น้องมาย

# Setup

## Worker Nodes

1. Set Static IP
```
sudo nano /etc/netplan/50-cloud-init.yaml
```
then paste this
```
network:
    ethernets:
        eth0:
            dhcp4: false
            addresses: [{Static IP of worker node}/24]
            gateway4: {Static IP of Gateway}
            nameservers:
              addresses: [{Static IP of Gateway},8.8.8.8,8.8.4.4,]
    version: 2
```

2. Install microk8s
```
sudo snap install microk8s --classic --channel=1.25
```

3. run this command
```
microk8s join {Static IP of master}:25000/{secret_key} --worker
```



## Master Node
1. Set Static IP <br/>
1.1 Go to settings <br/>
1.2 Go to network <br/>
1.3 Click at setup <br/>
1.4 Click at IPv4 <br/>
1.5 Change IPv4 Method to Manual <br/>
1.6 Type this in address <br/>
[{IP of Master Node}, {Netmask}, {IP of Gateway}] <br/>
1.7 On DNS field type 8.8.4.4, 8.8.8.8 <br/>
1.8 Restart network

2. Add nodes <br/>
1.1 sudo microk8s add-node <br/>
1.2 เอาคำสั่งไปวางใน Nodes <br/>
```
microk8s join 192.168.0.200:25000/9f50463f7abd06a0336e8feb774c070c/9f9d297ee2f6 --worker
```
1.3 ไป Enable DNS <br/>
1.4 Enable ingress <br/>

## ทุกตัว

เพิ่มในไฟล์/etc/resolv.conf ว่า
```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

เพิ่มใน /etc/hosts  ว่า
```
192.168.0.199 master02
192.168.0.200 master-virtual-machine
192.168.0.201 node01
192.168.0.202 node02
192.168.0.203 node03
192.168.0.204 node04
192.168.0.205 node05
```

# Application Deployment

## At master node
```
sudo microk8s enable ingress
sudo microk8s kubectl apply -f mongodb.yaml
sudo microk8s kubectl apply -f dataset-mgmt.yaml
sudo microk8s kubectl apply -f data-entry-getter.yaml
sudo microk8s kubectl apply -f gateway.yaml
sudo microk8s kubectl apply -f ingress.yaml
```

