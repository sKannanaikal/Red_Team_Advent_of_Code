import socket
import argparse
from tabnanny import verbose
from scapy.all import *
import random
import sys

ports = range(2320, 2325)
count = 0

def os_detection(host):
    ping = IP(dst=host)/ICMP()
    icmp_response = sr1(ping, verbose=0)
    ttl = icmp_response.getlayer(IP).ttl
    if ttl == 128:
        print('[+] Windows Host Detected!')
    elif ttl == 64:
        print('[+] Linux/Unix Host Detected')
    else:
        print('[-] Host Operating System Unknown')

def banner_grab(connection):
    connection.settimeout(5)
    banner = connection.recv(1024)
    print(banner.decode())

def collect_ipid(zombie):
    synack_packet = sr1(IP(dst=zombie)/TCP(sport=4534, dport=80, flags="SA"))
    ipid = synack_packet.getlayer(IP).id
    return int(ipid)


def zombie_scan(target, zombie):
    """
        1. Grab IP ID from zombie
        2. Send forged syn
        3. Grab and analyze IP ID from zombie
    """
    for port in ports:
        initial_ipid = collect_ipid(zombie=zombie)
        synack_packet = sr1(IP(dst=target, src=zombie)/TCP(sport=3483, dport=port))
        post_ipid = collect_ipid(zombie=zombie)

        if(initial_ipid + 2 == post_ipid):
            print('[+] Port: {port} is open on {host}'.format(port=port, host=target))

def standard_scan(host):
    global ports
    global count
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in ports:
            result = connection.connect_ex((host, port))
            if result == 0:
                print('[+] Port: {port} is open on {host}'.format(port=port, host=host))
                banner_grab(connection=connection)
                connection.close()
                count += 1
    except socket.error as error:
        print(error)
        sys.exit(-1)

def syn_stealth_scan(host):
    global count
    global ports
    for port in ports:
        source = 7493
        stealth_packet = sr1(IP(dst=host)/TCP(sport = source, dport = port, flags = "S"), verbose=0)
        recv_flags = stealth_packet.getlayer(TCP).flags
        if(recv_flags == 0x12):
            print('[+] Port: {port} is open on {host}'.format(port=port, host=host))
            count += 1
        reset_packet = IP(dst=host)/TCP(sport = source, dport = port, flags = "R")
        send(reset_packet, verbose=False)

def fin_scan(host):
    global count
    global ports
    for port in ports:
        source = 7493
        stealth_packet = sr1(IP(dst=host)/TCP(sport = source, dport = port, flags = "F"))
        recv_flags = stealth_packet.getlayer(TCP).flags
        if(recv_flags == 0x14):
            continue
        else:
            print('[+] Port: {port} is open on {host}'.format(port=port, host=host))
            count += 1

def xmas_scan(host):
    global count
    global ports
    for port in ports:
        source = 7493
        stealth_packet = sr1(IP(dst=host)/TCP(sport = source, dport = port, flags = "FPU"))
        recv_flags = stealth_packet.getlayer(TCP).flags
        if(recv_flags == 0x14):
            continue
        else:
            print('[+] Port: {port} is open on {host}'.format(port=port, host=host))
            count += 1

def main():

    print(
    """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⠖⠚⢉⣩⣭⡭⠛⠓⠲⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⡴⠋⠁⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢦⡀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⠃⢀⡴⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣆⠀⠀⠀
    ⠀⠀⠀⠀⡾⠁⣠⠋⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⠀
    ⠀⠀⠀⣸⠁⢰⠃⠀⠀⠀⠈⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀
    ⠀⠀⠀⡇⠀⡾⡀⠀⠀⠀⠀⣀⣹⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀
    ⠀⠀⢸⠃⢀⣇⡈⠀⠀⠀⠀⠀⠀⢀⡑⢄⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
    ⠀⠀⢸⠀⢻⡟⡻⢶⡆⠀⠀⠀⠀⡼⠟⡳⢿⣦⡑⢄⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
    ⠀⠀⣸⠀⢸⠃⡇⢀⠇⠀⠀⠀⠀⠀⡼⠀⠀⠈⣿⡗⠂⠀⠀⠀⠀⠀⠀⠀⢸⠁
    ⠀⠀⡏⠀⣼⠀⢳⠊⠀⠀⠀⠀⠀⠀⠱⣀⣀⠔⣸⠁⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀
    ⠀⠀⡇⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀
    ⠀⢸⠃⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⢀⠀⠀⠀⠀⠀⣾⠀⠀
    ⠀⣸⠀⠀⠹⡄⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠸⠀⠀⠀⠀⠀⡇⠀⠀
    ⠀⡏⠀⠀⠀⠙⣆⠀⠀⠀⠀⠀⠀⠀⢀⣠⢶⡇⠀⠀⢰⡀⠀⠀⠀⠀⠀⡇⠀⠀
    ⢰⠇⡄⠀⠀⠀⡿⢣⣀⣀⣀⡤⠴⡞⠉⠀⢸⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣧⠀⠀
    ⣸⠀⡇⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⢹⠀⠀⢸⠀⠀⢀⣿⠇⠀⠀⠀⠁⠀⢸⠀⠀
    ⣿⠀⡇⠀⠀⠀⠀⠀⢀⡤⠤⠶⠶⠾⠤⠄⢸⠀⡀⠸⣿⣀⠀⠀⠀⠀⠀⠈⣇⠀
    ⡇⠀⡇⠀⠀⡀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠸⡌⣵⡀⢳⡇⠀⠀⠀⠀⠀⠀⢹⡀
    ⡇⠀⠇⠀⠀⡇⡸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠮⢧⣀⣻⢂⠀⠀⠀⠀⠀⠀⢧
    ⣇⠀⢠⠀⠀⢳⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡎⣆⠀⠀⠀⠀⠀⠘
    ⢻⠀⠈⠰⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠘⢮⣧⡀⠀⠀⠀⠀
    ⠸⡆⠀⠀⠇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠆⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⡀⢢⡀
    """)

    global count

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True, help='The target of the port scan')
    parser.add_argument('--scan', type=str, required=True, help= 'Specify scan type Default(D), Stealth(S), Fin(F), Xmas(X) Zombie(Z)')
    parser.add_argument('--os', required=False, help='Specify wheter or not Host detection is necessary (y/n)')
    parser.add_argument('--zombie', required=False, help='Specify the zombie machine when conducting an idle/zombie scan')
    arguments = parser.parse_args()

    host = arguments.host
    scan_type = arguments.scan
    os_scan = arguments.os

    #Figure this out don't printout unless os in arguments
    if(os_scan == "y" or os_scan == "Y"):
        print('[+] OS Detection Selected')
        os_detection(host=host)

    if(scan_type.upper() == "D"):
        print('[+] Default Scan Chosen!')
        standard_scan(host)
    elif(scan_type.upper() == "S"):
        print('[+] Stealth Scan Chosen!')
        syn_stealth_scan(host)
    elif(scan_type.upper() == "F"):
        print('[+] Fin Scan Chosen!')
        fin_scan(host)
    elif(scan_type.upper() == "X"):
        print('[+] Xmas Scan Chosen!')
        xmas_scan(host)
    elif(scan_type.upper() == "Z"):
        print('[+] Idle Scan Chosen!')
        zombie = arguments.zombie
        if(zombie == "" or zombie == None):
            print('[-] Zombie machine not specified exiting')
            sys.exit(-1)
        zombie_scan(host, zombie)
    else:
        print('[-] Invalid Scan Type Program Exitting!')
        sys.exit(-1)

    print('[+] A total of {count} port(s) were open'.format(count=count))

    print('[+] Scan Completed!')

if __name__ == '__main__':
    main()