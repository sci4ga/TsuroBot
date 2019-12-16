import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print("IP is " + str(IP))
    return IP


def scan(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex((addr, port))
    if result == 0:
        try:
            name, alias, iplist = socket.gethostbyaddr(addr)
            return name
        except Exception:
            return True
    else:
        return 0


def run1():
    net = get_ip()
    net1 = net.split('.')
    a = '.'

    net2 = net1[0] + a + net1[1] + a + net1[2] + a
    st1 = 1
    en1 = 254
    found = {}

    print("Scanning started")

    for ip in range(st1, en1 + 1):
        addr = net2 + str(ip)
        result = scan(addr, 80)
        if (result):
            print(str(addr) + " is live")
            found[addr] = result
        else:
            print(str(addr) + " is not found")

    print("Scanning completed")
    print(str(found))


run1()
