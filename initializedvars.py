import sys
import json

def main():
    program = json.load(sys.stdin)

    functions = (list(program.values())[0])
    for function in functions:
        print("\n \n function " + str(function.get("name")))

        blockslabel = basicblocks(function.get("instrs"))
        cfg = getcfg(blockslabel[0], blockslabel[1])

        print("cfg for function: " + str(cfg))
        print("Reverse cfg: " + str(cfgreverse(cfg)))

        results = initializedvars(blockslabel, cfg, function)
        inn = results[0]
        out = results[1]

        for block in blockslabel[1]:
            print("\nfor block " + block + ", in to block is:")
            print(inn[block])
            print("out of block is:")
            print(out[block])




    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)
    #I think I forgot to write this on last week's code, sorry about that, but I learned how
    #to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file


def initializedvars(blockslabel, cfg, function):
    init = []
    if "args" in list(function.keys()):
        for arg in function.get("args"):
            init.append(arg.get("name"))

    def bigintersection(l): #l is a list of lists to merge as if they were sets
        intersection = l[0].copy()
        i = 1
        while i < len(l):
            if intersection is not None:
                for instr in intersection:
                    if instr not in l[i]:
                        intersection.remove(instr)
            else:
                intersection = []
            i+=1
        return intersection

    def setconversion(l):
        intersection = set(l[0].copy())
        i = 1
        while i < len(l):
            intersection = intersection & set(l[i])
            i+=1
        return list(intersection)

    def bigunion(l): #l is a list of lists to merge as if they were sets (must store as list of lists since elts are dicts)
        i = 0
        union = []
        while i < len(l):
            if l[i] is not None:
                for instr in l[i]:
                    if instr not in union:
                        union.append(instr)
            i+=1
        return union
         
    #merge = bigunion

         
    merge = setconversion


    def addnewinits(blocklabel, inb, labels):
        #inb is set of init vars at start of block
        currinits = inb.copy() #currinits is a LIST.
        block = labels[blocklabel]
        for instr in block:
            if "dest" in list(instr.keys()):
                if instr.get("dest") not in currinits:
                    currinits.append(instr.get("dest"))
                    #print("adding " + instr.get("dest"))
        outb = currinits
        return outb

    transfer = addnewinits

    results = dataflow(blockslabel, cfg, init, merge, transfer)
    return results


def dataflow(blockslabel, cfg, init, merge, transfer):
    blocks = blockslabel[0]
    labels = blockslabel[1]

    inn = {}
    inn["start"] = init
    out = {}
    for label in list(labels.keys()):
        out[label] = init

    #Remember: inn and out have block labels as keys, and lists of strings (the initialized variables) as values

    worklist = list(labels.keys())
    while len(worklist) > 0:
        block = worklist.pop(0)
        print("\n for block " + str(block) + ",")

        reverse = cfgreverse(cfg)
        preds = []
        if block in list(reverse.keys()):
            for p in reverse[block]:
                #print("pred of " + str(block) + " is " + str(p))
                preds.append(out[p])
        if len(preds) >= 1:
            inn[block] = merge(preds)
        else:
            inn[block] = init
        #ERROR: There's some bug in the way I'm defining merge I think. It's causing an infinite loop
        #in reaching defs (disappears when i change from union to intersection), and it's giving me wrong
        #answers here (why is primetest deleting t0? every path should have it initialized). Idk what's going
        #on here but something is broken with merge. FIXED DEFINITIONS. or it doesn't loop now at least lol.
        #not sure what's going on with initialized vars though. might just give up and just do reaching definitions.

        #print("in to block is " + str(inn[block]))

        if block != "end":
            oldoutblock = out[block]

            out[block] = transfer(block, inn[block], labels)
            #print("out of block is " + str(out[block]))

            """if out[block] != oldoutblock:
                for succ in cfg[block]:
                    worklist.append(succ)"""

            changed = False
            for x in out[block]:
                if x not in oldoutblock:
                    changed = True
            for y in oldoutblock:
                if y not in out[block]:
                    changed = True
            
            if changed == True:
                for succ in cfg[block]:
                    if succ not in worklist:
                        worklist.append(succ)
        #else:
            #print("block is end; no out!")
    return (inn, out)


def cfgreverse(cfg):
    reverse = {}
    for block in list(cfg.keys()):
        for succ in cfg[block]:
            if succ in list(reverse.keys()):
                reverse[succ] = reverse[succ] + [block]
            else:
                reverse[succ] = [block]
    return reverse


def basicblocks(onefunc):
    blocks = []
    labelstoblock = {}
    labelsnotbools = {}
    currlabel = [False, ""]
    instructions = onefunc
    i = 0
    newblock = []
    nolabel = 0
    while i < len(instructions): #for inst in instructions
        currdict = instructions[i] #currdict is the current instruction 

        if "label" in list(currdict.keys()): #label case
            if newblock != []:
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel] = newblock
                    labelsnotbools[currlabel[1]] = newblock
                elif nolabel == 0: # first block "start"
                    labelstoblock[(False,"start")] = newblock
                    labelsnotbools["start"] = newblock
                    nolabel+=1
                else: #other nonlabelled block
                    labelstoblock[False,("nolabel" + str(nolabel))] = newblock
                    labelsnotbools["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
            
            newblock = [currdict]
            currlabel = (True, currdict.get("label"))
        else:
            newblock.append(currdict) #regular non-terminator non-label command (but also acts on terminators too)
            if currdict.get("op") == "jump" or currdict.get("op") == "br": #jump or branch cases
                blocks.append(newblock)
                if currlabel[0] == True: #curr block has a label
                    labelstoblock[currlabel] = newblock
                    labelsnotbools[currlabel[1]] = newblock
                elif nolabel == 0: # first block "start"
                    labelstoblock[(False,"start")] = newblock
                    labelsnotbools["start"] = newblock
                    nolabel+=1
                else: #other nonlabelled block
                    labelstoblock[False,("nolabel" + str(nolabel))] = newblock
                    labelsnotbools["nolabel" + str(nolabel)] = newblock
                    nolabel+=1
                newblock = []
                currlabel = (False, "")
        i+=1
    

    #to deal with last block:
    blocks.append(newblock)
    if currlabel[0] == True: #curr block has a label
        labelstoblock[currlabel] = newblock
        labelsnotbools[currlabel[1]] = newblock
    elif nolabel == 0: # first block "start"
        labelstoblock[(False,"start")] = newblock
        labelsnotbools["start"] = newblock
        nolabel+=1
    else: #other nonlabelled block
        labelstoblock[False,("nolabel" + str(nolabel))] = newblock
        labelsnotbools["nolabel" + str(nolabel)] = newblock
        nolabel+=1

    return [blocks, labelsnotbools]



def getcfg(blocks, labelstoblock):
    currlabel = "start"
    nextlabel = "end"
    cfg = {}
    for block in blocks:
        if len(block) > 0:
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
