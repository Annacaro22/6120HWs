#ARGS: my benchmark, combination.json, which should return 16-- 4 branches, 7 labels, 5 function calls, and 0 jumps.

import sys
import json


#Program to count the number of significant commands; the number of times br, jmp, or function call are called, or
#a label appears.

count = 0
program = json.load(sys.stdin)
functions = (list(program.values())[0])
#print(functions)
func = 0
while func < len(functions):
    onefunc = functions[func]
    #onefunc = (list(program.values())[0])[0]
    #print(onefunc)
    instructions = onefunc.get("instrs")
    #instructions = (list(instrs.values())[0])
    #print(instructions)
    i = 0
    while i < len(instructions):
        currdict = instructions[i]
        if "label" in currdict.keys():
            count+=1
        elif currdict.get("op") == "call" or currdict.get("op") == "jmp" or currdict.get("op") == "br":
            count+=1
        i+=1
    func+=1

print(count)