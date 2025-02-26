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

        doms, level = finddoms(cfg)

        print("doms is " + str(doms))

        print("domlevel is " + str(level))

        tree = domtree(level, cfg)

        print("dominator tree is " + str(tree))

        frontier = domfrontier(doms, cfg)

        print("frontier is " + str(frontier))

        #test1 = testdoms(doms, cfgreverse(cfg))

        test2 = testdomtree(doms, tree, cfg)

        test3 = testfrontier(doms, frontier, cfg)



    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)
    #I learned how to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file






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

                #remove not working for some reason????
                #newkeys = keysonly.remove(0)

                if (newkeys) is not None and newkeys != []:
                    immdomindex = min(newkeys)
                    immdom = currdomlevels[immdomindex]
                    if immdom in tree.keys() and tree[immdom] is not None and tree[immdom] != []:
                        tree[immdom].append(vertex)
                    else:
                        tree[immdom] = [vertex]
    return tree




def domfrontier(doms, cfg):
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







def bigintersection(l): #l is a list of lists to merge as if they were sets
        intersection = l[0]
        i = 1
        while i < len(l):
            if intersection is not None:
                for instr in intersection:
                    if instr not in l[i]:
                        intersection.remove(instr)
            i+=1
        return intersection


def cfgreverse(cfg):
    reverse = {}
    for block in list(cfg.keys()):
        for succ in cfg[block]:
            if succ in list(reverse.keys()):
                reverse[succ] = reverse[succ] + [block]
            else:
                reverse[succ] = [block]
    return reverse

    







#TESTING:

def testdoms(doms, cfg): #DO NOT USE YET; still infinite loops on cycles :(
    error = 0
    for node in list(cfg.keys()) + ['end']:
        domscheck = {}
        intersections = {}
        #print("testing " + str(node))
        intersection = set(list(cfg.keys()) + ['end'])
        domscheck = getpathsintersection(cfg, node, set(), intersection, intersections)

        reverse = cfgreverse(cfg)
        for starterq in list(reverse.keys()) + ['end']:
            if starterq not in cfg.keys():
                domscheck = domscheck | {starterq}

        if domscheck != set(doms[node]):
            print ("ERROR! doms for " + str(node) + " has failed. \n Desired: " +str(domscheck) + " got: " + str(set(doms[node])) )
            error = 1
        #else pass, no error
    if error == 0:
        print("passed! yay :)")


def getpathsintersection(cfg, node, currpath, intersection, intersections):
    #intersections = {}
    #print("calculating for " + str(node))
    #print("intersections is " + str(intersections) )
    if node not in cfg.keys():
        return currpath | {node}
    else:
        reverse = cfgreverse(cfg)      
        for child in cfg[node]:
            #print("child " + str(child))
            if currpath in intersections.values(): #if we've already processed; cycle
                #print("intersections " + str(intersections))
                #print("(preloop) intersection is: " + str(intersection))
                intersection = intersection & intersections[node]
                intersections[child] = intersection
                #print("(loop) intersection is: " + str(intersection))
            else:
                intersection = intersection & getpathsintersection(cfg,child, currpath | {node}, intersection, intersections)
                intersections[child] = intersection
                #print("intersection is: " + str(intersection))
            #print("added child to intersections " + str(intersections))
        #print("intersection is " + str(intersection))
        return intersection



def testdomtree(doms, tree, cfg): #we are now confident that doms works and can just use that
    works = True
    for parent in tree.keys():
        for child in tree[parent]:
            if parent not in doms[child]:
                works = False
                print("ERROR, " + str(child) + " is not dominated by " + str(parent))
            for node in tree.keys():
                if node != parent and node != child and parent in doms[node] and node in doms[child]:
                    works = False
                    print("ERROR, " + str(node) + " is between " + str(parent) + " and " + str(child))
    if works == True:
        print("passed! yay :)")




def testfrontier(doms, frontier, cfg): #we are now confident that domtree works and can just use that
    works = True
    for node in cfg.keys():
        for front in frontier[node]:
            if node in doms[front]:
                works = False
                print("ERROR, " + str(front) + " is dominated by " + str(node))

            for othernode in list(cfg.keys()) + ['end']:
                if othernode in doms[front] and othernode in frontier[node] and othernode != front:
                    works = False
                    print("ERROR, there is node " + str(othernode) +" in the frontier of " + str(node) + " before " + str(front))
    if works == True:
        print("passed! yay :)")
            
            














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
