import sys
import json

def main():
    program = json.load(sys.stdin)
    print()


    functions = (list(program.values())[0])
    func = 0
    while func < len(functions):
        onefunc = functions[func]
        print("\n Basic Blocks in function " + onefunc.get("name") + " are: ")
        blocklabel = basicblocks(onefunc)
        print("\n labels to blocks: ")
        print(blocklabel[1])

        print("\n CFG in function " + onefunc.get("name") + " is: ")
        print(getcfg(blocklabel[0],blocklabel[1]))        

        func+=1



#jump, branch, call, label(no jump just continue)
def basicblocks(onefunc):
    blocks = []
    labelstoblock = {}
    currlabel = [False, ""]
    instructions = onefunc.get("instrs")
    i = 0
    newblock = []
    nolabel = 0
    while i < len(instructions): #for inst in instructions
        currdict = instructions[i] #currdict is the current instruction 

        if "label" in currdict.keys():
            if newblock != []: #since we divide blocks after terminators and after labels, if you have
            #a terminator followed by a label, you get an empty block, which we don't need to store.
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel[1]] = newblock
                elif nolabel == 0: # first block "start"
                    labelstoblock["start"] = newblock
                    nolabel+=1
                else: #other nonlabelled block
                    labelstoblock["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
                print("\n")
                print(newblock)
            newblock = []
            currlabel = (True, currdict.get("label"))
        else:
            newblock.append(currdict)
            if currdict.get("op") == "jump" or currdict.get("op") == "br":
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel[1]] = newblock
                elif nolabel == 0: #first blcok "start"
                    labelstoblock["start"] = newblock
                    nolabel+=1
                else: #other nonlabelled block
                    labelstoblock["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
                print("\n")
                print(newblock)
                newblock = []
                currlabel = (False, "")
        i+=1
    
    blocks.append(newblock)
    if currlabel[0] == True: #current block has a label
        labelstoblock[currlabel[1]] = newblock
    elif nolabel == 0: #first block "start"
        labelstoblock["start"] = newblock
        nolabel+=1
    else: #other nonlabelled block
        labelstoblock["nolabel" + str(nolabel)] = newblock
        nolabel+=1
    print("\n")
    print(newblock)

    return [blocks, labelstoblock]




def getcfg(blocks, labelstoblock):

    cfg = {}
    for block in blocks:
        lastinstr = block[-1] #last instruction of block
        for key, val in labelstoblock.items(): #this is just to get the label of current block
            if val == block:
                currlabel = key
        if lastinstr.get("op") == "jmp":
            cfg[currlabel] = [lastinstr.get("labels")[0]] #only one child block
        elif lastinstr.get("op") == "br":
            cfg[currlabel] = [lastinstr.get("labels")[0]]
            cfg[currlabel].append(lastinstr.get("labels")[1]) #2 children blocks
        elif lastinstr.get("op") == "ret":
            cfg[currlabel] = ["end"] #return goes to end
        elif blocks.index(block) < len(blocks)-1:
            cfg[currlabel] = [blocks[blocks.index(block)+1]] #falls through to next block

    cfg[currlabel] = ["end"]  #last block goes to end

    return cfg



if __name__ == '__main__':
    main()



