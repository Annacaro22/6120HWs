# pylint: disable=missing-function-docstring, invalid-name, trailing-whitespace, superfluous-parens, fixme, line-too-long, missing-module-docstring, pointless-string-statement


import sys
import json
import copy


def main():

    fulltrace = json.load(open('getpath.json',))

    programmy = json.load(sys.stdin)

    trace = fulltrace.get("path")

    """traceoldmul = [{"dest":"b","op":"const","type":"bool","value":True},
{"dest":"x","op":"const","type":"int","value":5},
{"dest":"x","op":"const","type":"int","value":12},
{"args":["b"],"labels":["true","false"],"op":"br"},
{"args":["x"],"op":"print"},
{"dest":"b2","op":"const","type":"bool","value":True},
{"args":["b2"],"labels":["doubletrue","false"],"op":"br"},
{"args":["x"],"op":"print"},
{"op":"ret"}
]


    traceold = [{"dest":"b","op":"const","type":"bool","value":True},
{"dest":"x","op":"const","type":"int","value":5},
{"dest":"x","op":"const","type":"int","value":12},
{"args":["b"],"labels":["true","false"],"op":"br"},
{"args":["x"],"op":"print"},
{"op":"ret"}
]"""

    #just have to load in trace (and truefalse as part of trace) from terminal somehow
    
    newprogrammy = copy.copy(programmy)
    
    functions = (list(programmy.values())[0])
    functionindex = 0

    function = functions[0]
    _, labelstoblock = basicblocks(function.get("instrs"))

    program = function.get("instrs")

    newprogram = [{"label": "abort"}]
    newprogram = newprogram + program    

    allbranchinfo = findbranches(trace, program)

    firstbranch = allbranchinfo[0]
    _,_,_,firstbrindex,_ = firstbranch

    preceeding, numlabelsrem = removelabels(program[0:firstbrindex])

    newprogram = preceeding + newprogram


    branchinfo = allbranchinfo[0]

    content = inserting(branchinfo, labelstoblock)

    _, _, _ , progbrindex,_ = branchinfo

    newprogbrindex = progbrindex - numlabelsrem

    templist = newprogram[0:newprogbrindex]
    templist = templist + content
    templist = templist + newprogram[newprogbrindex:]
    newprogram = templist

    ((newprogrammy["functions"])[functionindex])["instrs"] = newprogram

    functionindex+=1


    #print(json.dumps(newprogrammy))

    with open("outfile.json", "w") as outfile:
        json.dump(newprogrammy, outfile)
    #I learned how to do this writing json to outfile from this stackoverflow post: 
    #https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file


#stuff we need to insert for each given branch
#should have speculate, b, guard, commint, contents of true branch, ret
def inserting(branchinfo, labelstoblock):
    _, brinstr, booldef, _, branchvalue = branchinfo

    print("inserting" + str(brinstr))

    instrlist = []
    
    instrlist.append({"op":"speculate"})
    instrlist.append(booldef)

    if branchvalue:
        instrlist.append({"args":[booldef.get("dest")], "dest": "newb", "op":"id", "type":"bool"})
    else:
        instrlist.append({"args":[booldef.get("dest")], "dest": "newb", "op":"not", "type":"bool"})

    instrlist.append({"args":["newb"],"labels" : ["abort"], "op":"guard"})
    instrlist.append({"op":"commit"})


    if branchvalue:
        branchtotake = brinstr.get("labels")[0]
    else:
        branchtotake = brinstr.get("labels")[1]

    instrlist = instrlist + labelstoblock[branchtotake]

    instrlist.append({"op":"ret"})

    return instrlist


def findbranches(trace, program):
    print("findbranches")
    allbranchinfo = []
    traceindex = 0
    for instr in trace:
        if "op" in instr.keys():
            if instr.get("op") == "br":
                booldef = getbooldef(trace, instr, traceindex)
                if instr in program:
                    progbrindex = program.index(instr)
                    pathchosen = trace[traceindex+1].get("branch value")
                    info = (traceindex, instr, booldef, progbrindex, pathchosen)
                    allbranchinfo.append(info)
        traceindex+=1

    return allbranchinfo



def getbooldef(trace, brinstr, brindex):
    print("getbooldef")
    booldef = {}
    b = brinstr.get("args")[0]
    traceindex = 0
    for instr in trace:
        if (traceindex < brindex):
            if instr.get("dest") == b:
                booldef = instr
        traceindex+=1

    if booldef == {}:
        print("error! could not find definition of bool " + b + " in trace")
    
    return booldef

        

def removelabels(program):
    numlabels = 0
    newprogram = []
    for instr in program:
        if "label" not in instr.keys():
            newprogram.append(instr)
        else:
            numlabels+=1

    return newprogram, numlabels













#edits trace to remove jumps and replace branches with guards
def fixtrace(trace):
    newtrace = []
    removelabels = []
    for instr in trace:
        if instr.get("op") == "br":
            removelabels.append(instr.get("labels")[0])
            guardy = {}
            guardy["args"] = instr.get("args")
            guardy["labels"] = instr.get("labels")[1]
            guardy["op"] = "guard"
            newtrace.append(guardy)
        elif instr.get("op") != "jmp":
            newtrace.append(instr)

    return newtrace, removelabels




#stitches trace back into program;
#adds speculate and commit, adds the guards where they were replaced in the trace, and deletes uneccesary labels & jumps
def stitch(trace, program, removelabels):
    program.insert(0, {"op" : "spectulate"})
    traceindex = 0
    for instr in program:
        if instr in trace:
            traceindex+=1
        else:
            if "label" in instr.keys():
                if instr.get("label") in removelabels:
                    program.remove(instr)
            elif instr.get("op") == "br":
                progindex = program.index(instr)
                program.insert(progindex, trace[traceindex])
                program.remove(instr)
                program.insert(progindex+1, {"op":"commit"})
                traceindex+=1
    

    
            








    

    
















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
    nextlabel = "realend"
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
                cfg[currlabel] = ["realend"] #return goes to end
            elif blocks.index(block) == len(blocks)-1:
                cfg[currlabel] = ["realend"]  #last block goes to end IF it doesn't end with a jmp/br
            else: 
                nextblock = blocks[blocks.index(block)+1]
                for key, val in labelstoblock.items(): #this is just to get the label of next block
                    if val == nextblock:
                        nextlabel = key
                cfg[currlabel] = [nextlabel] #falls through to next block

    return cfg



if __name__ == '__main__':
    main()
