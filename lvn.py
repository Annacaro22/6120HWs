import sys
import json
import itertools

def main():
    program = json.load(sys.stdin)


    functions = (list(program.values())[0])
    newvariable = 0
    for func in functions:
        blocks = basicblocks(func)[0]     
        for block in blocks:
            memorymesses = False
            for instr in block:
                if instr.get("op") == "alloc" or instr.get("op") == "ptradd": #if it messes with memory just leave it alone
                    memorymesses = True
            if memorymesses == False:
                lvn(block, newvariable)

        function = list(itertools.chain.from_iterable(blocks))

        (func)["instrs"] = function

    with open("outfile.json", "w") as outfile:
        json.dump(program, outfile)

    print(program)




def lvn(block, newvariable):
    rowcount = 0
    table = {} # maps value tuples to canonical variables and row number. table = {value tuple : (canon var, #)}
    cloud = {} #maps variable names to value numbers / rows in table. cloud = {curr var : #}

    for instr in block:
        iscopy = False

        changednewvars = {}

        currindex = block.index(instr)
        oginstr = instr

        if instr.get("args") is not None:
            argoutofblock = [False] * len(instr.get("args"))

        #establish value
        if instr.get("op") == "const":
            value = (instr.get("op"), instr.get("value"), instr.get("type"))
        else:
            if instr.get("args") is not None:
                for arg in instr.get("args"): #If you've got an arg not in the cloud, i.e. came from another block
                #or something, then add it to the cloud and table with UNKNOWN value.
                    if arg not in cloud.keys():
                        argoutofblock[instr.get("args").index(arg)] = True
                        #but first! before you add! you have to see if this unknown value will be rewritten to,
                        #and if so, change the variable name
                        rewritelater = False #bool to hold whether the current var will be rewritten later.
                        argtomemory = False #bool to hold whether the current var we're considering will be used as an arg in a memory instruction; if so, we shouldn't rename it.
                        for laterinstr in block[block.index(instr)+1:]:
                            if laterinstr.get("dest") == arg:
                                rewritelater = True
                            if laterinstr.get("args") is not None:
                                if arg in laterinstr.get("args") and (laterinstr.get("op") == "alloc" or laterinstr.get("op") == "ptradd"):
                                    argtomemory = True

                        
                        if rewritelater == True and argtomemory == False: #if instr will be rewritten later in the block.
                            oldarg = arg
                            arg = ":v" + str(newvariable) #to make a unique variable name for each new variable; using commas
                            #idea cribbed from michael who pointed out that a user probably won't include colon in their
                            #variable names since the type is denoted by colons
                            instr.get("args")[instr.get("args").index(oldarg)] = arg
                            changednewvars[arg] = oldarg


                        rowcount = rowcount+1
                        newvariable+=1
                        cloud[arg] = rowcount
                        table["UNKNOWN" + str(rowcount)] = instr.get("args")[instr.get("args").index(arg)], rowcount


            value = [instr.get("op")]
            if instr.get("args") is not None:
                for arg in instr.get("args"):
                    value.append(arg)

            value = tuple(value)            

      
        ogdest = instr.get("dest")

        if value in table.keys() and instr.get("op") != "alloc" and instr.get("op") != "call" and instr.get("op") != "ptradd": #we've already calculated this, we can reuse it. SHOULD BLACKLIST ALLOC, CALL
            var, num = table[value]

            iscopy = True

            copy = {}
            copy["args"] = [str(var)]
            copy["dest"] = instr.get("dest")
            copy["op"] = "id"
            copy["type"] = instr.get("type")

            block.insert(block.index(instr),copy)
            block.remove(instr)
        else: #new value
            iscopy = False
            rowcount = rowcount+1
            newvariable +=1
            num=rowcount #1 indexing my rows


            rewritelater = False #bool to hold whether the current instruction instr will be rewritten later.
            argtomemory = False #bool to hold whether the current dest var we're considering will be used as an arg in a memory instruction; if so, we shouldn't rename it.
            for laterinstr in block[block.index(instr)+1:]:
                if laterinstr.get("dest") == instr.get("dest"):
                    rewritelater = True
                if laterinstr.get("args") is not None:
                    if instr.get("dest") in laterinstr.get("args") and (laterinstr.get("op") == "alloc" or laterinstr.get("op") == "ptradd"):
                        argtomemory = True
            



            if rewritelater == True and instr.get("op") != "alloc" and instr.get("op") != "call" and "label" not in instr.keys() and "dest" in instr.keys() and "ptr" not in instr.get("type") and argtomemory == False: #if instr will be rewritten later in the block.
                dest = ":v" + str(newvariable) #to make a unique variable name for each new variable; using commas
                #idea cribbed from michael who pointed out that a user probably won't include colon in their
                #variable names since the type is denoted by colons
                instr["dest"] = dest
            else:
                dest = instr.get("dest")
            

            

            arglist = instr.get("args")

            if arglist is not None:
                for arg in arglist: #reconstruction: for arg in instr.args, replace arg with table[cloud[arg]]'s
                #canonical variable

                    if argoutofblock[instr.get("args").index(arg)] == False: #but don't replace it if it's come in from
                    #another block!!
                        
                        ournum = cloud[arg] #row number of canon variable we want
                        canonvar = None
                        for varnum in table.values():
                            currnum = varnum[1] 
                            if currnum == ournum: #if we're in the correctly numbered row
                                canonvar = varnum[0] #let the canon variable we want be this current variable

                        newarg = canonvar #call it newarg since we want to replace each argument with this
                        
                        newvalue = []
                        i = 0
                        while i < len(value):
                            if value[i] == arg:
                                newvalue.append(newarg)
                            else:
                                newvalue.append(value[i])
                            i+=1

                        value = tuple(newvalue)
 
                        arglist.insert(arglist.index(arg), newarg)
                        arglist.remove(arg)


                        if value in table.keys() and instr.get("op") != "alloc" and instr.get("op") != "call" and instr.get("op") != "ptradd": #we've already calculated this, we can reuse it. SHOULD BLACKLIST ALLOC, CALL
                            var, num = table[value]
                            iscopy = True

                            copy = {}
                            copy["args"] = [str(var)]
                            copy["dest"] = instr.get("dest")
                            copy["op"] = "id"
                            copy["type"] = instr.get("type")

                            block.insert(currindex,copy)
                            block.remove(block[currindex+1])

                        
            if iscopy == False:
                if instr.get("op") == "call":
                    table[(value, num)] = dest, num
                else:
                    table[value] = dest, num

        cloud[ogdest] = num


        if instr.get("args") is not None:
            for arg in instr.get("args"):
                if argoutofblock[instr.get("args").index(arg)] == True and arg in changednewvars.keys(): 
                    origarg = changednewvars[arg]
                    instr.get("args")[instr.get("args").index(arg)] = origarg

        





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





if __name__ == '__main__':
    main()

