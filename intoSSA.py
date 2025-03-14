import sys
import json

def main():
    program = json.load(sys.stdin)
    

    functions = (list(program.values())[0])
    for function in functions:
        function = SSAify(function)

    for function in functions:
        print(function)

    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)
    #I learned how to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file





def SSAify(function):
    blocks, labels = basicblocks(function.get("instrs"))
    variables, defs = setvarsanddefs(function, blocks, labels)

    #blocks = list of block dict lists
    #labels = dict mapping labels to block(dict)s
    #variables = list of variables used in the program
    #defs = dictionary mapping variables to block labels that use them
    
    #print(variables)
    #print(defs)


    function = insertgetset(function, variables, defs, labels)

    cfg = getcfg(blocks, labels)
    for blockl in labels.keys():
        blockd = labels[blockl]
        rename(blockd, cfg, variables, labels)

    return function

    """#rename(entry)
    reverse = cfgreverse(cfg)
    for blockl in cfg.keys():
        if blockl not in reverse.keys():
            rename(labels[bl], cfg, variables, labels)"""


def setvarsanddefs(function, blocks, label):
    variables = []

    for blockd in blocks:
        for instr in blockd:
            if "args" in instr.keys():
                for arg in instr.get("args"):
                    variables.append(arg)

    defs = {}
    for blockd in blocks:
        blockl = labelofblock(blockd, label)
        for instr in blockd:
            instrargs = instr.get("args")
            instrdest = instr.get("dest")
            if instrargs is not None:
                for instrarg in instrargs:
                    if instrarg not in variables:
                        variables.append(instrarg)
            if instrdest is not None:
                if instrdest not in variables:
                    variables.append(instrdest)
                if instrdest in list(defs.keys()):
                    if blockl not in defs[instrdest]:
                        defs[instrdest] = defs[instrdest] + [blockl]
                else:
                    defs[instrdest] = [blockl]

    return variables, defs
        


def insertgetset(function, variables, defs, labelstoblock):
    #print("insert setget")
    for var in variables:
        if var in defs.keys():
            for defblockl in defs[var]:
                if defblockl is not None:
                    #defblockl = labelofblock(defblock, labelstoblock)
                    
                    defblockd = labelstoblock[defblockl]
                    
                    defblockd = addset(defblockd, function, var)
                    
                    frontier = domfrontier(function)
                    
                    #if defblockl is not None: #DON'T THINK THIS SHOULD BE HERE but idk
                    for frontl in frontier[defblockl]:
                        front = labelstoblock[frontl]

                        #add phi node to front, unless we have done so already
                        hasphi = False
                        for instr in front:
                            if instr.get("op") == "get":
                                hasphi = True
                        if hasphi == False:
                            newget = {"op": "get", "dest": var} #make json dictionary bril get command here!!
                            #print("adding get")
                            front.insert(0, newget)


                        if front not in defs[var]:
                            defs[var] = defs[var] + [front]

    return function

#change to go thru all children instead of all dominance frontier blocks. add set function too
#or keep as frontier strategy but do what michael is doing, keep track of all ancestors that need to be
#changed at the end, just do one backward pass at the end to change them.



def addset(blockd, function, var):
    labelstoblock = basicblocks(function.get("instrs"))[1]
    #blockd = labelstoblock[blockl]
    newvarname = var + "'"
    #variables with ' are shadow variables
    newset = {"op":"set", "args":[newvarname,var]}
    blockd.append(newset)
    #print("adding set")
    #labelstoblock[block] = block
    return blockd







def rename(block, cfg, variables, labels):
    topop = {}
    stacks = {} #new variable names we're adding
    for var in variables:
        stacks[var] = []
    for instr in block:
        if instr.get("args") is not None:
            for arg in instr.get("args"):
                if arg in stacks.keys() and stacks[arg] != []:
                    instr["args"].remove(arg)
                    instr["args"].append(stacks[arg].pop())
            
        if instr.get("dest") is not None:
            desty = instr.get("dest")
            newname = desty + "0"
            instr["dest"] = newname
            if desty in stacks.keys():
                stacks[desty] = stacks[desty] + [newname]
            else:
                stacks[desty] = [newname]

            if desty in topop.keys():
                topop[desty] = topop[desty] + [newname]
            else:
                topop[desty] = [newname]

    currlabel = labelofblock(block, labels)
    if currlabel in cfg.keys():
        for succl in cfg[currlabel]:
            if succl in labels.keys():
                succ = labels[succl]
                for instr in succ:
                    if instr.get("args") is not None:
                        for arg in instr.get("args"):
                            if arg in stacks.keys() and stacks[arg] != []:
                                instr.get("args").insert((instr.get("args")).index(arg), stacks[arg])
                                instr.get("args").remove(arg)


    tree = domtree((finddoms(cfg))[1], cfg)
    if currlabel in tree.keys():
        for immdom in tree[currlabel]:
            if immdom in cfg.keys():
                rename(labels[immdom], cfg, variables, labels)


    #pop all the names we just added
    for destyy in topop.keys():
        currlist = stacks[destyy]
        for newname in topop[destyy]:
            if newname in currlist:
                currlist.remove(newname)


        
    



    
                    























    


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
