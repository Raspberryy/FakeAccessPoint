# Enter Folder
cd Programs

# Python Modules
sudo apt-get install python3-dev -y
sudo apt-get install python-dev -y

wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py --insecure

wget https://pypi.python.org/packages/18/fa/dd13d4910aea339c0bb87d2b3838d8fd923c11869b1f6e741dbd0ff3bc00/netifaces-0.10.4.tar.gz
tar xvzf netifaces-0.10.4.tar.gz
rm netifaces-0.10.4.tar.gz
cd netifaces-0.10.4
python setup.py install
cd ..

# Clean
rm ez_setup.py
rm setuptools-26.0.0.zip

# DHCP3 Server
sudo apt-get install dhcp3-server -y --force-yes

if [ "$1" != "--kali" ]
then

  # Ettercap
  sudo apt-get install zlib1g zlib1g-dev -y
  sudo apt-get install build-essential -y
  sudo apt-get install ettercap -y
  sudo apt-get update
  sudo apt-get install ettercap-text-only -y

  # AirCrack-Moduel
  wget http://download.aircrack-ng.org/aircrack-ng-1.1.tar.gz
  tar xfvz aircrack-ng-1.1.tar.gz
  rm cd aircrack-ng-1.1.tar.gz
  rm aircrack-ng-1.1/common.mak
  mv common.mak aircrack-ng-1.1/common.mak
  cd aircrack-ng-1.1
  make
  sudo make install

fi

