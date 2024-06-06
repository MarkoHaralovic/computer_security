#! /bin/sh

IPT=/sbin/iptables

$IPT -P INPUT DROP
$IPT -P OUTPUT DROP
$IPT -P FORWARD DROP

$IPT -F INPUT
$IPT -F OUTPUT
$IPT -F FORWARD

$IPT -A INPUT   -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A OUTPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

$IPT -A INPUT   -p icmp -j ACCEPT
$IPT -A FORWARD -p icmp -j ACCEPT
$IPT -A OUTPUT  -p icmp -j ACCEPT


$IPT -A FORWARD -p tcp -d 203.0.113.100 --dport 80 -j ACCEPT
$IPT -A FORWARD -p tcp -d 203.0.113.100 --dport 443 -j ACCEPT


$IPT -A FORWARD -p udp -d 203.0.113.200 --dport 53 -j ACCEPT
$IPT -A FORWARD -p tcp -d 203.0.113.200 --dport 53 -j ACCEPT

$IPT -A FORWARD -p tcp -s 10.0.0.20 -d 203.0.113.100 --dport 22 -j ACCEPT
$IPT -A FORWARD -p tcp -s 10.0.0.20 -d 203.0.113.200 --dport 22 -j ACCEPT

$IPT -A FORWARD -p tcp -s 203.0.113.100 -d 10.0.0.100 --dport 10000 -j ACCEPT


$IPT -A FORWARD -s 203.0.113.100 -j DROP


$IPT -A FORWARD -p tcp -d 10.0.0.100 --dport 22 -m iprange --src-range 10.0.0.0-10.0.0.105 -j ACCEPT

$IPT -A FORWARD -p tcp -d 10.0.0.100 --dport 10000 -s 203.0.113.100 -j ACCEPT
$IPT -A FORWARD -p tcp -d 10.0.0.100 --dport 10000 -m iprange --src-range 10.0.0.0-10.0.0.105 -j ACCEPT

$IPT -A FORWARD -s 10.0.0.100 -j DROP

$IPT -A FORWARD -p tcp -s 10.0.0.0/24 ! -s 10.0.0.100 --dport 80 -j ACCEPT
$IPT -A FORWARD -p tcp -s 10.0.0.0/24 ! -s 10.0.0.100 --dport 443 -j ACCEPT
$IPT -A FORWARD -p udp -s 10.0.0.0/24 ! -s 10.0.0.100 --dport 53 -j ACCEPT
$IPT -A FORWARD -p tcp -s 10.0.0.0/24 ! -s 10.0.0.100 --dport 53 -j ACCEPT

$IPT -A FORWARD -i eth0 -d 192.168.1.0/24 -j DROP

$IPT -A INPUT -p tcp -s 10.0.0.20 --dport 22 -j ACCEPT

$IPT -A INPUT -i eth0 -p tcp --dport 22 -j DROP
$IPT -A INPUT -i eth1 -p tcp --dport 22 -j DROP
$IPT -A INPUT -i eth2 -p tcp --dport 22 -j DROP

$IPT -A INPUT -j DROP