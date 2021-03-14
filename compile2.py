import sys
def split(s):
    d = []
    n = ''
    for c in s:
        if c == ' ':
            if n != '':
                d.append(n)
            n = ''
        elif c == '(':
            if n != '':
                d.append(n)
            d.append('(')
            n = ''
        elif c == ')':
            if n != '':
                d.append(n)
            d.append(')')
            n = ''
        elif c == '\n':
            if n != '':
                d.append(n)
            d.append(c)
            n = ''
        elif c == '\t':
            if n != '':
                d.append(n)
            n = ''
        elif c == ';':
            if n != '':
                d.append(n)
            d.append(c)
            n = ''
        elif c == '{' or c == '}':
            if n != '':
                d.append(n)
            d.append(c)
            n = ''
        elif c == ',':
            if n != '':
                d.append(n)
            n = ''
        elif c == '+':
            if n == '+':
                d.append('++')
                n = ''
            elif n == '':
                n = '+'
            else:
                d.append(n)
                n = '+'
        elif c == '-':
            if n == '-':
                d.append('--')
                n = ''
            elif n == '':
                n = '-'
            else:
                d.append(n)
                n = '-'
        elif c == '=':
            if n == '-' or n == '+' or n == '=':
                d.append(f'{n}=')
                n = ''
            elif n == '':
                n = c
            else:
                d.append(n)
                n = c
        elif c in OPS:
            if n == '':
                n = c
            else:
                d.append(n)
                n = c
        elif c.isnumeric():
            if n in OPS:
                d.append(n)
                n = c
            elif n == '':
                n = c
            elif not n.isnumeric():
                n += c
            else:
                n += c
        elif c == '.':
            if n != '':
                d.append(n)
            d.append('.')
            n = ''
        else:
            if n in OPS:
                d.append(n)
                n =''
            n += c
    if n != '':
        d.append(n)
    return d

parse_util = {
    "+_I_I":lambda x, y: f'ADD R1, {x}, {y}',
    "+_V_I":lambda x, y: f'LOD R1, {x}\nADD R1, R1, {y}',
    "+_I_V":lambda x, y: f'LOD R1, {y}\nADD R1, R1, {x}',
    "+_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nADD R1, R1, R2',
    "-_I_I":lambda x, y: f'SUB R1, {x}, {y}',
    "-_V_I":lambda x, y: f'LOD R1, {x}\nSUB R1, R1, {y}',
    "-_I_V":lambda x, y: f'LOD R1, {y}\nSUB R1, R1, {x}',
    "-_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nSUB R1, R1, R2',
    "/_I_I":lambda x, y: f'DIV R1, {x}, {y}',
    "/_V_I":lambda x, y: f'LOD R1, {x}\nDIV R1, R1, {y}',
    "/_I_V":lambda x, y: f'LOD R1, {y}\nDIV R1, R1, {x}',
    "/_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nDIV R1, R1, R2',
    "*_I_I":lambda x, y: f'MLT R1, {x}, {y}',
    "*_V_I":lambda x, y: f'LOD R1, {x}\nMLT R1, R1, {y}',
    "*_I_V":lambda x, y: f'LOD R1, {y}\nMLT R1, R1, {x}',
    "*_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nMLT R1, R1, R2',
    "^_I_I":lambda x, y: f'XOR R1, {x}, {y}',
    "^_V_I":lambda x, y: f'LOD R1, {x}\nXOR R1, R1, {y}',
    "^_I_V":lambda x, y: f'LOD R1, {y}\nXOR R1, R1, {x}',
    "^_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nXOR R1, R1, R2',
    "&_I_I":lambda x, y: f'AND R1, {x}, {y}',
    "&_V_I":lambda x, y: f'LOD R1, {x}\nAND R1, R1, {y}',
    "&_I_V":lambda x, y: f'LOD R1, {y}\nAND R1, R1, {x}',
    "&_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nAND R1, R1, R2',
    "|_I_I":lambda x, y: f'OR R1, {x}, {y}',
    "|_V_I":lambda x, y: f'LOD R1, {x}\nOR R1, R1, {y}',
    "|_I_V":lambda x, y: f'LOD R1, {y}\nOR R1, R1, {x}',
    "|_V_V":lambda x, y: f'LOD R1, {x}\nLOD R2, {y}\nOR R1, R1, R2',

    "+_P_I":lambda x: f'ADD R1, R1, {x}',
    "+_P_V":lambda x: f'LOD R2, {x}\nADD R1, R1, R2',
    "-_P_I":lambda x: f'SUB R1, R1, {x}',
    "-_P_V":lambda x: f'LOD R2, {x}\nSUB R1, R1, R2',
    "/_P_I":lambda x: f'DIV R1, R1, {x}',
    "/_P_V":lambda x: f'LOD R2, {x}\nDIV R1, R1, R2',
    "*_P_I":lambda x: f'MLT R1, R1, {x}',
    "*_P_V":lambda x: f'LOD R2, {x}\nMLT R1, R1, R2',
    "^_P_I":lambda x: f'XOR R1, R1, {x}',
    "^_P_V":lambda x: f'LOD R2, {x}\nXOR R1, R1, R2',
    "&_P_I":lambda x: f'AND R1, R1, {x}',
    "&_P_V":lambda x: f'LOD R2, {x}\nAND R1, R1, R2',
    "|_P_I":lambda x: f'OR R1, R1, {x}',
    "|_P_V":lambda x: f'LOD R2, {x}\nOR R1, R1, R2',

    "+_P_P":lambda: f'POP R2\nADD R1, R1, R2',
    "-_P_P":lambda: f'POP R2\nSUB R1, R1, R2',
    "/_P_P":lambda: f'POP R2\nDIV R1, R1, R2',
    "*_P_P":lambda: f'POP R2\nMLT R1, R1, R2',
    "^_P_P":lambda: f'POP R2\nXOR R1, R1, R2',
    "&_P_P":lambda: f'POP R2\nAND R1, R1, R2',
    "|_P_P":lambda: f'POP R2\nOR R1, R1, R2',

}

OPS = ['+','-','/','*','==','!=','^','&','|']

def tk(d, t):
    return [d, t]

def parse_exp(d=[]):
    o = []
    os= []
    i = 0
    while True:
        print('PARSE_EXP',o, os)
        if d[i] in OPS:
            os.append(d[i])
        elif d[i] == '(':
            os.append(d[i])
        elif d[i] == ')':
            while os[::-1][0] != '(':
                try:
                    o.append(os.pop())
                except IndexError:
                    return o
        elif d[i].isnumeric() or d[i].isascii():
            o.append(d[i])
        i += 1
        try:
            d[i]
        except IndexError:
            while os != []:
                o.append(os.pop())
            no = []
            for i in range(len(o)):
                if not o[i] == '(':
                   no.append(o[i]) 
            return no
    return o
            

def parse_rpn(d):
    i = 0
    o = []
    wp = False
    while True:
        d1 = d[i]
        print('PARSE_RPN',d1)
        if not d1 in OPS:
            d2 = d[i+1]
            if not d2 in OPS:
                op = d[i+2]
                if op in OPS:
                    if wp:
                        o.append(tk('SAV', []))
                    o.append(tk(f'{op}_{"I" if d1.isnumeric() else "V"}_{"I" if d2.isnumeric() else "V"}', [d1,d2]))
                    
                    #o.append(tk('SAV', []))
                    wp = True
                    i += 3
            elif d2 in OPS:
                o.append(tk(f'{d2}_P_{"I" if d1.isnumeric() else "V"}', [d1]))
                i+=2
        elif d1 in OPS:
            o.append(tk(f'{d1}_P_P', []))
            i+=1
        try:
            d[i]
        except IndexError:
            return o
    return o

def _parse_full_expression_(exp, vars_):
    _d = parse_exp(split(exp))
    _d2 = parse_rpn(_d)
    print(_d2)
    o = ''
    for o_ in _d2:
        if o_[0].endswith('_I_I'):
            #print('e', o_)
            d1 = parse_util[o_[0]](o_[1][0], o_[1][1])
            #print(d1)
            o+=(d1)+'\n'
        elif o_[0].endswith('_V_I'):
            d1 = parse_util[o_[0]](vars_[o_[1][0]][1], o_[1][1])
            o+=(d1)+'\n'
        elif o_[0].endswith('_I_V'):
            d1 = parse_util[o_[0]]( o_[1][0], vars_[o_[1][1]][1])
            o+=(d1)+'\n'
        elif o_[0].endswith('_V_V'):
            d1 = parse_util[o_[0]](  vars_[o_[1][0]][1],  vars_[o_[1][1]][1] )
            o+=(d1)+'\n'
        
        elif o_[0].endswith('_P_I'):
            d1 = parse_util[o_[0]](o_[1][0])
            o+=(d1)+'\n'
        elif o_[0].endswith('_P_V'):
            d1 = parse_util[o_[0]](vars_[o_[1][0]][1])
            o+=(d1)+'\n'
        elif o_[0].endswith('_P_P'):
            d1 = parse_util[o_[0]]()
            o+=(d1)+'\n'
        elif o_[0] == 'SAV':
            o+=('PSH R1')+'\n'
    return o
class Compiler:
    def __init__(self, code):
        self.tokens = split(code)
        self.output = 'CAL .main\nHLT\n'
        self.cti = -1
        self.vf = 0x200
        self.cci = 0
        self.vars = {}
        self.cf = []
        self.structs = {}
    def f(self):
        self.cti += 1
        return self.tokens[self.cti]
    def p(self, d):
        self.output += d + '\n'
    def c(self):
        while True:
            try:
                d = self.f()
            except IndexError:
                #print(self.output)
                return self.output, self.vars, self.structs
            if d == 'int':
                # Int variable define
                vn = self.f()
                if vn.isascii() and not vn == '*':
                    eqs = self.f()
                    if eqs == '=':
                        __d = ''
                        while True:
                            d2 = self.f()
                            print(d2, __d)
                            if d2 != ';':
                                __d += d2
                            else:
                                break
                        __d_ = split(__d)
                        print('C_C1',__d_, __d)
                        if __d_[0].isascii() and not __d_[0].isnumeric() and (not __d_[0] in OPS+['(',')']) and __d_[::-1][0] == ')':
                            # function call
                            self.vars[vn] = ['int', self.vf]
                            d___ = self.f()
                            if d___ == '(':
                                d___ = self.f()
                                while d___ != ')':
                                    if d___.isnumeric():
                                        self.p(f'PSH {d___}')
                                    elif len(split(d___)) == 1:
                                        self.p(f'LOD R1, {self.vars[d___][1]}')
                                        self.p(f'PSH R1')    
                            self.p(f'CAL .{__d_[0]}')
                            self.p(f'STR {self.vf}, R1')
                            self.vf += 1
                        elif __d_.__len__() == 1:
                            if __d.isnumeric():
                                self.vars[vn] = ['int', self.vf]
                                self.p(f'STR {self.vf}, {__d}')
                                self.vf += 1
                            else:
                                self.vars[vn] = ['int', self.vf]
                                self.p(f'LOD R1, {self.vars[__d][1]}')
                                self.p(f'STR {self.vf}, R1')
                                self.vf += 1
                        else:
                            _d = parse_exp(__d_)
                            _d2 = parse_rpn(_d)
                            print('C_C2',_d2)
                            for o_ in _d2:
                                if o_[0].endswith('_I_I'):
                                    #print('e', o_)
                                    d1 = parse_util[o_[0]](o_[1][0], o_[1][1])
                                    #print(d1)
                                    self.p(d1)
                                elif o_[0].endswith('_V_I'):
                                    d1 = parse_util[o_[0]](self.vars[o_[1][0]][1], o_[1][1])
                                    self.p(d1)
                                elif o_[0].endswith('_I_V'):
                                    d1 = parse_util[o_[0]]( o_[1][0], self.vars[o_[1][1]][1])
                                    self.p(d1)
                                elif o_[0].endswith('_V_V'):
                                    d1 = parse_util[o_[0]](  self.vars[o_[1][0]][1],  self.vars[o_[1][1]][1] )
                                    self.p(d1)
                                
                                elif o_[0].endswith('_P_I'):
                                    d1 = parse_util[o_[0]](o_[1][0])
                                    self.p(d1)
                                elif o_[0].endswith('_P_V'):
                                    d1 = parse_util[o_[0]](self.vars[o_[1][0]][1])
                                    self.p(d1)
                                elif o_[0].endswith('_P_P'):
                                    d1 = parse_util[o_[0]]()
                                    self.p(d1)
                                elif o_[0] == 'SAV':
                                    self.p('PSH R1')
                            self.vars[vn] = ['int', self.vf]
                            self.p(f'STR {self.vf}, R1')
                            self.vf += 1
                    elif eqs == '(':
                        # Int function define
                        at = self.f()
                        self.p(f'.{vn}')
                        self.cf.append(vn)
                        if at != ')':
                            an = self.f()
                            while True:
                                self.vars[an] = [at, self.vf]
                                self.p(f'POP R1')
                                self.p(f'STR {self.vf}, R1')
                                self.vf += 1
                elif vn == '*':
                    print('e')
                    vna = self.f()
                    if vna.isascii() and not vna in ['(', ')'] and not vna == '*':
                        eqs = self.f()
                        if eqs == '=':
                            p_d = self.f()
                            if split(p_d).__len__() == 1 and p_d.isnumeric():
                                self.vars[vna] = ['int*', self.vf]
                                self.p(f'STR {self.vf}, {p_d}')
                                self.vf += 1
                            elif split(p_d).__len__() == 1 and p_d.isascii() and not p_d.isnumeric() and p_d.startswith('&'):
                                self.vars[vna] = ['int*', self.vf]
                                self.p(f'STR {self.vf}, {self.vars[self.f()][1]}')
                                self.vf+=1
            elif d == '}':
                self.cf.pop()
            elif d == 'struct':
                vn = self.f()
                if vn.isascii() and not vn.isnumeric() and not vn in ['(', ')']:
                    opb = self.f()
                    if opb == '{':
                        self.f()
                        self.structs[vn] = {}
                        at_t = self.f()
                        at_n = self.f()
                        cb = self.f()
                        self.f()
                        while at_t != '}' and at_n != '}' and cb != '}':
                            self.structs[vn][at_n] = at_t
                            at_t = self.f()
                            try:
                                at_n = self.f()
                                cb = self.f()
                                self.f()
                            except IndexError: break
                    else:
                        eqs = self.f()
                        if eqs == ';':
                            self.vars[opb] = [f'struct_{vn}', self.vf]
                            #self.vf += self.structs[vn].keys().__len__()
                            for var__ in self.structs[vn].keys():
                                self.vars[f'{opb}_struct_::{var__}'] = [self.structs[vn][var__], self.vf]
                                self.vf += 1
            elif d == 'return':
                d2 = self.f()
                if d2 == ';':
                    if self.cf != []:
                        self.p(f'RET')
                        self.cci -= 1
                elif d2.isnumeric():
                    self.p(f'IMM R1, {d2}\nRET')
                elif d2.isascii() and not d2[0] in ['(', ')'] and not d2.isnumeric():
                    self.p(f'LOD R1, {self.vars[d2][1]}\nRET')
                else:
                    d6 = self.f()
                    while d6 != ';':
                        d2 += d6
                        d6 = self.f()
                    print('eee',d2)
                    d3 = split(d2)
                    d4 = parse_exp(d3)
                    d5 = parse_rpn(d4)
                    for o_ in d5:
                        #print(o_)
                        if o_[0].endswith('_I_I'):
                                    #print('e', o_)
                            d1 = parse_util[o_[0]](o_[1][0], o_[1][1])
                                    #print(d1)
                            self.p(d1)
                        elif o_[0].endswith('_V_I'):
                            d1 = parse_util[o_[0]](self.vars[o_[1][0]][1], o_[1][1])
                            self.p(d1)
                        elif o_[0].endswith('_I_V'):
                            d1 = parse_util[o_[0]]( o_[1][0], self.vars[o_[1][1]][1])
                            self.p(d1)
                        elif o_[0].endswith('_V_V'):
                            d1 = parse_util[o_[0]](  self.vars[o_[1][0]][1],  self.vars[o_[1][1]][1] )
                            self.p(d1)
                                
                        elif o_[0].endswith('_P_I'):
                            d1 = parse_util[o_[0]](o_[1][0])
                            self.p(d1)
                        elif o_[0].endswith('_P_V'):
                            d1 = parse_util[o_[0]](self.vars[o_[1][0]][1])
                            self.p(d1)
                        elif o_[0] == 'SAV':
                            self.p('PSH R1')
                        elif o_[0].endswith('_P_P'):
                            d1 = parse_util[o_[0]]()
                            self.p(d1)
                    if self.cf != []:
                        self.p('RET')
            else:
                if d == '*':
                    vn = self.f()
                    if vn in self.vars and self.vars[vn][0] == 'int*':
                        eqs = self.f()
                        if eqs == '=':
                            # reassign data where pointer is pointing
                            p_d = self.f()
                            if p_d.isnumeric() and not p_d in ['(', ')']:
                                self.p(f'LOD R1, {self.vars[vn][1]}')
                                self.p(f'STR R1, {p_d}')
                            elif p_d.isascii() and not p_d.isnumeric() and not p_d in ['(', ')']:
                                self.p(f'LOD R1, {self.vars[vn][1]}')
                                self.p(f'LOD R2, {self.vars[p_d][1]}')
                                self.p(f'STR R1, R2')
                            else:
                                dat = ''
                                d2 = p_d
                                while d2 != ';':
                                    dat = dat+d2
                                    d2 = self.f()
                                self.p(_parse_full_expression_(dat, self.vars)[:-1])
                                self.p(f'LOD R2, {self.vars[vn][1]}')
                                self.p(f'STR R2, R1')
                elif d in self.vars and self.vars[d][0].startswith('struct_'):
                    # struct modification
                    dot = self.f()
                    if dot == '.':
                        prop = self.f()
                        if prop in self.structs[self.vars[d][0][7:]]:
                            eqs = self.f()
                            if eqs == '=':
                                nd = self.f()
                                if nd.isnumeric():
                                    self.p(f'STR {self.vars[d+"_struct_::"+prop][1]}, {nd}')
                                elif nd.isascii() and not nd.isnumeric() and not nd in ['(', ')']:
                                    self.p(f'LOD R1, {self.vars[nd]}')
                                    self.p(f'STR {self.vars[d+"_struct_::"+prop][1]}, R1')
                                else:
                                    da = ''
                                    d__ = self.f()
                                    while d__ != ')':
                                        da += d__
                                        d__ = self.f()
                                    o__ = parse_exp(da)
                                    o_ = parse_rpn(o__)[0]
                                    if o_[0].endswith('_I_I'):
                                    #print('e', o_)
                                        d1 = parse_util[o_[0]](o_[1][0], o_[1][1])
                                    #print(d1)
                                        self.p(d1)
                                    elif o_[0].endswith('_V_I'):
                                        d1 = parse_util[o_[0]](self.vars[o_[1][0]][1], o_[1][1])
                                        self.p(d1)
                                    elif o_[0].endswith('_I_V'):
                                        d1 = parse_util[o_[0]]( o_[1][0], self.vars[o_[1][1]][1])
                                        self.p(d1)
                                    elif o_[0].endswith('_V_V'):
                                        d1 = parse_util[o_[0]](  self.vars[o_[1][0]][1],  self.vars[o_[1][1]][1] )
                                        self.p(d1)
                                
                                    elif o_[0].endswith('_P_I'):
                                        d1 = parse_util[o_[0]](o_[1][0])
                                        self.p(d1)
                                    elif o_[0].endswith('_P_V'):
                                        d1 = parse_util[o_[0]](self.vars[o_[1][0]][1])
                                        self.p(d1)
                                    elif o_[0] == 'SAV':
                                        self.p('PSH R1')
                                    elif o_[0].endswith('_P_P'):
                                        d1 = parse_util[o_[0]]()
                                        self.p(d1)

c = Compiler(open(sys.argv[1], 'r').read())
d = c.c()
print(d[0])
print(d[1:])
open(sys.argv[2], 'w').write(d[0])
#print(_parse_full_expression_("(((5+4)+(4+3))+3)+(3+4)", {}))