# CouchDB installation for CentOS 7

## Enabling the Apache CouchDB package repository

Place the following text into `/etc/yum.repos.d/bintray-apache-couchdb-rpm.repo`:
```
[bintray--apache-couchdb-rpm]
name=bintray--apache-couchdb-rpm
baseurl=http://apache.bintray.com/couchdb-rpm/el$releasever/$basearch/
gpgcheck=0
repo_gpgcheck=0
enabled=1
```

## Installing the Apache CouchDB packages

Run the command:
```
$ sudo yum -y install epel-release && yum install couchdb
```

## Start the service

Run the command:
```
systemctl start couchdb
systemctl enable couchdb
```

Now check the service.
```
systemctl status couchdb
```

Now check the server port.
```
netstat -plntu
```

Apache CouchDB has been successfully installed on the CentOS 7 server, and is running under default port 5984.

## Enable Apache CouchDB HTTP server

Apache CouchDB provides the HTTP server for admin access on default port 5984. And has an admin panel Web UI named 'Fauxton'.

In this step, we will enable the CouchDB HTTP server for admin panel access. So to begin with, go to the apache couchdb installation directory '/opt/couchdb', and edit the 'default.ini' configuration file under 'etc/' directory.

```
cd /opt/couchdb
vim etc/default.ini
```

Now go to the '[chttpd]' configuration line and change the bind_address value with your IP address.
```
[chttpd]
port = 5984
bind_address = 0.0.0.0
```

Save and exit.

Restart the couchdb service using the following systemctl command.
```
systemctl restart couchdb
```

Next, open your web browser and type your server IP address as shown below.

http://192.168.1.11:5984/_utils/

And you should get the Fauxton web UI page.

### Note
If you have firewall running on your server, open the couchdb port 5984 using the firewall-cmd command, as shown below.

```
firewall-cmd --add-port=5984/tcp --permanent
firewall-cmd --reload
```

## Configure admin account CouchDB
By default, the fresh Apache CouchDB installation has an 'Admin Party'. So anyone who connects to CouchDB server can do anything, including create, delete, add new user etc. In this step, we want to add new admin account for the CouchDB, and we will create that admin account from the admin panel.

Open your web browser and visit the following server IP address on port 5984.

http://192.168.1.11:5984/_utils/

Now click on the 'Admin Party' tab, type the admin user and password for couchdb, and then click the 'Create Admin' button.

New admin user for couchdb has been created.

Now, if you want to login to the admin panel Fauxton again, you will have to enter the login details.

Type your admin user and password to get access to the admin panel.