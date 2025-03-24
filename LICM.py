# pylint: disable=missing-function-docstring, invalid-name, trailing-whitespace, superfluous-parens, fixme


import sys
import json



def main():
    program = json.load(sys.stdin)

    program2 = program

    functions = (list(program.values())[0])
    index = 0
    for function in functions:
        blocks, labelstoblock = basicblocks(function.get("instrs"))
        cfg = getcfg(blocks, labelstoblock)
        reverse = cfgreverse(cfg)

        blockandlabel = basicblocks(function.get("instrs"))
        inn, out = reachingdefs(blockandlabel,cfg,function)
        
        newfunction = LICM(cfg, reverse, labelstoblock, function, inn, out)

        functionss = program2.get("functions")


        functionss[index] = newfunction


        index +=1



    with open("outfile.json", "w") as outfile:
        json.dump(program2, outfile)
    #I learned how to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file




def LICM(cfg, reverse, blockslabel, function, inn, out):
    natloops = natLoops(cfg, reverse)


    for header, loop in natloops.items():
        if len(reverse[header]) == 1:
            mergepre = True
            cfg = mergePreheaders(cfg, reverse, header, blockslabel, loop)[1]
            blockslabel = mergePreheaders(cfg, reverse, header, blockslabel, loop)[0]
            reverse = cfgreverse(cfg)
            preheader = "singlePre"
        else:
            if len(reverse[header]) == 2:
                mergepre = False
                preheader = (reverse[header])[0]
            else:
                mergepre = True
                cfg = mergePreheaders(cfg, reverse, header, blockslabel, loop)[1]
                blockslabel = mergePreheaders(cfg, reverse, header, blockslabel, loop)[0]
                reverse = cfgreverse(cfg)
                preheader = "singlePre"

        function = loopLICM([header] + loop, blockslabel, cfg, function, header, preheader, inn, out, mergepre)
    return function



def loopLICM(loop, blockslabel, cfg, function, header, preheader, inn, out, mergepre):
    #find loop invariants
    loopInvariants = []

    defsintoloop = inn[header]

    for block in loop: #remember block is block label, not dictionary
        blockd = blockslabel[block]
        for instr in blockd:
            if isLoopInvariant(instr, block, loopInvariants, blockslabel, cfg, function, loop, inn, out, defsintoloop) is True:
                if (instr, block) not in loopInvariants:
                    loopInvariants.append((instr, block))

    
    oldLoopInv = []
    while loopInvariants != oldLoopInv:
        oldLoopInv = loopInvariants

        defsintoloop = inn[header]

        for block in loop: #remember block is block label, not dictionary
            blockd = blockslabel[block]
            for instr in blockd:
                if isLoopInvariant(instr, block, loopInvariants, blockslabel, cfg, function, loop, inn, out, defsintoloop) is True:
                    if (instr, block) not in loopInvariants:
                        loopInvariants.append((instr, block))

    #find loop invariants that are safe to move
    safeToMove = []
    for instr, block in loopInvariants:
        if SafeToMove(instr, block, loopInvariants, cfg, inn, blockslabel, loop):
            safeToMove.append((instr, block))

    #possibly write merged preheader first
    reverse = cfgreverse(cfg)
    if "singlePre" in reverse.keys():
        oldpreheads = reverse["singlePre"]

        instrlist = function.get("instrs")

        for blockl in oldpreheads:
            block = blockslabel[blockl]
            for instr in block:
                if instr.get("op") == "br" or instr.get("op") == "jmp":
                    if header in instr.get("labels"): #change any jmp or br instructions from header to singlepre
                        oldinstr = instr
                        newinstr = instr
                        newinstr.get("labels").insert(instr.get("labels").index(header), "singlePre")
                        newinstr.get("labels").remove(header)

                        instrlist.insert(instrlist.index(oldinstr), newinstr)
                        instrlist.remove(oldinstr)

        instrlist.insert(instrlist.index({"label": header}), {"label": "singlePre"})

    #move the loop invariant
    for instr, block in safeToMove:

        blockd = blockslabel[block]
        preheaderd = blockslabel[preheader]

        preheaderd.append(instr)
        blockd.remove(instr)


        blockslabel[block] = blockd
        blockslabel[preheader] = preheaderd
        
        instrlist = function.get("instrs")

        instrlist.remove(instr)

        reverse = cfgreverse(cfg)
        if preheader in reverse.keys():
            if mergepre:
                insertindex = instrlist.index({'label' : 'singlePre'}) + 1
            else:
                preheaderindex = instrlist.index({'label' : preheader}) + 1
                insertindex = preheaderindex + len(preheaderd)
        else:
            preheaderindex = 0
            insertindex = preheaderindex + len(preheaderd) - 1
        instrlist.insert(insertindex, instr)

    return function

        
        



def isLoopInvariant(instr, blockl, loopinvariants, blockslabel, cfg, function, loop, inn, out, defsintoloop):
    if instr.get("args") is not None:
        if instr.get("dest") is not None:
            for arg in instr.get("args"):
                if arg == instr.get("dest"):
                    return False
                

    if instr.get("op") == "br" or instr.get("op") == "jmp":
        return False 

    yep = False
    if instr.get("args") is not None:
        goodArg = True
        block_reachingdefs = inn[blockl]

        blockloop_reachingdefs = []
        for i in block_reachingdefs:
            for blockl in loop:
                if i in blockslabel[blockl]:
                    blockloop_reachingdefs.append(i)

        defs = []
        for arg in instr.get("args"):

            for reachingdef in blockloop_reachingdefs:
                if reachingdef.get("dest") is not None:
                    if arg == reachingdef.get("dest"):
                        defs.append(reachingdef)

                       
            if len(defs) == 1:
                elsy = False
                if defs[0] in loopinvariants:
                    return True
            else:
                elsy = True
                for defn in defs:
                    for blockly in loop:
                        if defn in blockslabel[blockly]:
                            goodArg = False
        if elsy and goodArg:
            yep = True

    return yep


def SafeToMove(instr, blockl, loopinvariants, cfg, inn, blockslabel, loop): #block is block label
    doms = finddoms(cfg)[0]
    #Definition dominates all uses
    alluses = inn['end']
    reachy = []    
    if instr.get("dest") is not None:
        for instruc in alluses:
            if instruc.get("args") is not None:
                for arg in instruc.get("args"):
                    if arg == instr.get("dest"):
                        reachy.append(instruc)

    for r in reachy:
        for blockly in cfg.keys():
            if r in blockslabel[blockly]:
                if blockl not in doms[blockly]:
                    return False


    #No other definitions of the same variable (inside the loop)
    if instr.get("dest") is not None:
        for block in loop:
            for instruc in blockslabel[block]:
                if instruc.get("dest") is not None:
                    if instr.get("dest") == instruc.get("dest") and instr != instruc:
                        return False


    #Dominates all loop exits
    if blockl not in doms['end']:
        return False

    return True



def natLoops(cfg, reverse):
    doms = finddoms(cfg)[0]
    natloops = {}

    backedges = []
    for node in cfg.keys():
        for child in cfg[node]:
            if child in doms[node]:
                if (child, node) not in backedges: #otherwise both directions will be put in
                    backedges.append((node, child))


    for (A, B) in backedges:
        loopy = [A, B]
        oldloop = []
        while oldloop != loopy:
            oldloop = loopy
            for node in loopy:
                addToLoop(A, node, B, loopy, reverse)

        natloops[B] = loopy

    return natloops





def addToLoop(header, currnode, B, loopy, reverse):
    if currnode not in loopy:
        if currnode == B:
            loopy.append(B)
        else:
            if currnode in reverse.keys():
                predscond = True
                for pred in reverse[currnode]:
                    if pred not in loopy:
                        predscond = False
                if predscond is True:
                    loopy.append(currnode)






def mergePreheaders(cfg, reverse, loopHeader, labelstoblocks, loop):
    reverse = cfgreverse(cfg)
    newEmptyPreheader = "singlePre"
    labelstoblocks["singlePre"] = [{"label": "singlePre"}]
    for pre in reverse[loopHeader]:
        if pre not in loop:
            cfg[pre].insert(0, newEmptyPreheader)
            cfg[pre].remove(loopHeader)
    cfg[newEmptyPreheader] = [loopHeader]
    
    return labelstoblocks, cfg
#remember after you call this to refresh reverse as well since cfg has changed


    



    
                    























def reachingdefs(blockslabel, cfg, function):
    init = []
    if "args" in list(function.keys()):
        for arg in function.get("args"):
            init.append({"dest" : arg.get("name")})

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
         
    merge = bigunion


    def killsanddefs(blocklabel, inb, labels):
        #inb is set of active defs at start of block
        currdefs = inb.copy() #currdefs is a LIST. I know originally we want to be sets but can't store a set of dicts
        #at least not in python. so i'm doing list of dicts
        killer = False
        block = labels[blocklabel]
        for instr in block:
            if currdefs is not None:
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

        reverse = cfgreverse(cfg)
        preds = []
        if block in list(reverse.keys()):
            for p in reverse[block]:
                preds.append(out[p])
        if len(preds) >= 1:
            inn[block] = merge(preds)
        else:
            inn[block] = init


        if block != "end":
            oldoutblock = out[block]

            out[block] = transfer(block, inn[block], labels)

            
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


    return (inn, out)    


def labelofblock(block, labels):
    for label in labels:
        if block == labels[label]:
            return label
    return None


def finddoms(cfg):
    predcfg = cfgreverse(cfg)
    olddom = None
    dom = {}

    for vertex in (list(cfg.keys()) + ['end']):
        dom[vertex] = set(cfg.keys()) | {'end'}
    domlevel = {}
    while dom != olddom:
        olddom = dom
        for vertex in (list(cfg.keys()) + ['end']):
            if vertex not in list(predcfg.keys()):
                currdoms = set({vertex})
                currdomslevel = {}
            else:
                currdoms = set(list(cfg.keys()))
                currdomslevel = {}
                for pred in predcfg[vertex]:
                    if pred in dom.keys():
                        currdoms = currdoms & set(dom[pred])

                for pred in predcfg[vertex]:
                    if pred in list(domlevel.keys()):
                        for level, domm in list(domlevel[pred].items()):
                            if domm in currdoms:
                                currdomslevel[level+1] = domm  
                                     
            dom[vertex] = list(currdoms | {vertex})
            domlevel[vertex] = currdomslevel | {0 : vertex}
    return dom, domlevel


def domtree(domlevel, cfg):
    reverse = cfgreverse(cfg)
    tree = {}
    for starter in cfg.keys():
        if starter not in reverse.keys(): #AKA has no preds AKA is a starter block
            tree[starter] = []
    oldtree = None
    while oldtree != tree:
        oldtree = tree
        for vertex in (list(cfg.keys()) + ['end']):
            if vertex in reverse.keys() and reverse[vertex] is not None: #AKA has some pred AKA not a starter block
                currdomlevels = domlevel[vertex]
                keysonly = list(currdomlevels.keys())
                
                newkeys = []
                for num in keysonly:
                    if num != 0:
                        newkeys.append(num)

                if (newkeys) is not None and newkeys != []:
                    immdomindex = min(newkeys)
                    immdom = currdomlevels[immdomindex]
                    if immdom in tree.keys() and tree[immdom] is not None and tree[immdom] != []:
                        tree[immdom].append(vertex)
                    else:
                        tree[immdom] = [vertex]
    return tree


def domfrontier(function):
    blockslabel = basicblocks(function.get("instrs"))
    cfg = getcfg(blockslabel[0], blockslabel[1])

    doms = (finddoms(cfg))[0]

    reversedoms = cfgreverse(doms)
    frontier = {}
    for node in (list(cfg.keys()) + ['end']):
        frontier[node] = []
        postdoms = reversedoms[node]
        for postdom in postdoms:
            if postdom in cfg.keys():
                for child in cfg[postdom]:
                    if child not in postdoms:
                        if node in frontier.keys():
                            frontier[node] = frontier[node] + [child]
                        else:
                            frontier[node] = [child]
    return frontier







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
    for currdict in instructions: #for inst in instructions
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
