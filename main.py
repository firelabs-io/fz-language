# opcodes: mov, add, sub, jmp, jmc, label, ret, end
import sys
import time

class machine:
    def __init__(self, program):
        self.tokens = []
        self.reg = {'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0}    
        self.label = {}
        self.stack = []
        self.debug = False
    def tokenize(self):
        i = 0
        for line in program:
            line = line.replace(',', '')
            if line.endswith(':'):
                self.label[line[:-1]] = i
            
            self.tokens.append(line.split(' '))
            i += 1
    def labelc(self, i):
        j = 0
        while j < len(self.tokens):
            tokens = self.tokens[j]
            if tokens[0][:-1] in self.label:
                if tokens[0] == "main:":
                    i = j
                    break
            j += 1
        return i
    def run(self):
        i = self.labelc(0)
        while i < len(self.tokens):
            token = self.tokens[i]
            opcode = token[0]
            if opcode == 'mov':
                op1, op2 = token[1], token[2]
                if op2 in self.reg:
                    self.reg[op1] = self.reg[op2]
                elif not op2.isdigit():
                    print("ERROR: trying assign non integer number to register or non existent register")
                    exit(1)
                else:
                    self.reg[op1] = int(op2)
            elif opcode == 'add':
                op1, op2 = token[1], token[2]
                if op2 in self.reg:
                    self.reg[op1] = self.reg[op1] + self.reg[op2]
                elif not op2.isdigit():
                    print("ERROR: adding non integer number to register or non existent register")
                    exit(1)
                else:
                    self.reg[op1] += int(op2)
            elif opcode == 'sub':
                op1, op2 = token[1], token[2]
                if op2 in self.reg:
                    self.reg[op1] = self.reg[op1] - self.reg[op2]
                elif not op2.isdigit():
                    print("ERROR: subtracting non integer number to register or non existent register")
                    exit(1)
                else:
                    self.reg[op1] -= int(op2)
            elif opcode == 'jmp':
                op1 = token[1]
                if op1 not in self.label:
                    print("ERROR: jumping to label that don't exist")
                    exit(1)
                self.stack.append(i)
                i = self.label[op1]
            elif opcode == 'jmc':
                op1, op2 = token[1], token[2]
                if op1 not in self.label:
                    print("ERROR: jumping to label that don't exist")
                    exit(1)
                elif op2 in self.reg:
                    if self.reg[op2] != 0:
                        if self.reg[op2] < 0:
                            ...
                        else:
                            self.stack.append(i)
                            i = self.label[op1]
                elif not op2.isdigit():
                    print("ERROR: jump compare need have number or register")
                else:
                    if int(op2) != 0:
                        if op2 < 0:
                            ...
                        else:
                            self.stack.append(i)
                            i = self.label[op1]
            elif opcode == 'jnc':
                op1, op2 = token[1], token[2]
                if not op1 in self.label:
                    print("ERROR: jumping to label don't exist")
                    exit(1)
                elif op2 in self.reg:
                    if self.reg[op2] == 0:
                        self.stack.append(i)
                        i = self.label[op1]
                elif not op2.isdigit():
                    print("ERROR: jump compare need have number or register")
                    exit(1)
                else:
                    if int(op2) == 0:
                        self.stack.append(i)
                        i = self.label[op1]
            elif opcode == 'ret':
                if not self.stack:
                    print("ERROR: returning to non existent address")
                    exit(1)
                i = self.stack[-1]
                self.stack.pop()
            elif opcode == 'exit':
                if len(token) == 2:
                    op1 = token[1]
                    if op1 in self.reg:
                        exit(self.reg[op1])
                    elif not op1.isdigit():
                        print("ERROR: exit number must be integer")
                        exit(1)
                    exit(int(op1))
                else:
                    exit(0)
            elif opcode == "out":
                op1 = token[1]
                if op1 in self.reg:
                    print(self.reg[op1])
                else:
                    print(op1)
            elif opcode == "in":
                op1 = token[1]
                if op1 in self.reg:
                    inp = int(input())
                    self.reg[op1] = inp
                else:
                    print("ERROR: must have register")
            if self.debug:
                print(self.reg, self.label, self.stack, token)
                time.sleep(0.5)
            i += 1

program = []


with open(sys.argv[1], 'r') as file:
    for line in file:
        program.append(line.strip())
m = machine(program)
if len(sys.argv) == 3:
    m.debug = True
m.tokenize()
m.run()
