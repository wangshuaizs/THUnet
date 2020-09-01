#!/usr/bin/python
#-*-coding:utf-8 -*-

import time, requests, sys, os, hashlib, subprocess, chardet

def is_net_ok(ping_target):
    p = subprocess.Popen("ping -w 2 " + ping_target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
    (stdoutput, erroutput) = p.communicate();
    encoding = chardet.detect(stdoutput)['encoding'];
    #encoding = 'UTF-8';
    output = stdoutput.decode(encoding);
    retcode = p.returncode;
    res = ("ttl" not in output);
    
    if res:
        #print('Ping failed.');
        return False;
    else:
        #print('Ping success.');
        return True;


def login(username, password):
    data = {
        'action' : 'login',
        'username' : username,
        'password' : '{MD5_HEX}' + hashlib.md5(password.encode()).hexdigest(),
        'ac_id' : '1'
        };

    headers = {
        'Host': 'net.tsinghua.edu.cn',
        'Origin': 'http://net.tsinghua.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://net.tsinghua.edu.cn/wireless/',
        };
    
    response = requests.post('http://net.tsinghua.edu.cn/do_login.php', data=data, headers=headers);
    print(response.text);


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python ./login.py <username> <password>\n");
        os._exit(1);

    username = sys.argv[1];
    password = sys.argv[2];

    while True:
        if not is_net_ok("dl.acm.org"):
            print("\n");
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())));
            print('The network is disconnected.');
            login(username, password)
                
        else:
            time.sleep(1);