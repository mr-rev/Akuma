from subprocess import Popen,PIPE

def execute(cmd_list):
    proc=Popen(cmd_list,shell=True,stdout=PIPE,stderr=PIPE,encoding="utf-8",errors="replace")
    out,err=proc.communicate()
    if(proc.returncode==0):return ["\n"+out]
    else:return ["\n[!] "+err,None]