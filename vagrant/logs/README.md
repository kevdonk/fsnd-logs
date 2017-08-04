This repo contains a virtual machine with a program that reads and reports on fake news data.
Executing `logs/application.py` will display information about popular articles, authors and days where the site traffic logs had more than 1% errors.

### Requires

VirtualBox https://www.virtualbox.org/wiki/Downloads
Vagrant https://www.vagrantup.com/downloads.html

### Set up

1. Navigate to the folder with the Vagrantfile in it
2. run `vagrant up`
3. run `vagrant ssh`
4. navigate to shared folder with `cd /vagrant`
5. copy data to db with `psql -d news -f newsdata.sql` (available from Udacity course)

### To Run
1. navigate to logs folder with `cd logs`
2. execute program with `python application.py`

