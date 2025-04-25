import sys
import json

#Program to calculate the basic blocks of a bril program and to create its CFG. Note that these are
#separated by function. The blocks and CFG will print out in the terminal after running this program.
#Note that I assert that all blocks have at least one child in my CFG. Leaves therefore point to 'end'.

def main():
    program = json.load(sys.stdin)


    functions = (list(program.values())[0])
    func = 0
    while func < len(functions):
        onefunc = functions[func]
        print("\n Basic Blocks in function " + onefunc.get("name") + " are: ")
        blocklabel = basicblocks(onefunc)

        print("\n CFG in function " + onefunc.get("name") + " is: ")
        print(getcfg(blocklabel[0],blocklabel[1]))        

        func+=1



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

        if "label" in currdict.keys(): #label case
            if newblock != []: #since we divide blocks after terminators and after labels, if you have
            #a terminator followed by a label, you get an empty block, which we don't need to store.
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel[1]] = newblock
                    print("\n" + currlabel[1] + ":")
                elif nolabel == 0: # first block "start"
                    labelstoblock["start"] = newblock
                    nolabel+=1
                    print("\n start:")
                else: #other nonlabelled block
                    labelstoblock["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
                    print("\n nolabel " + str(nolabel) + ":")
                print(newblock)
            newblock = []
            currlabel = (True, currdict.get("label"))
        else:
            newblock.append(currdict) #regular non-terminator non-label command (but also acts on terminators too)
            if currdict.get("op") == "jump" or currdict.get("op") == "br": #jump or branch cases
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel[1]] = newblock
                    print("\n" + currlabel[1] + ":")
                elif nolabel == 0: #first block "start"
                    labelstoblock["start"] = newblock
                    nolabel+=1
                    print("\n start:")
                else: #other nonlabelled block
                    labelstoblock["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
                    print("\n nolabel " + str(nolabel) + ":")
                print(newblock)
                newblock = []
                currlabel = (False, "")
        i+=1
    

    #to deal with last block:
    blocks.append(newblock)
    if currlabel[0] == True: #current block has a label
        labelstoblock[currlabel[1]] = newblock
        print("\n" + currlabel[1] + ":")
    elif nolabel == 0: #first block "start"
        labelstoblock["start"] = newblock
        nolabel+=1
        print("\n start:")
    else: #other nonlabelled block
        labelstoblock["nolabel" + str(nolabel)] = newblock
        nolabel+=1
        print("\n nolabel" + str(nolabel) + ":")
    print(newblock)

    return [blocks, labelstoblock]




def getcfg(blocks, labelstoblock):
    currlabel = "start"
    nextlabel = "end"
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
        elif blocks.index(block) == len(blocks)-1:
            cfg[currlabel] = ["end"]  #last block goes to end IF it doesn't end with a jmp/br
        else: 
            nextblock = blocks[blocks.index(block)+1]
            for key, val in labelstoblock.items(): #this is just to get the label of next block
                if val == nextblock:
                    nextlabel = key
            cfg[currlabel] = [nextlabel] #falls through to next block

    return cfg



if __name__ == '__main__':
    main()



