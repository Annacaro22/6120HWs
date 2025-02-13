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

        results = availablexps(blockslabel, cfg, function)
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


def availablexps(blockslabel, cfg, function):
    init = []

    def bigintersection(l): #l is a list of lists to merge as if they were sets (must store as list of lists since elts are dicts)
        intersection = l[0]
        i = 1
        while i < len(l):
            if intersection is not None:
                for instr in intersection:
                    if instr not in l[i]:
                        intersection.remove(instr)
            i+=1
        return intersection
         
    merge = bigintersection


    def addnewexps(blocklabel, inb, labels):
        #inb is set of active defs at start of block
        newexps = inb.copy() #newexps is a LIST. I know originally we want to be sets but can't store a set of dicts
        #at least not in python. so i'm doing list of dicts
        block = labels[blocklabel]
        for instr in block:


            #yknow i've decided not to do this one, initialized vars seems easier


            if newexps is not None:
                for olddef in currdefs:
                    if instr.get("dest") == olddef.get("dest"): #if we are defining to a var that is defined to in currdefs already
                        currdefs.remove(olddef) #instr kills olddef
                        if instr not in currdefs:
                            currdefs.append(instr) #instr replaces olddef
                        killer = True #use killer to process whether current instr has already been processed as a killer def
            if killer == False and "dest" in list(instr.keys()): #else branch essentially; NEW definition
                if currdefs is None:
                    currdefs = [instr]
                elif instr not in currdefs:
                    currdefs.append(instr) #add new def to definitions

            killer = False
        outb = currdefs
        return outb

    transfer = killsanddefs

    results = dataflow(blockslabel, cfg, init, merge,transfer)
    return results


def dataflow(blockslabel, cfg, init, merge, transfer):
    blocks = blockslabel[0]
    labels = blockslabel[1]

    inn = {}
    inn["start"] = init
    out = {}
    for label in list(labels.keys()):
        out[label] = init

    #Remember: inn and out have block labels as keys, and lists of instructions (the reaching definitions) as values

    worklist = list(labels.keys())
    while len(worklist) > 0:
        block = worklist.pop(0)
        #print("\n for block " + str(block) + ",")

        reverse = cfgreverse(cfg)
        preds = []
        if block in list(reverse.keys()):
            for p in reverse[block]:
                #print("pred of " + str(block) + " is " + str(p))
                preds.append(out[p])
        if block != "start":
            inn[block] = merge(preds)

        #print("in to block is " + str(inn[block]))

        if block != "end":
            oldoutblock = out[block]

            out[block] = transfer(block, inn[block], labels)
            #print("out of block is " + str(out[block]))

            if out[block] != oldoutblock:
                for succ in cfg[block]:
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
