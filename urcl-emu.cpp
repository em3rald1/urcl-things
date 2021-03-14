#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <math.h>
#include <cmath>
#include <conio.h>
#include <stdio.h>

#define addrr 0
#define addir 1
#define addii 2
#define subrr 3
#define subir 4
#define subii 5
#define subri 89
#define rshr 6
#define rshl 7
#define lshr 8
#define lshl 9
#define incr 10
#define incl 11
#define decr 12
#define decl 13
#define xorrr 14
#define xorlr 15
#define xorll 16
#define orrr 17
#define orlr 18
#define orll 19
#define andrr 20
#define andlr 21
#define andll 22
#define notr 23
#define notl 24
#define mov 25
#define imm 26
#define lodr 27
#define lodl 28
#define stral 29
#define strar 30
#define strrl 31
#define strrr 32
#define brar 33
#define bral 34
#define brcr 35
#define brcl 36
#define bncr 37
#define bncl 38
#define brzr 39
#define brzl 40
#define bnzr 41
#define bnzl 42
#define brnl 56
#define brnr 57
#define brpl 58
#define brpr 59
#define nop 43
#define hlt 44
#define pshl 45
#define pshr 46
#define popi 47
#define calr 48
#define call 49
#define ret 50
#define sav 51
#define rsr 52
#define in 53
#define outr 54
#define outl 55
#define mltrr 60
#define mltlr 61
#define mltll 62
#define divrr 63
#define divlr 64
#define divrl 65
#define divll 66
#define modrr 67
#define modlr 68
#define modrl 69
#define modll 70

#define brllrr 71
#define brllrl 72
#define brlllr 73
#define brlrrr 74
#define brlrrl 75
#define brlrlr 76

#define brglrr 77
#define brglrl 78
#define brgllr 79
#define brgrrr 80
#define brgrrl 81
#define brgrlr 82

#define brelrr 83
#define brelrl 84
#define brerrr 85
#define brerrl 86

#define bnelrr 87
#define bnelrl 88
#define bnerrr 89
#define bnerrl 90

#define bodl 91
#define bodr 92

#define bevl 93
#define bevr 94

typedef unsigned char u8;
typedef unsigned short u16;
using std::vector;
using std::cin;
using std::cout;

class EMU {
    u16 ip;
    vector<u16> memory;
    vector<u16> regs;
    vector<u8> ports;
    bool z, v, n;
    public:
        EMU() {
            this->memory.reserve(0xffff);
            regs.reserve(0xff);
            ports.reserve(0xff);
            for(int i = 0; i < 0xffff; i++) memory[i] = 0;
            for(int i = 0; i < 0xff;   i++) regs[i]   = 0;
            for(int i = 0; i < 0xff;   i++) ports[i]  = 0;
            regs[0xff-3] = 0x7fff; // vsp
            regs[0xff-2] = 0x8fff; // csp
            regs[0xff-1]   = 0x9fff; // ssp
            this->ip = 0;
            this->z = true;
            this->v = false;
            this->n = false;
        }
        u16 fetch() {
            return this->memory[this->ip++];
        }
        void push(u16 d) {
            this->memory[this->regs[0xff-3]] = d;
            this->regs[0xff-3]--;
        }
        u16 pop() {
            this->regs[0xff-3]++;
            return this->memory[this->regs[0xff-3]];
        }
        void _call(u16 a) {
            this->memory[this->regs[0xff-2]] = this->ip;
            this->regs[0xff-2]--;
            this->ip = a;
        }
        void _ret() {
            this->regs[0xff-2]++;
            this->ip = this->memory[this->regs[0xff-2]];
        }
        void _sav(u16 r) {
            this->memory[this->regs[0xff-1]] = this->regs[r];
            this->regs[0xff-1]--;
        }
        void _rsr(u16 r) {
            this->regs[0xff-1]++;
            this->regs[r] = this->memory[this->regs[0xff-1]];
        }
        void uf(int d) {
            this->z = d == 0;
            this->v = d > std::pow(2, 16);
            this->n = d > std::pow(2, 16) || d < 0;
        }
        bool step() {
            bool res = false;
            u16 ins = fetch();
            
            //cout << ins << '\n';
            switch(ins) {
                case addii: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = fetch();
                    regs[dest] = o1+o2;
                    uf(o1+o2);
                    break;
                }
                case addir: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    regs[dest] = o1+o2;
                    uf(o1+o2);
                    break;
                }
                case addrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1+o2;
                    uf(o1+o2);
                    break;
                }
                case subii: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = fetch();
                    regs[dest] = o1-o2;
                    uf(o1-o2);
                    break;
                }
                case subir: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1-o2;
                    uf(o1-o2);
                    break;
                }
                case subri: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    regs[dest] = o1-o2;
                    uf(o1-o2);
                    break;
                }
                case subrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1-o2;
                    uf(o1-o2);
                    break;
                }
                case rshr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = o1 >> 1;
                    uf(o1 >> 1);
                    break;
                }
                case rshl: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = o1 >> 1;
                    uf(o1 >> 1);
                    break;
                }
                case lshr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = o1 << 1;
                    uf(o1 << 1);
                    break;
                }
                case lshl: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = o1 << 1;
                    uf(o1 << 1);
                    break;
                }
                case incr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = o1+1;
                    uf(o1+1);
                    break;
                }
                case incl: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = o1+1;
                    uf(o1+1);
                    break;
                }
                case decr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = o1-1;
                    uf(o1-1);
                    break;
                }
                case decl: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = o1-1;
                    uf(o1-1);
                    break;
                }
                case xorll: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = fetch();
                    regs[dest] = o1^o2;
                    uf(o1^o2);
                    break;
                }
                case xorlr: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1^o2;
                    uf(o1^o2);
                    break;
                }
                case xorrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1^o2;
                    uf(o1^o2);
                    break;
                }
                case orll: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = fetch();
                    regs[dest] = o1|o2;
                    uf(o1|o2);
                    break;
                }
                case orlr: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1|o2;
                    uf(o1|o2);
                    break;
                }
                case orrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1|o2;
                    uf(o1|o2);
                    break;
                }
                case andll: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = fetch();
                    regs[dest] = o1&o2;
                    uf(o1&o2);
                    break;
                }
                case andlr: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1&o2;
                    uf(o1&o2);
                    break;
                }
                case andrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[dest] = o1&o2;
                    uf(o1&o2);
                    break;
                }
                case notr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = ~o1;
                    uf(~o1);
                    break;
                }
                case notl: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = ~o1;
                    uf(~o1);
                    break;
                }
                case mov: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    regs[dest] = o1;
                    break;
                }
                case imm: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    regs[dest] = o1;
                    break;
                }
                case lodl: {
                    u16 dest = fetch();
                    u16 a = fetch();
                    regs[dest] = memory[a];
                    break;
                }
                case lodr: {
                    u16 dest = fetch();
                    u16 a = regs[fetch()];
                    regs[dest] = memory[a];
                    break;
                }
                case stral: {
                    u16 dest = fetch();
                    u16 a = fetch();
                    memory[dest] = a;
                    break;
                }
                case strar: {
                    u16 dest = fetch();
                    u16 a = regs[fetch()];
                    memory[dest] = a;
                    break;
                }
                case strrl: {
                    u16 dest = regs[fetch()];
                    u16 a = fetch();
                    memory[dest] = a;
                    break;
                }
                case strrr: {
                    u16 dest = regs[fetch()];
                    u16 a = regs[fetch()];
                    memory[dest] = a;
                    break;
                }
                case brar: {
                    u16 dest = regs[fetch()];
                    ip = dest;
                    break;
                }
                case bral: {
                    u16 dest = fetch();
                    ip = dest;
                    break;
                }
                case brcr: {
                    u16 dest = regs[fetch()];
                    if(this->v) ip = dest;
                    break;
                }
                case brcl: {
                    u16 dest = fetch();
                    if(this->v) ip = dest;
                    break;
                }
                case bncl: {
                    u16 dest = fetch();
                    if(!this->v) ip = dest;
                    break;
                }
                case bncr: {
                    u16 dest = fetch();
                    if(!this->v) ip = dest;
                    break;
                }
                case brzl: {
                    u16 dest = fetch();
                    if(this->z) ip = dest;
                    break;
                }
                case brzr: {
                    u16 dest = regs[fetch()];
                    if(this->z) ip = dest;
                    break;
                }
                case bnzl: {
                    u16 dest = fetch();
                    if(!this->z) ip = dest;
                    break;
                }
                case bnzr: {
                    u16 dest = regs[fetch()];
                    if(!this->z) ip = dest;
                    break;
                }
                case brnl: {
                    u16 dest = fetch();
                    if(this->n) ip = dest;
                    break;
                }
                case brnr: {
                    u16 dest = regs[fetch()];
                    if(this->n) ip = dest;
                    break;
                }
                case brpl: {
                    u16 dest = fetch();
                    if(!this->n) ip = dest;
                    break;
                }
                case brpr: {
                    u16 dest = regs[fetch()];
                    if(!this->n) ip = dest;
                    break;
                }
                case brllrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brllrl: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brlllr: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brlrrr: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brlrrl: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brlrlr: {
                    u16 dest = regs[fetch()];
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    if(o1 < o2) ip = dest;
                    break;
                }
                case brglrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brglrl: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brgllr: {
                    u16 dest = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brgrrr: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brgrrl: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brgrlr: {
                    u16 dest = regs[fetch()];
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    if(o1 > o2) ip = dest;
                    break;
                }
                case brelrr: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 == o2) ip = dest;
                    break;
                }
                case brelrl: {
                    u16 dest = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 == o2) ip = dest;
                    break;
                }
                case brerrr: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    if(o1 == o2) ip = dest;
                    break;
                }
                case brerrl: {
                    u16 dest = regs[fetch()];
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    if(o1 == o2) ip = dest;
                    break;
                }
                case nop: break;
                case hlt:{ 
                    res = true;
                    break;
                }
                case pshl: {
                    push(fetch());
                    break;
                }
                case pshr: {
                    push(regs[fetch()]);
                    break;
                }
                case popi: {
                    regs[fetch()] = pop();
                    break;
                }
                case call: {
                    _call(fetch());
                    break;
                }
                case calr: {
                    _call(regs[fetch()]);
                    break;
                }
                case ret: {
                    _ret();
                    break;
                }
                case sav: {
                    _sav(fetch());
                    break;
                }
                case rsr: {
                    _rsr(fetch());
                    break;
                }
                case in: {
                    u16 r = fetch();
                    u16 p = fetch();
                    //cout << p << " "<< r << "\n";
                    if(p == 78) {
                        u16 c = getch();
                        ports[p] = c;
                    }
                    regs[r] = ports[p];
                    break;
                }
                case outr: {
                    u16 p = fetch();
                    u16 r = fetch();
                    if(p == 78) {
                        cout << (char)regs[r];
                    }
                    ports[p] = regs[r];
                    break;
                }
                case outl: {
                    u16 p = fetch();
                    u16 r = fetch();
                    if(p == 78) {
                        cout << (char)r;
                    }
                    ports[p] = r;
                    break;
                }
                case mltlr: {
                    u16 d = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[d] = o1*o2;
                    uf(o1*o2);
                    break;
                }
                case mltrr: {
                    u16 d = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[d] = o1*o2;
                    uf(o1*o2);
                    break;
                }
                case divrl: {
                    u16 d = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = fetch();
                    regs[d] = (int)(o1/o2);
                    break;
                }
                case divlr: {
                    u16 d = fetch();
                    u16 o1 = fetch();
                    u16 o2 = regs[fetch()];
                    regs[d] = (int)(o1/o2);
                    break;
                }
                case divrr: {
                    u16 d = fetch();
                    u16 o1 = regs[fetch()];
                    u16 o2 = regs[fetch()];
                    regs[d] = (int)(o1/o2);
                    break;
                }
            }
            return res;
        }
        void debug() {
            cout << "REGISTERS:\n";
            for (int i = 0; i < 0xff; i++) {
                if(regs[i] != 0) cout << "$" << i << ": " << regs[i] << "\n";
            }
            cout << "PORTS:\n";
            for(int i = 0; i < 0xff; i++) {
                if(ports[i] != 0) cout << "%" << i << ": " << (int)ports[i] << "\n";
            }
            cout << "IP: " << ip << "\n";
        }
        void start(u16 s_p, bool db) {
            ip = s_p;
            volatile bool x = false;
            while(!x) {
                x = step();
                if(x) break;
            }
            if(db) debug();
        }
        void load(vector<u16> d, int size) {
           // cout << "load_pre_for\n";
            for(int i = 0; i < size; i++) {memory[i] = d[i];}
        }
};

vector<u16> convert(vector<u8> d) {
    vector<u16> output;
    output.reserve(d.size());
   // cout << "ok_1\n";
    //cout << d.size() << "\n";
    for(int i = 0; i < d.size()/2; i+=2) {
        output[i/2] = (d[i] << 8) | d[i+1];
        
    }
    //cout << "ok_2\n";
    output.reserve(d.size());
    return output;
}

int main(int argc, char** argv) {
    if(argc < 2) {
        cout << "Usage: " << argv[0] << " <compiled file>\n";
        return 1;
    }
    EMU urcl;
    //cout << "ok1\n";
    std::ifstream d(argv[1], std::ios::binary);
   // cout << "ok2\n";
    vector<u8> d1(std::istreambuf_iterator<char>(d), {});
    u16 *ptr = reinterpret_cast<u16*>(d1.data());
    std::vector<u16> s(ptr, ptr+d1.size()/2);
    urcl.load(s, s.size());
    urcl.start(0, true);
}