// named.conf
//

options {
	directory "/var/named/etc/namedb";
	dnssec-enable no;
	dnssec-validation no;
        allow-recursion { any; };
        allow-query { any; };
        allow-query-cache { any; };
};

key "rndc-key" {
	algorithm hmac-md5;
	secret "pUkeN0gBlageylNhNauKdQ==";
};

controls {
        inet 127.0.0.1 allow { localhost; } keys { "rndc-key"; };
};

zone "." {
	type master;
	file "root.com";
};

zone "com." {
	type master;
	file "com";
};

zone "example.com." {
	type master;
	file "example-com";
};

zone "0.0.127.IN-ADDR.ARPA" {
	type master;
	file "localhost.rev";
};

zone "100.51.198.IN-ADDR.ARPA" {
	type master;
	file "198.in-addr.arpa";
};

zone "IN-ADDR.ARPA" {
 	type master;
 	file "in-addr.arpa";
};

