#really should make this and blocks two functions in the same file/class


import sys
import json

cfg = {}

program = json.load(sys.stdin)
blocks = basicblocks(program) #really i should have this be a function call to the other function in the same file

for block in blocks:
    if block[-1].get("op") == "jmp":
        cfg[block] = #the instruction at whatever x jumps to
    if block[-1].get("op") == "br":
        cfg[block] = #the instructions at whatever x, y branch to
    if block[-1].get("op") == "label":
        cfg[block] = #the next instruction, bc if we've hit a label then that means we're just progressing as normal

return cfg


