#! /bin/sh

if [ `id -u` -ne  0 ]; then
    echo "You must be root to run this script."
    exit 1
fi

himage -e server > /dev/null
if test $? -ne 0; then
    echo "If server is not a unique name, multiple experiments are running with the same node names."
    echo "Experiment Terminate / File Quit / sudo cleanupAll"
    echo ""
    echo "If the error is: 'cannot find node name server', you must start the experiment: Experiment->Execute"
    exit 1
fi

cd conf_files

echo "Preparing DNS ..."
# Resolv conf:
for h in pc admin database www FW
do
    hcp resolv.conf.edu $h:/etc/resolv.conf
done

for h in client server
do
    hcp resolv.conf.com $h:/etc/resolv.conf
done

# DNS server:
himage dns killall -9 named > /dev/null 2>&1
himage dns mkdir -p /var/named/etc/namedb
himage server killall -9 named > /dev/null 2>&1
himage server mkdir -p /var/named/etc/namedb

hcp named.conf.edu root.edu example-edu 203.in-addr.arpa in-addr.arpa localhost.rev    dns:/var/named/etc/namedb
hcp named.conf.com root.com example-com 198.in-addr.arpa in-addr.arpa localhost.rev    server:/var/named/etc/namedb

hcp rndc.key dns:/etc/bind/
hcp rndc.key server:/etc/bind/

himage dns named -c /var/named/etc/namedb/named.conf.edu
himage server named -c /var/named/etc/namedb/named.conf.com

echo "Preparing Web ..."
# Web server:
for h in www server database
do
    himage $h killall -9 lighttpd > /dev/null 2>&1
    himage $h mkdir -p /usr/local/etc/lighttpd
    himage $h mkdir -p /var/log/lighttpd
    himage $h chown -R www-data:www-data /var/log/lighttpd
    hcp lighttpd-${h}.conf $h:/usr/local/etc/lighttpd/lighttpd.conf
    himage $h chmod 755 /usr/local/etc/lighttpd/lighttpd.conf
    himage $h mkdir -p /root/www
    hcp index.html.${h} ${h}:/root/www/index.html
    himage -b $h lighttpd -f /usr/local/etc/lighttpd/lighttpd.conf
done

