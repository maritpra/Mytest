#/usr/bin/python3

import json
import socket
import subprocess
from scapy.all import IP, ICMP, sr1

def test_tcp_port(host, port):
    """Test if a specific TCP port is open."""
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"TCP Port {port} on {host} is OPEN.")
    except socket.timeout:
        print(f"TCP Port {port} on {host} is BLOCKED or CLOSED (Timeout).")
    except ConnectionRefusedError:
        print(f"TCP Port {port} on {host} is BLOCKED or CLOSED (Connection Refused).")
    except Exception as e:
        print(f"Error testing TCP Port {port} on {host}: {e}")

def test_udp_port(host, port):
    """Test if a specific UDP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)
            message = b"Test UDP Packet"
            sock.sendto(message, (host, port))
            sock.recvfrom(1024)  # Expecting a response
            print(f"UDP Port {port} on {host} is OPEN.")
    except socket.timeout:
        print(f"UDP Port {port} on {host} is BLOCKED or CLOSED (Timeout).")
    except Exception as e:
        print(f"Error testing UDP Port {port}: {e}")

def test_icmp(host):
    """Test if ICMP (ping) is allowed to a host."""
    try:
        packet = IP(dst=host)/ICMP()
        response = sr1(packet, timeout=2, verbose=0)
        if response:
            print(f"ICMP Ping to {host} is ALLOWED.")
        else:
            print(f"ICMP Ping to {host} is BLOCKED or UNREACHABLE (Timeout).")
    except Exception as e:
        print(f"Error testing ICMP Ping to {host}: {e}")

def test_icmp_with_ping(host):
    try:
        result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"ICMP Ping to {host} is ALLOWED.")
        else:
            print(f"ICMP Ping to {host} is BLOCKED or UNREACHABLE.")
    except Exception as e:
        print(f"Error testing ICMP Ping to {host}: {e}")

def test_hosts_with_protocols(test_list):
    """Test hosts with specified protocols."""
    for test in test_list:
        host = test["host"]
        protocol = test["protocol"]
        port = test.get("port")  # Port may not be applicable for ICMP
        
        print(f"Testing Host: {host}, Protocol: {protocol}")
        if protocol.lower() == "icmp":
            print(f"  Testing ICMP Ping to {host}...")
            test_icmp_with_ping(host)
        elif protocol.lower() == "tcp" and port is not None:
            print(f"  Testing TCP Port {port}...")
            test_tcp_port(host, port)
        elif protocol.lower() == "udp" and port is not None:
            print(f"  Testing UDP Port {port}...")
            test_udp_port(host, port)
        else:
            print(f"  Invalid test configuration: {test}")
        print("=" * 50)

# Load the list from JSON file
with open("test_ip_port.json", "r") as file:
    tests_to_run = json.load(file)

# Perform tests
test_hosts_with_protocols(tests_to_run)