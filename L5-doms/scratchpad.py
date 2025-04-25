"""
for dominators domstest:

"""

"""if node not in reverse.keys(): #node is starter
            return currpath | {node}
        elif node not in cfg.keys(): #node is end
            return currpath | {node}"""   

"""def testsingledom(doms,cfg, node, suppdom):
    error = 0
    domscheck = {}
    domscheck = getpathsintersection(cfg, node, set())

    domscheck = domscheck | {'start'}
    
    if domscheck != set(doms[node]):
        print ("ERROR! doms for " + str(node) + " has failed. \n Desired: " + str(set(doms[node])) + " got: " + str(domscheck))
        error = 1
    #else pass, no error
    if error == 0:
        print("passed! yay :)")"""



#if node in intersections.keys() or child in intersections.keys()

#^ or or and or one by itself or another by itself idk 