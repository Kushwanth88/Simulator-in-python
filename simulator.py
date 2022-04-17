import re
from threading import *
import ctypes
def data(ins):
    if ins == '\n':
        return None
    var, indv, indf, frmt, pc  = '', 1, 0, '', 0 
    for ch in ins:
        if ch == ":":
            indv = 0
        if indv:
             var += ch
        if ch == ".":
            indf = 1
        if indf == 1:
            if ch == " ":
                indf = 0
                break
            else:
                frmt += ch
        pc += 1
    end = pc
    while 1:
        i = ins[end]
        end += 1
        if i == '#' or i == "\n":
            break 
    exec('{} = {}'.format('globals()[var]', ins[pc:end]))
    if len(globals()[var]) != 1:
        a = list(globals()[var])
        try:
            b = ''
            for it in a:
                b += it
            if len(a[0]) == 1:
                globals()[var] = b
            else:
                globals()[var] = a
        except:
            globals()[var] = a
def address(st):
    st = st.replace(')', '')
    a = st.split('(')
    return int(a[0]) + registers[a[1]]
registers = {}
console = []
cs = 0
class fetch(Thread):
    def run(self):
        global ir
        try:
            ir = instrs[pc]
        except:
            return None
class decode(Thread):
    def run(self):
        global clu
        if clu == None:
            return None
        clu = clu.replace(', ', ',')
        clu = clu.split('#')[0].strip()
        clu = re.split(',| ', clu)
        if clu[0] == 'j':
            pc = sd[clu[1]] - 1
            clu, ex = None, None
class execute(Thread):
    def run(self):
        global halt, ex
        if ex == None:
            return ex
        if len(ex) > 1:
            if  ex[1] == '$a0':
                console.append(globals()[ex[2]])
        if ex[0] == 'syscall':
            global cs
            print(console[cs], end = '')
            cs += 1
        if ex[0] == 'li':
            registers[ex[1]] = int(ex[2])
        elif ex[0] == 'la':
            registers[ex[1]] = id(globals()[ex[2]])
        elif ex[0] == 'addi':
            registers[ex[1]] = registers[ex[2]] + int(ex[3])
        elif ex[0] == 'bne':
            if registers[ex[1]] != registers[ex[2]]:
                pc = sd[ex[3]] - 1
                ex, clu = None, None
        elif ex[0] == 'beq':
            if registers[ex[1]] == registers[ex[2]]:
                pc = sd[ex[3]] - 1
                ex, clu = None, None
        elif ex[0] == 'subi':
            registers[ex[1]] = registers[ex[2]] - int(ex[3])
        elif ex[0] == 'sub':
            registers[ex[1]] = registers[ex[2]] - registers[ex[3]]
        elif ex[0] == 'sw':
            ads = address(ex[2])
            print(ads)
            val = (ctypes.c_int).from_address(ads)
            val = registers[ex[1]]
        elif ex[0] == 'lw':
            ads = address(ex[2])
            registers[ex[1]] = ctypes.cast(ads, ctypes.py_object).value
        elif ex[0] == 'jal':
            registers[ex[1]] = pc+1
            try:
                pc = (int(registers[ex[2]])//4)
            except:
                pc = sd[ex[2]]
            pc -= 1
            ex, clu = None, None     
        elif ex[0] == 'jalr':
            registers[ex[1]], pc = pc+1, (registers[ex[2]]+int(ex[3]))//4
            pc -= 1
            ex, clu = None, None
        elif ex[0] == 'sll':
            registers[ex[1]] = registers[ex[2]]*int(ex[3])
        elif ex[0] == 'move':
            registers[ex[1]] = registers[ex[2]]
        elif ex[0] == 'slt':
            registers[ex[1]] = registers[ex[2]] < registers[ex[3]]
class riscV:
    def __init__(self, file_path):
        file = open(file_path, 'r')
        self.file = file
    def exec(self):
        global sd, instrs, clu, ex, halt, pc
        pc, clu, ex, halt, sd = 0, None, None, 0, {}
        file = self.file
        while 1:
            str = file.readline()
            str.strip()
            if str == '.text\n':
                break
            elif str == '.data\n':
                continue
            else:
                data(str)
        str = file.readlines()
        pd = 0
        instrs = []
        for it in str:
            st = it.split(':')
            if len(st) == 2:
                sd[st[0]] = pd
                if st[1] != '\n':
                    instrs.append(st[1])
                    pd += 1
            elif it != '\n':
                instrs.append(it)
                pd += 1
        n = len(instrs)
        while pc<n:
            if halt:
                break
            t1 = fetch()
            t2 = decode()
            t3 = execute()
            t1.start()
            t2.start()
            t3.start()
            ex, clu = clu, ir
            pc += 1
obj = riscV('label.txt')
obj.exec()
print(registers)