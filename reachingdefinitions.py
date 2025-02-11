import sys
import json

def main():
    program = json.load(sys.stdin)

    functions = (list(program.values())[0])
    for function in functions:
        blockslabel = basicblocks(function.get("instrs"))
        cfg = getcfg(blockslabel[0], blockslabel[1])

        reachingdefs(blockslabel, cfg, function)

        dataflow(blockslabel, cfg)


    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)
    #I think I forgot to write this on last week's code, sorry about that, but I learned how
    #to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file


def reachingdefs(blockslabel, cfg, function):
    init = {"dest" : function.get("args")}

    def bigunion(l): #l is a list of sets to merge
        union = {}
        for s in l:
            union = union.union(s)
        return union
         
    merge = bigunion


    def killsanddefs(block, inb):
        #inb is set of active defs at start of block
        currdefs = inb #currdefs is a SET
        killer = False
        for instr in block:
            for olddef in currdefs:
                if instr.get("dest") == olddef.get("dest"): #if we are defining to a var that is defined to in currdefs already
                    currdefs.remove(olddef) #instr kills olddef
                    currdefs.add(instr) #instr replaces olddef
                    killer = True #use killer to process whether current instr has already been processed as a killer def
            if killer == False and "dest" in instr.keys(): #else branch essentially; NEW definition
                currdefs.add(instr) #add new def to definitions

            killer = False
        outb = currdefs
        return outb

    transfer = killsanddefs

    dataflow(blockslabel, cfg, init, merge,transfer)


def dataflow(blockslabel, cfg, init, merge, transfer):
    blocks = blockslabel[0]
    labels = blockslabel[1]

    inn = {}
    inn["start"] = init
    out = {}
    for b in blocks: #ERROR: need to make my dicts keys be labels of blocks not blocks themselves bc lists (which
    #is what blocks are, just lists of instrs) can't be dict keys :pensive: need to update this all over
        out[b] = init

    worklist = blocks
    while len(worklist) > 0:
        block = blocks.pop(0)

        reverse = cfgreverse(cfg)
        preds = []
        for p in reverse(block):
            preds.append(out[label[p]])
        inn[block] = merge(preds)

        oldoutblock = out[block]

        out[block] = transfer(block, inn[block])

        if out[block] != oldoutblock:
            for succ in cfg[block]:
                worklist.append(label.get(succ))


def cfgreverse(cfg):
    reverse = {}
    for block in cfg.keys():
        for succ in cfg[blocks]:
            if succ in reverse.keys():
                reverse[succ] = reverse[succ] + [block]
            else:
                reverse[succ] = [block]
    return reverse


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

    return [blocks, labelstoblock]



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
