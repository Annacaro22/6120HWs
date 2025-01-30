#ARGS: the positions.json file in bril/test/parse, should have 1 jump

import sys
import json


#Program to count the number of branching commands; the number of times br and jmp are called. Alternatively,
#the number of arrows in a CFG

count = 0
program = json.load(sys.stdin)
functions = (list(program.values())[0])
func = 0
while func < len(functions):
    instrs = (list(program.values())[0])[0]
    instructions = (list(instrs.values())[0])
    i = 0
    while i < len(instructions):
        currdict = instructions[i]
        if currdict.get("op") == "jmp":
            count+=1
        if currdict.get("op") == "br":
            count+=2 #add two because branch opens up two new possible paths
        i+=1
    func+=1

print(count)