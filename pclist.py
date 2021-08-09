# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:11:50 2020

@author: kurinskiyas
"""
import pyad.adquery
import codecs
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
#import re
#import multiprocessing.dummy
#import multiprocessing


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', '-w','100','-4', host]
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE # default
    result = 1
    try:
        result = subprocess.call(command, startupinfo=si)
    except subprocess.CalledProcessError as e:
        print(e.output)
        return 0
    return  result == 0
def ConnectRDP(host):
    process = subprocess.Popen('for /F "usebackq tokens=1,2,3,4,5*" %i in (`qwinsta /server:'+host+' ^| find "Активно"`) do @if "%l" == "Активно" ( echo %k )',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output,error = process.communicate()
    if error == b'':
        d_out = codecs.decode(output,'UTF-8')
        #d_error = codecs.decode(error,'UTF-8')
        #print ("Output:"+d_out)
        #print("Error:"+d_error)
        id=int(d_out)
        subprocess.call('mstsc /v:'+host+' /shadow:'+str(id)+' /noconsentprompt /control')
        #print('mstsc /v:'+host+' /shadow:'+str(id)+' /noconsentprompt /control')
    else:
        return False
    return True
   
def GetDomainComputerList():
    q = pyad.adquery.ADQuery()

    q.execute_query(
    attributes = ['cn','description'],
    where_clause = "objectClass = 'computer'",
    base_dn = "ou=Workstations,ou=Севморнефтегеофизика,ou=Росгеология,ou=RosGeo,dc=rosgeologia,dc=corp"
    )
    res=[[x['cn'],x['description'][0] if x['description'] else ''] for x in q.get_results()]
    return res

if __name__ == "__main__":
    
    print(GetDomainComputerList())
