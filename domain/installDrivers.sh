#executed as sudo
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

apt-get install -y apt-utils
apt-get install -y gnupg2
apt-get install -y software-properties-common
apt-get install -y wget
apt-get install -y python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
sed -i "/osm-download.etsi.org/d" /etc/apt/sources.list
wget -qO - https://osm-download.etsi.org/repository/osm/debian/ReleaseNINE/OSM%20ETSI%20Release%20Key.gpg | apt-key add -
add-apt-repository -y "deb [arch=amd64] https://osm-download.etsi.org/repository/osm/debian/ReleaseNINE stable devops IM osmclient"
apt-get update
pip3 install python-magic pyangbind verboselogs
apt-get install -y python3-osmclient