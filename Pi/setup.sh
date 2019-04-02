apt-get install git 
git clone https://github.com/kismetwireless/kismet.git
git clone https://github.com/the-tcpdump-group/libpcap.git
apt-get install screen ncurses-dev libpcap-dev tcpdump libmicrohttpd-dev flex byacc
cd libpcap
./configure
make
make install
cd ..
cd kismet
./configure
make dep
make
make install
sed -i 's/logtypes=[^$]\+/logtypes=netxml/g' /usr/local/etc/kismet.conf
sed -i 's/ncsource=[^$]\+/ncsource=wlan0/g' /usr/local/etc/kismet.conf
sed -i 's/logprefix=[^$]\+/logprefix=\/home\/pi\/kismet/g' /usr/local/etc/kismet.conf
mkdir /home/pi/kismet
chmod 777 /home/pi/kismet
cp ./packaging/systemd/kismet.service.in /lib/systemd/system/kismet.service
systemctl daemon-reload 
systemctl start kismet
systemctl enable kismet


