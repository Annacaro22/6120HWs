import sys
import json

def main():
    program = json.load(sys.stdin)
    print("basic blocks: ")
    blocks = basicblocks(program)
    print(blocks)
    print("cfg: ")
    cfg = cfg(blocks)
    print(cfg)



def basicblocks(program):
    return []
    blocks = []

    functions = (list(program.values())[0])
    func = 0
    while func < len(functions):
        instrs = (list(program.values())[0])[0]
        instructions = (list(instrs.values())[0])
        i = 0
        while i < len(instructions): #for inst in instructions
            currdict = instructions[i] #currdict is the current instruction       
            if currdict.get("op") == "jmp":
                newblock = [] #add instruction that jump points to to the new block
                blocks.append(newblock)
            elif currdict.get("op") == "br":
                newblock = [] # add instruction 1 that branch points to to the new block
                newblock2 = [] # add instruction 2 that branch points to to the new block
                blocks.apend(newblock)
                blocks.append(newblock2)
            blocks[i].append(currdict) #i don't think the i is right here bc the index of the instruction isn't necessarily the number of the block
            #maybe keep a currblock counter?? and update accordingly?
            i+=1
        func+=1

    return blocks




def cfg(blocks):
    return {}
    cfg = {}
    
    for block in blocks:
        if block[-1].get("op") == "jmp":
            cfg[block] = #the instruction at whatever x jumps to
        if block[-1].get("op") == "br":
            cfg[block] = #the instructions at whatever x, y branch to
        if block[-1].get("op") == "label":
            cfg[block] = #the next instruction, bc if we've hit a label then that means we're just progressing as normal

    return cfg
