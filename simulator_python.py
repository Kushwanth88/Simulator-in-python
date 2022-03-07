
import re
import os
import ctypes
class riscV:
    def __init__(self, f):
        file = open(f, 'r')
        fun = os.path.basename(f)
        #read the given file and copy into a string.
        str = file.read()   
        #splitting the string into individual lines.
        str = re.split('\n', str)
        #to remove the white spaces before and after lines.
        str = [i.strip() for i in str]
        self.str = str
        self.fun = fun
    def makefunction(self):
        str = self.str
        fun = self.fun
        def remcom(st):
            s = ''
            for it in st:
                if it == '#':
                    break
                else:
                    s += it
            return s
        #removing the comments from each line in str.
        str = [remcom(it) for it in str]

        rs = range(len(str))
        sd = {}
        for it in rs:
            ip = str[it].split(':')
            if len(ip)==2:
                str[it] = ip[1].strip()
                sd[ip[0].strip()] = it

        def index(st):
            return int(st[-1])

# function used for add instruction.
        def eva(args, *arg):
            args = [index(it) for it in args]
            return arg[args[0]] + arg[args[1]]

# function used for subract instruction.
        def evs(args, *arg):
            args = [index(it) for it in args]
            return arg[args[0]] - arg[args[1]]

#function used for sw instruction.
        def evsw(str):
            s = ''
            flag = 0
            for it in str:
                if it == "(":
                    offset = int(s)
                    s = ''
                else:
                    if it == ")":
                        break
                    else:
                        s += it
                return offset , index(s)
        def function(*arg):
            arg = list(arg)
    #n = number of instructions
            n = len(str)
            pc = 0
    #As every operation takes 4bytes then total n operations take 4*n operations 
    #The condition the loop should end after n operations
            while pc < 4*n:
                st = str[pc//4]
                #to replace , into the empty space
                iter = (' '.join(st.split(','))).split() 
                #the first string is op
                op = iter[0]
                #if op = add or sub perform respective operations
                if op == "add" or op == "sub":
                    ret = index(iter[1])
                    args = iter[2:]
                    if op == "add":
                        pc += 4
                        arg[ret] = eva(args, *arg)
                    else:
                        pc += 4
                        arg[ret] = evs(args, *arg)
                        #if op = bne branch not equals then compare 2nd and third string
                elif op == "bne":
                    rs1, rs2 = index(iter[1]), index(iter[2])
                    flag = (arg[rs1]!=arg[rs2])
                            #if flag is true then check thrid string and go that 
                    if flag:
                        pc = 4*sd[iter[3].strip()]
                    #if flag is false execute next instruction
                    else:
                        pc += 4
                #if op = jal (jump and link)
                elif op == "jal":
                    rt = index(iter[1])
                    arg[rt] = pc + 4
                            #check 3rd string in that line
                    try:
                        pc = int(iter[2])
                    except:
                        pc = 4*sd[iter[2]]
                elif op == "sw":
                    rt = index(iter[1])
                    of, rd = evsw(iter[2])
                    rd = of + arg[rd]
                    arg[rt] = ctypes.cast(rd, ctypes.py_object).value
                elif op == "jalr":
                    rd = index(iter[1])
                    rs, of = index(iter[2]), int(iter[3])
                    arg[rd], pc = pc+4, arg[rs]+of
                else:
                    pc += 4
            return arg[0]



















