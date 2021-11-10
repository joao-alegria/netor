#executed as sudo
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

apt-get install -y apt-utils=1.6.*
apt-get install -y gnupg2=2.2.*
apt-get install -y software-properties-common=0.96.24.32.*
apt-get install -y wget=1.19.*
apt-get install -y python-dev=2.7.* python3-dev=3.6.* build-essential=12.* libssl-dev=1.1.* libffi-dev=3.2.* libxml2-dev=2.9.* libxslt1-dev=1.1.* zlib1g-dev=1:1.2.11.*
sed -i "/osm-download.etsi.org/d" /etc/apt/sources.list
wget -qO - https://osm-download.etsi.org/repository/osm/debian/ReleaseNINE/OSM%20ETSI%20Release%20Key.gpg | apt-key add -
add-apt-repository -y "deb [arch=amd64] https://osm-download.etsi.org/repository/osm/debian/ReleaseNINE stable devops IM osmclient"
apt-get update
pip3 install python-magic==0.4.24 pyangbind==0.8.1 verboselogs==1.7
apt-get install -y python3-osmclient