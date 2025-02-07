import sys
import json
import itertools


def main():
    program = json.load(sys.stdin)

    functions = (list(program.values())[0])

    for func in functions:
        #do something to function (func)

        #OR

        x = 0

        basicblockss = basicblocks(func)
        blocks = basicblockss[0]
        labelstoblock = basicblockss[1]     
        for block in blocks:
            x+=1

        function = list(itertools.chain.from_iterable(blocks))

        (func)["instrs"] = function

    #print(program)

    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)




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
            """if "label" not in (instructions[i-1]).keys(): #since we divide blocks after terminators and after labels, if you have
            #a terminator followed by a label, you get an empty block, which we don't need to store."""
            blocks.append(newblock)
            if currlabel[0] == True: #curr block has a label
                labelstoblock[currlabel] = newblock
            elif nolabel == 0: # first block "start"
                labelstoblock[(False,"start")] = newblock
                nolabel+=1
            else: #other nonlabelled block
                labelstoblock[False,("nolabel" + str(nolabel))] = newblock
                nolabel+=1
            
            newblock = [currdict]
            currlabel = (True, currdict.get("label"))
        else:
            newblock.append(currdict) #regular non-terminator non-label command (but also acts on terminators too)
            if currdict.get("op") == "jump" or currdict.get("op") == "br": #jump or branch cases
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel] = newblock
                elif nolabel == 0: # first block "start"
                    labelstoblock[(False,"start")] = newblock
                    nolabel+=1
                else: #other nonlabelled block
                    labelstoblock[False,("nolabel" + str(nolabel))] = newblock
                    nolabel+=1
                newblock = []
                currlabel = (False, "")
        i+=1
    

    #to deal with last block:
    blocks.append(newblock)
    if currlabel[0] == True: #curr block has a label
        labelstoblock[currlabel] = newblock
    elif nolabel == 0: # first block "start"
        labelstoblock[(False,"start")] = newblock
        nolabel+=1
    else: #other nonlabelled block
        labelstoblock[False,("nolabel" + str(nolabel))] = newblock
        nolabel+=1

    """print("blocks")
    print(blocks)

    print("labelstoblock")
    print(labelstoblock)"""

    return [blocks, labelstoblock]












if __name__ == '__main__':
    main()