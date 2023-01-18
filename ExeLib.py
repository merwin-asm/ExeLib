"""
ExeLib 1.0.0

For getting return and logging from exec and also limit cpu time and ram usage...

Use: from Exelib import exec_

How to return ?? 

     __reexec__ <whatever you want to return>

How to log ??

    __logging__ <whatever you want to log>

How to use auto return ??
    
    exec_("bla bla bla" , auto_return = "<something you want to return , when the program crashes>")

How to access these ??

    rets , logs = exec_("bla bla bla")

How to set cpu time ??
    
    exec_(cmd,cpu_t= <time in seconds>)

How to limit ram usage  ??
    
    exec_(cmd,ram_u= <max-size>)

"""

import random
import json
import time
import os


RETURN_KEY_WORD = "__reexec__" # Can be chnaged if you want a custom return cmd

LOG_KEY_WORD = "__logging__" # Can be chnaged if you want a custom log cmd 


CMDS = """
import atexit
import json
import signal
import resource
import os

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

# checking time limit exceed
def time_exceeded(signo, frame):
    print("ENDED EXEC_")
    raise SystemExit(1)


def set_max_runtime(seconds):
	# setting up the resource limit
	soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
	resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
	signal.signal(signal.SIGXCPU, time_exceeded)


def EXEC_LIB_RETURN_FUN(ret):
    try:
        f = open('.__exec_code__.exec_py','r')
    except:
        f = open('.__exec_code__.exec_py','x')
    try:
        con = json.loads(f.read())
    except:
        con = {}
    f.close()
    try:
        con['return'].append(ret)
    except:
        con['return'] = [ret]
    f = open('.__exec_code__.exec_py','w')
    f.write(json.dumps(con))
    f.close()
def EXEC_LIB_LOG_FUN(log):
    try:
        f = open('.__exec_code__.exec_py','r')
    except:
        f = open('.__exec_code__.exec_py','x')
    try:
        con = json.loads(f.read())
    except:
        con = {}
    f.close()
    log = {"time":time.time(),"txt":log}
    try:
        con['logs'].append(log)
    except:
        con['logs'] = [log]
    f = open('.__exec_code__.exec_py','w')
    f.write(json.dumps(con))
    f.close()
def exit_handler():
    EXEC_LIB_RETURN_FUN(___AUTORET___)
    atexit.register(exit_handler)

"""

def exec_(cmd, auto_return=None,ram_u=None,cpu_t=None,  globals_=None, locals_=None):
    
    CMDS_ = ""

    if ram_u != None:
        CMDS_ += f"\nlimit_memory({ram_u})\n"
    
    if cpu_t != None:
        CMDS_ += f"\nset_max_runtime({cpu_t})\n"
    
    while True:
        EXEC_CODE = str(random.randint(1000000000,99999999999999))
    
        if not os.path.isfile(f".{EXEC_CODE}.exec_py"):
            break
    
    CMDS_ = CMDS.replace("__exec_code__", EXEC_CODE)

    if auto_return == None:
        auto_return = "None"

    CMDS_ = CMDS_.replace("___AUTORET___",auto_return)

    exec_cmd = ""

    cmd = cmd.split(RETURN_KEY_WORD)
    
    i = 0
    
    for cmd_ in cmd:
        if i%2 == 0:
            exec_cmd += cmd_
        else:
            cmd__ = cmd_.split("\n")
            exec_cmd += "EXEC_LIB_RETURN_FUN(" + cmd__[0] + ")\n"
            del cmd__[0]
            for cmd___ in cmd__:
                exec_cmd += cmd___ + "\n"

        i += 1
    
    cmd = exec_cmd
    

    cmd = cmd.split(LOG_KEY_WORD)

    exec_cmd = ""

    i = 0
    
    for cmd_ in cmd:
        if i%2 == 0:
            exec_cmd += cmd_
        else:
            cmd__ = cmd_.split("\n")
            exec_cmd += "EXEC_LIB_LOG_FUN(" + cmd__[0] + ")\n"
            del cmd__[0]
            for cmd___ in cmd__:
                exec_cmd += cmd___ + "\n"
        i += 1
    
    exec_cmd = CMDS_ +  exec_cmd
    
    exec(exec_cmd,globals_,locals_)
    
    if os.path.isfile(f".{EXEC_CODE}.exec_py"):
        exec_file = open(f".{EXEC_CODE}.exec_py", "r") 
        exec_file_con = exec_file.read()
        exec_file.close()
        
        try:
            os.remove(".{EXEC_CODE}.exec_py")
        except:
            pass
        exec_file_con = json.loads(exec_file_con)
        
        try:
            a =  exec_file_con["return"]
        except: 
            a = None

        try:
            b =  exec_file_con["logs"]
        except:
            b = None

        return a , b
    
    else:

        return None , None

if __name__ == "__main__":
    print(exec_("print('Hi')\n__reexec__ 'HI:w'\n__logging__ 'Hi me'"))
