import sys
import json
import itertools


def main():
    program = json.load(sys.stdin)


    functions = (list(program.values())[0])
    func = 0
    while func < len(functions):
        onefunc = functions[func]

        blocks = basicblocks(onefunc.get("instrs"))[0]

        #wrap in iteration to convergence, while function is still changing
        prevfunction = None
        function = onefunc.get("instrs")

        while function != prevfunction:
            prevfunction = function.copy()
            
            function = defined_not_used(function)

            blocks = basicblocks(function)[0]


            j = 0
            while j < len(blocks):
                blocks[j] = rewritten(blocks[j])
                j+=1


            function = list(itertools.chain.from_iterable(blocks))


        (functions[func])["instrs"] = function
        #putting our updated instructions back into the JSON file

        func+=1
    

    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)
    #I learned how to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file

    



def defined_not_used(function):
    used = []
    instructions = function

    i=0
    while i < len(instructions): #loop through getting used vars
        currdict = instructions[i] #current instruction
        if currdict.get("args") is not None:
            for arg in currdict.get("args"):
                used.append(arg)      
        i+=1


    j=0
    while j < len(instructions): #loop through finding assigned vars that aren't used
        currdict = instructions[j] #current instruction
        destination = currdict.get("dest")
        if destination is not None and destination not in used:
            instructions.remove(currdict)
        j+=1

    return instructions



def rewritten(currblock):
    last_def = {} #defined but not used, variables -> instructions

    for currdict in currblock: #currdict is the current instruction
        #check for uses (RHS appearances-- using x)
        if currdict.get("args") is not None:
            for arg in currdict.get("args"):
                if arg in last_def.keys():
                    del last_def[arg]

        #check for defs (LHS appearances-- rewriting x)
        instrucdest = currdict.get("dest")
        if instrucdest is not None and instrucdest in last_def:
            currblock.remove(last_def[instrucdest]) #deleting from instructions, not from last_def
            
        last_def[instrucdest] = currdict

    return currblock



















def basicblocks(onefunc):
    blocks = []
    labelstoblock = {}
    currlabel = [False, ""]
    instructions = onefunc
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