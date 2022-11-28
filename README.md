# SDS-final-project - น้องมาย

# Setup

## Worker Nodes

1. Set Static IP
```
sudo nano /etc/dhcpcd.conf
```
then paste these lines
```
interface eth0
static ip_address=x.x.x.y/24
static routers=x.x.x.1
static domain_name_servers=8.8.8.8
```
then ```sudo reboot```


2. Install microk8s
```
sudo snap install microk8s --classic
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
1.3 Enable DNS <br/>
1.4 Enable ingress <br/>

## ทุกตัว

เพิ่มใน /etc/hosts  ว่า
```
192.168.0.198 master00
192.168.0.170 master01
192.168.0.171 master02
192.168.0.201 node01
192.168.0.202 node02
192.168.0.203 node03
192.168.0.204 node04
192.168.0.205 node05
```

# Application Deployment

## At master node
```
sudo microk8s enable ingress dns
sudo microk8s kubectl apply -f db.yaml
sudo microk8s kubectl apply -f todo.yaml
sudo microk8s kubectl apply -f todo-noti.yaml
sudo microk8s kubectl apply -f ingress.yaml
```

