ISA = {
    'addrr': 0,
    'addir': 1,
    'addii': 2,
    'subrr': 3,
    'subir': 4,
    'subii': 5,
    'rshr': 6,
    'rshl': 7,
    'lshr': 8,
    'lshl': 9,
    'incr': 10,
    'incl': 11,
    'decr': 12,
    'decl': 13,
    'xorrr': 14,
    'xorlr': 15,
    'xorll': 16,
    'orrr': 17,
    'orlr': 18,
    'orll': 19,
    'andrr': 20,
    'andlr': 21,
    'andll': 22,
    'notr': 23,
    'notl': 24,
    'mov': 25,
    'imm': 26,
    'lodr': 27,
    'lodl': 28,
    'stral': 29,
    'strar': 30,
    'strrl': 31,
    'strrr': 32,

    'brar': 33,
    'bral': 34,

    'brcr': 35,
    'brcl': 36,

    'bncr': 37,
    'bncl': 38,

    'brzr': 39,
    'brzl': 40,

    'bnzr': 41,
    'bnzl': 42,

    'nop': 43,
    'hlt': 44,
    'pshl': 45,
    'pshr': 46,
    'pop': 47,

    'calr': 48,
    'call': 49,

    'ret': 50,

    'sav': 51,
    'rsr': 52,

    'in': 53,
    'outr': 54,
    'outl': 55,

    'mltrr': 60,
    'mltlr': 61,
    'mltll': 62,
    'divrr': 63,
    'divlr': 64,
    'divrl': 65,
    'divll': 66,
    'modrr': 67,
    'modlr': 68,
    'modrl': 69,
    'modll': 70,

    'brllrr': 71,
    'brllrl': 72,
    'brlllr': 73,
    'brlrrr': 74,
    'brlrrl': 75,
    'brlrlr': 76,
    'brglrr': 77,
    'brglrl': 78,
    'brgllr': 79,
    'brgrrr': 80,
    'brgrrl': 81,
    'brgrlr': 82,
    'brelrr': 83,
    'brelrl': 84,
    'brerrr': 85,
    'brerrl': 86,
    'bnelrr': 87,
    'bnelrl': 88,
    'bnerrr': 89,
    'bnerrl': 90,
}

def r(d): return d[0] == 'R' or d[0] == '$'
def n(d): return d.isnumeric() or to_int(d)
def p_(d): return d[0] == '%'
def split(s=''):
    ss = s.splitlines()
    words = []
    for l in ss:
        k=l.split(',')
        for w in k:
            words += w.split()
        words.append('\n')
    return words

def to_int(d=''):
    if d.startswith('0x'): # hex value
        return int(d[2:], 16)
    elif d.startswith('\'') and d.endswith('\'') and d.__len__() == 3:
        return ord(d[1:-1])
    elif d.startswith('0b'):
        return int(d[2:], 2)
    elif d.startswith('.'):
        return d
    else:
        try:
            return int(d)
        except ValueError:
            return False

def tr(d):
    if d.startswith('R') or d.startswith('$'):
        return int(d[1:])-1
    elif d == 'VSP':
        return 0xff-3
    elif d == 'CSP':
        return 0xff-2
    elif d == 'SSP':
        return 0xff-1

class Compiler:
    def __init__(self, code=''):
        self.code = code
        self.tokens = split(code)
        self.cci = -1
        self.cti = 0
        self.labels = {}
        self.output = [0]*(2**16)
    def f(self):
        self.cci += 1
        return self.tokens[self.cci].replace(',', '')
    def p(self,d=0):
        self.output[self.cti] = d
        self.cti += 1
    def co(self):
        d = self.output[::-1]
        i = 0
        try:
            while d[i] == 0:
                i += 1
            self.output = d[i-4:][::-1]
        except IndexError:
            pass
    def po(self):
        nd = []
        for i in self.output:
            if type(i) == str:
                if i.startswith('.'):
                    nd.append(self.labels[i[1:]])
            else:
                nd.append(i)
        self.output = nd
    def c(self):
        inCom = False
        d1 = self.f()
        while True:
            if d1 == '\n':
                inCom = False
            elif inCom:
                pass
            elif d1 == 'MOV':
                d2 = self.f()
                d3 = self.f()
                self.p(ISA['mov'])
                self.p(tr(d3))
                self.p(tr(d2))
            elif d1 == 'IMM':
                d2 = self.f()
                d3 = self.f()
                self.p(ISA['imm'])
                self.p(tr(d2))
                self.p(to_int(d3))
            elif '//' in d1:
                inCom = True
            elif d1 == 'ADD':
                de = self.f()
                d2 = self.f()
                d3 = self.f()
                if r(d2) and r(d3):
                    self.p(ISA['addrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                    self.p(tr(d3))
                elif n(d2) and r(d3):
                    self.p(ISA['addir'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(tr(d3))
                elif n(d2) and n(d3):
                    self.p(ISA['addii'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(to_int(d3))
            elif d1 == 'SUB':
                de = self.f()
                d2 = self.f()
                d3 = self.f()
                if r(d2) and r(d3):
                    self.p(ISA['subrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                    self.p(tr(d3))
                elif n(d2) and r(d3):
                    self.p(ISA['subir'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(tr(d3))
                elif n(d2) and n(d3):
                    self.p(ISA['subii'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(to_int(d3))
            elif d1 == 'DW':
                d = self.f()
                if n(d):
                    self.p(to_int(d))
            elif d1 == 'RSH':
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['rshr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                elif n(d2):
                    self.p(ISA['rshl'])
                    self.p(tr(de))
                    self.p(to_int(d2))
            elif d1 == 'LSH':
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['lshr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                elif n(d2):
                    self.p(ISA['lshl'])
                    self.p(tr(de))
                    self.p(to_int(d2))
            elif d1 == 'INC':
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['incr'])
                    self.p(tr(de))
                    self.p(tr(d2))
            elif d1 == 'DEC':
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['decr'])
                    self.p(tr(de))
                    self.p(tr(d2))
            elif d1 == 'XOR':
                de = self.f()
                d2 = self.f()
                d3 = self.f()
                if r(d2) and r(d3):
                    self.p(ISA['xorrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                    self.p(tr(d3))
                elif n(d2) and r(d3):
                    self.p(ISA['xorlr'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(tr(d3))
                elif n(d2) and n(d3):
                    self.p(ISA['xorll'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(to_int(d3))
            elif d1 == 'OR':
                de = self.f()
                d2 = self.f()
                d3 = self.f()
                if r(d2) and r(d3):
                    self.p(ISA['orrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                    self.p(tr(d3))
                elif n(d2) and r(d3):
                    self.p(ISA['orlr'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(tr(d3))
                elif n(d2) and n(d3):
                    self.p(ISA['orll'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(to_int(d3))
            elif d1 == 'AND':
                de = self.f()
                d2 = self.f()
                d3 = self.f()
                if r(d2) and r(d3):
                    self.p(ISA['andrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                    self.p(tr(d3))
                elif n(d2) and r(d3):
                    self.p(ISA['andlr'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(tr(d3))
                elif n(d2) and n(d3):
                    self.p(ISA['andll'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                    self.p(to_int(d3))
            elif d1 == 'NOT':
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['notr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                elif n(d2):
                    self.p(ISA['notl'])
                    self.p(tr(de))
                    self.p(to_int(d2))
            elif d1 == "LOD":
                de = self.f()
                d2 = self.f()
                if r(d2):
                    self.p(ISA['lodr'])
                    self.p(tr(de))
                    self.p(tr(d2))
                elif n(d2):
                    self.p(ISA['lodl'])
                    self.p(tr(de))
                    self.p(to_int(d2))
            elif d1 == "STR":
                de = self.f()
                d2 = self.f()
                if n(de) and n(d2):
                    self.p(ISA['stral'])
                    self.p(to_int(de))
                    self.p(to_int(d2))
                elif n(de) and r(d2):
                    self.p(ISA['strar'])
                    self.p(to_int(de))
                    self.p(tr(d2))
                elif r(de) and n(d2):
                    self.p(ISA['strrl'])
                    self.p(tr(de))
                    self.p(to_int(d2))
                elif r(de) and r(d2):
                    self.p(ISA['strrr'])
                    self.p(tr(de))
                    self.p(tr(d2))
            elif d1 == 'NOP':
                self.p(ISA['nop'])
            elif d1 == 'HLT':
                self.p(ISA['hlt'])
            elif d1.startswith('.'):
                self.labels[d1[1:]] = self.cti
            elif d1.startswith('B') and d1.lower()+'l' in ISA:
                l = self.f()
                if l.startswith('.'):
                    self.p(ISA[d1.lower()+'l'])
                    self.p(l)
            elif d1 == '@org':
                o = self.f()
                self.cti = int(o)
            elif d1 == 'PSH':
                d = self.f()
                if n(d):
                    self.p(ISA['pshl'])
                    self.p(to_int(d))
                elif r(d):
                    self.p(ISA['pshr'])
                    self.p(tr(d))
            elif d1 == 'POP':
                d = self.f()
                if r(d):
                    self.p(ISA['pop'])
                    self.p(tr(d))
            elif d1 == 'CAL':
                l = self.f()
                if l.startswith('.'):
                    self.p(ISA['call'])
                    self.p(l)
            elif d1 == 'RET':
                self.p(ISA['ret'])
            elif d1 == 'SAV':
                d = self.f()
                if r(d):
                    self.p(ISA['sav'])
                    self.p(tr(d))
            elif d1 == 'RSR':
                d = self.f()
                if r(d):
                    self.p(ISA['rsr'])
                    self.p(tr(d))
            elif d1 == 'IN':
                d = self.f()
                p = self.f()
                if p_(p) and r(d):
                    self.p(ISA['in'])
                    self.p(tr(d))
                    self.p(int(p[1:])-1)
            elif d1 == 'OUT':
                p = self.f()
                d = self.f()
                if p_(p) and r(d):
                    self.p(ISA['outr'])
                    self.p(int(p[1:])-1)
                    self.p(tr(d))
                elif p_(p) and n(d):
                    self.p(ISA['outl'])
                    self.p(int(p[1:])-1)
                    self.p(to_int(d))
            elif d1 == 'BRE':
                d = self.f()
                c1 = self.f()
                c2 = self.f()
                if r(c1) and r(c2):
                    self.p(ISA['brelrr'])
                    self.p(d)
                    self.p(tr(c1))
                    self.p(tr(c2))
                elif r(c1) and n(c2):
                    self.p(ISA['brelrl'])
                    self.p(d)
                    self.p(tr(c1))
                    self.p(to_int(c2))
            
            try:
                d1 = self.f()
            except IndexError:
                self.co()
                self.po()
                return self.output
import sys 
d2 = open(sys.argv[1], 'r').read()
d = Compiler(d2)
i = d.c()
print(i)
n = []
for d_ in i:
    n.append(d_&0xff)
    n.append((d_ >> 8) & 0xff)
    
print(n)
open(sys.argv[2], 'wb').write(bytearray(n))