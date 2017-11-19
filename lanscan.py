#Cross-Platform Network Scanner v1.0 by HcH
#Network scanner based on system ping and TCP scanning, tested on Windows/Raspbian

#returning the system/OS name can be done using platform
from platform import system as system_name
#for executing shell commands we import system
from os import system as system_call
#for gethostname function we need socket
import socket

#get the range of the scan based off the host ip address that's able to communicate to the internet
#it returns a join with rpartition, it splits the string at the last occurrence of the argument string so the last octet of the ipv4 address is removed
def get_scanrange():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return ''.join(s.getsockname()[0].rpartition('.')[:2])

#a scanrange will look like 10.0.0. , the for loop will fill in 1-254 for us at the last octet of the ipv4 address
network = str(get_scanrange())

#ping as system call function, for windows and linux!
def ping(host):
    #ping parameters depending on OS
    parameters = "-n 1 -w 3" if system_name().lower()=="windows" else "-c 1"
    #the ping command itself
    return system_call("ping " + parameters + " " + host + ">NUL") == 0

#scannerplugin example, tries to connect to webservers
def http(ipaddr):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.3)
    if not s.connect_ex((ipaddr,80)):
        s.close()                      
        return 1
    else:
        s.close()

#scannerplugin example, tries to connect to ftpservers
def ftp(ipaddr):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.3)
    if not s.connect_ex((ipaddr,21)):
        s.close()                      
        return 1
    else:
        s.close()

#scannerplugin example, tries to connect to telnetservers
def telnet(ipaddr):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.3)
    if not s.connect_ex((ipaddr,23)):
        s.close()                      
        return 1
    else:
        s.close()

#to obtain getfqdn function we now import from socket:
from socket import *

def run():
    print ''
    #ping addresses <network>.1 to <network>.254
    for ip in xrange(1,254):
        ipaddr = network + str(ip)
        #the function 'getfqdn' returns the remote hostname, add it easily to a 1 line output
        if ping(ipaddr):
            print '%s \t ::: \t PING  \t ::: \t %s' %(ipaddr, getfqdn(ipaddr))
        if ftp(ipaddr):
            print '%s \t ::: \t FTP   \t ::: \t %s' %(ipaddr, getfqdn(ipaddr))
        if telnet(ipaddr):
            print '%s \t ::: \t TNET  \t ::: \t %s' %(ipaddr, getfqdn(ipaddr))
        if http(ipaddr):
            print '%s \t ::: \t HTTP  \t ::: \t %s' %(ipaddr, getfqdn(ipaddr))

#here's the main:
if __name__ == '__main__':
    print '\n' + 'Cross-Platform Network Scanner v1.0' + '\n' + '\n' + 'Scanning ' + network + '1-254 ...'
    run()
    raw_input('\n' + 'Done')
