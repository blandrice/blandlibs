import os
import argparse
from glob import glob
import re
pypath = os.path.dirname(os.path.abspath(__file__))
libspath = os.path.abspath(os.path.join(pypath, '..', 'libs'))
outpath = os.path.abspath(os.path.join(pypath, '..', 'out'))
temppath = os.path.abspath(os.path.join(pypath, '..', 'temp'))
if not os.path.exists(temppath):
    os.mkdir(temppath)

global libslist
libslist = []

global includedlibs
includedlibs = []

global gbl_pubactions
gbl_pubactions = []

global gbl_pubargs
gbl_pubargs = []

global gbl_privactions
gbl_privactions = []

global gbl_privargs
gbl_privargs = []

global indentstr
indentstr = "    "


def listkrunkfiles(path):
    global libslist
    if not len(libslist):
        libslist = [y for x in os.walk(path)
                    for y in glob(os.path.join(x[0], '*.krnk'))]
    return libslist


def findlibpath(klibname):
    libs = listkrunkfiles(libspath)
    libshort = [os.path.basename(lib) for lib in libs]
    # print(libshort)
    if not klibname in libshort:
        print("ERROR: {} lib not found in libs path {}".format(klibname, libspath))
        exit()
    else:
        return libs[libshort.index(klibname)]


def reformatlibfile(libpath, klibname):
    libobj = {
        "libfile": "",
        "pubactions": [],
        "pubaction_args": [],
        "privactions": [],
        "privaction_args": []
    }
    # templibpath = os.path.join(temppath, "temp_" + klibname+".krnk")
    templibpath = libpath
    # once intermediate file (with all includes replaced) is created, do reformat
    # find all global vars and actions
    with open(libpath, 'r') as flib:
        bracketstack = ""
        openbracks = ['[', '(', '{']
        closebracks = [']', ')', '}']

        # globalvars
        globalvars = []
        # globalactions
        globalactions = []
        pubactions = []
        pubaction_args = []
        privactions = []
        privaction_args = []

        # for line in flib:
        for idx, line in enumerate(flib):
            # print(line)
            # match a variable

            # find globals (not in brackets)
            if not bracketstack:
                # find variables
                for vartype in ['num', 'str', 'bool', 'obj']:
                    m = re.search(
                        r"(^\s*\b{}\b)\s*(\[\])*\s*(.+?)\s?=\s*(.*)\s*".format(vartype), line.strip().replace(";", ""))
                    if m:
                        # print(m.group(1), m.group(3), m.group(4))
                        globalvars.append(m.group(3))
                        pass
                # find method names
                for vartype in ['num', 'str', 'bool', 'obj', 'public', "private", ""]:
                    m = re.findall(
                        r"^\s*(\b{}\b)\s*(\[\])*\s*action\s*(.*)(\()(.*)(\)).*$|^(\b{}\b)\s*(\[\])*\s*action\s*(.*).*$".format(vartype, vartype, vartype), line.strip())
                    if m:
                        funcname = ''
                        funcargs = ''
                        if '(' in m[0]:
                            funcname = m[0][m[0].index('(')-1].replace("(", "")
                            funcargs = m[0][m[0].index('(')+1]
                        else:
                            funcname = m[0][-1].replace("(", "")
                        # print(funcname)
                        # print(line)
                        if vartype == "public":
                            pubactions.append(funcname)
                            pubaction_args.append(funcargs)
                        elif vartype == "private":
                            privactions.append(funcname)
                            privaction_args.append(funcargs)
                        else:
                            globalactions.append(funcname)

            # detect if you are in a bracket
            brackstr = re.findall(r"([\[{(\]})])", line.strip())
            for brack in brackstr:
                if brack in openbracks:
                    bracketstack += brack
                elif brack in closebracks:
                    # match the close bracket with the open bracket
                    if bracketstack and (openbracks.index(bracketstack[-1]) == closebracks.index(brack)):
                        bracketstack = bracketstack[:-1]  # pop the bracket
                    else:
                        print("ERROR: {}".format(libpath))
                        print("\tunmatched bracket {} in line {}: {}".format(
                            brack, idx+1, line))
                        print(bracketstack)
                        exit()

    text_file = open(libpath, "r")
    # read whole file to a string
    newText = text_file.read()
    # close file
    text_file.close()
    # print(newText)
    # print(globalvars)
    # print(klibname)
    for var in globalvars:
        # newText = newText.replace(var, klibname+"_"+var)
        newText = re.sub(
            r'(?<![a-zA-Z0-9_.]){}(?![a-zA-Z0-9_])'.format(var), klibname+"_"+var, newText)
    # print(globalactions)
    for act in globalactions:
        newText = re.sub(
            r'(?<![a-zA-Z0-9_.]){}(?![a-zA-Z0-9_])'.format(act), klibname+"_"+act, newText)
    # print(pubactions)
    for act in pubactions:
        newText = re.sub('public\s*action\s*(?<![a-zA-Z0-9_]){}(?![a-zA-Z0-9_])'.format(
            act), "action " + klibname+"_"+act, newText)
    for act in privactions:
        newText = re.sub('private\s*action\s*(?<![a-zA-Z0-9_]){}(?![a-zA-Z0-9_])'.format(
            act), "action " + klibname+"_"+act, newText)

    lines = newText.split("\n")
    lines_with_include_replaced = []
    for idx, line in enumerate(lines):
        includelines = checkinclude(line,idx, libpath)
        if includelines:
            lines_with_include_replaced += includelines.split("\n")
        else:
            lines_with_include_replaced.append(line)

    libobj["libfile"] = '\n'.join(lines_with_include_replaced)
    # libobj["libfile"] = newText
    # print(newText)
    libobj["pubactions"] = [klibname+"_"+act for act in pubactions]
    libobj["pubaction_args"] = pubaction_args
    libobj["privactions"] = [klibname+"_"+act for act in privactions]
    libobj["privaction_args"] = privaction_args

    # templibpath = os.path.join(temppath, "temp_" + klibname+".krnk")

    # # check includes and replace all
    # with open(libpath, 'r') as flib:
    #     with open(templibpath, 'w') as ftemp:
    #         for idx, line in enumerate(flib):
    #             includelines = checkinclude(line, libpath)
    #             if includelines:
    #                 ftemp.write(includelines)
    #             else:
    #                 ftemp.write(line)
    return libobj


def checkinclude(line,idx, filepath):
    # search and replace #include<lib.krnk>
    global includedlibs
    global gbl_pubactions
    global gbl_pubargs
    global gbl_privactions
    global gbl_privargs

    if line.strip().startswith("#include"):
        m = re.search("#include\s*<(.+?.krnk)>", line)
        if not (m):
            print("WARNING: #include format not correct.")
            # print(""+ str(idx) + ": " + line.strip())
            print("\t\tline {}: {}".format(idx+1, line.strip()))
            print("\t\tExpected format: #include <yourlibname.krnk>")
        elif m.group(1) in includedlibs:
            print("Warn: already included lib once: {}".format(m.group(1)))
            print("\tFile: {}".format(filepath))
        else:
            includedlibs.append(m.group(1))
            klibname = m.group(1)
            libpath = findlibpath(klibname)
            libobj = reformatlibfile(libpath, klibname.split(".")[0])

            # print(libobj["libfile"])
            # write out file
            gbl_pubactions = gbl_pubactions + libobj["pubactions"]
            gbl_pubargs = gbl_pubargs + libobj["pubaction_args"]
            gbl_privactions = gbl_privactions + libobj["privactions"]
            gbl_privargs = gbl_privargs + libobj["privaction_args"]
            return libobj["libfile"]

    return False


def main():
    parser = argparse.ArgumentParser(
        description='bandrice\'s custom library compiler')
    parser.add_argument('script', nargs='?', help='script to compile')
    args = parser.parse_args()

    if not (args.script.endswith(".krnk") or args.script.endswith(".txt")):
        print("Error: input file does not end with .krnk or .txt:")
        print("\t{}".format(args.script))
        exit()

    # all includes here
    tempfilename = os.path.join(temppath, os.path.basename(args.script))
    outputfilename = os.path.join(
        outpath, "f_" + os.path.basename(args.script))
    finaloutputfilename = os.path.join(
        outpath, "o_" + os.path.basename(args.script))
    outputprivfilename = os.path.join(
        outpath, "op_" + os.path.basename(args.script))
    with open(args.script, 'r') as fscript:
        with open(tempfilename, 'w') as tempscript:
            for idx, line in enumerate(fscript):
                includelines = checkinclude(line,idx, tempfilename)
                if includelines:
                    tempscript.write(includelines)
                    tempscript.write('\n')
                else:
                    tempscript.write(line)

    global gbl_pubactions
    global gbl_pubargs
    global gbl_privactions
    global gbl_privargs
    global indentstr
    # place public actions from libraries into the main script
    # start bracket search () {
    # prepend any public actions from other libs
    # add rest of public action contents from current lib

    otherlibpubactions = []
    otherlibprivactions = []
    with open(tempfilename, 'r') as tempscript:
        with open(outputfilename, 'w') as outscript:
            state = "none"
            startbrack = 0
            endbrack = 0
            bracketstack = ""
            openbracks = ['[', '(', '{']
            closebracks = [']', ')', '}']
            actionargs = ""
            actioncontents = ""
            actionname = ""
            strargs = ""
            trailingstr = ""
            privatelines = []

            for idx, line in enumerate(tempscript):
                if state == "none":
                    for acttype in ['public', 'private']:
                        m = re.findall(
                            r"^\s*(\b{}\b)\s*(\[\])*\s*action\s*(.*)(\()(.*)\).*$".format(acttype), line.strip())
                        if m:
                            state = "parseargs"
                            # print(m)
                            actiontype = acttype
                            actionname = m[0][2]
                            strargs = m[0][4]
                            break
                    else:
                        outscript.write(line)
                for char in line:
                    if state == "parseargs":
                        if char in openbracks:
                            bracketstack += char
                            if startbrack == endbrack:
                                startbrack += 1
                        elif bracketstack and char in closebracks:
                            if openbracks.index(bracketstack[-1]) == closebracks.index(char):
                                # pop the bracket
                                bracketstack = bracketstack[:-1]
                                if bracketstack == "":
                                    endbrack += 1
                                    state = "parseactcontents"
                                    continue
                            else:
                                print("ERROR: {}".format(tempfilename))
                                print("\tunmatched bracket {} in line {}: {}".format(
                                    char, idx+1, line))
                                print(bracketstack)
                                exit()
                        elif startbrack > endbrack:
                            actionargs += char
                    if state == "parseactcontents":
                        if bracketstack and char in closebracks:
                            if openbracks.index(bracketstack[-1]) == closebracks.index(char):
                                # pop the bracket
                                bracketstack = bracketstack[:-1]
                                if bracketstack == "":
                                    endbrack += 1
                                    state = "save"
                                    trailingstr = line[idx:]
                        if startbrack > endbrack:
                            actioncontents += char
                        if char in openbracks:
                            bracketstack += char
                            if startbrack == endbrack:
                                startbrack += 1

                    # test
                    if state == "save":
                        outscript.write("{} action {}({})".format(actiontype,
                                                                  actionname, strargs) + "{\n")
                        libactions = []
                        tgbl_pubactions = gbl_pubactions.copy()
                        for x in reversed(tgbl_pubactions):
                            if x.endswith(actionname):
                                libactions.append(x)
                                del gbl_pubargs[gbl_pubactions.index(x)]
                                gbl_pubactions.remove(x)
                        tgbl_privactions = gbl_privactions.copy()
                        for x in reversed(tgbl_privactions):
                            if x.endswith(actionname):
                                libactions.append(x)
                                del gbl_privargs[gbl_privactions.index(x)]
                                gbl_privactions.remove(x)

                        for x in reversed(libactions):
                            invokelibstr = re.compile(
                                r"(?<![a-zA-Z0-9_])(\bobj\b|\bstr\b|\bnum\b|\bbool\b|\[\s*\])(?![a-zA-Z0-9_])").sub("", strargs)
                            outscript.write(
                                "{}{}({});\n".format(indentstr, x, invokelibstr.strip()))
                        outscript.write(actioncontents + "\n}\n")

                        outscript.write(trailingstr)
                        state = "finish"
                    if state == "finish":
                        actionargs = ""
                        actioncontents = ""
                        actionname = ""
                        strargs = ""
                        trailingstr = ""
                        state = "none"
                        break

            # if public action does not exist in main file - need to create it and prepend libraries' public actions

            otherlibpubactions = set([x.split("_")[-1]
                                     for x in gbl_pubactions])
            otherlibprivactions = set([x.split("_")[-1]
                                       for x in gbl_privactions])
            if otherlibpubactions or otherlibprivactions:
                outscript.write("\n\n")

                def autowrite(otherlibactions, gblactions, gblargs, prefix,output):
                    for x in otherlibactions:
                        # lookup the arguments
                        currentargs = ""
                        for g in gblactions:
                            if g.endswith(x):
                                currentargs = gblargs[gblactions.index(g)]
                                break
                        # write out top level public action definition
                        output.write(
                            "{} action {} ({})".format(prefix, x, currentargs) + "{\n")
                        # invoke separate lib public actions
                        for gblact in gblactions:
                            if gblact.endswith(x):
                                # outscript.write("public action {} ({}) {" + gblact,)
                                currentargs = gblargs[gblactions.index(
                                    gblact)]
                                invokelibstr = re.compile(
                                    r"(?<![a-zA-Z0-9_])(\bobj\b|\bstr\b|\bnum\b|\bbool\b|\b\[\s*\]\b)(?![a-zA-Z0-9_])").sub("", currentargs)
                                output.write(
                                    "{}{}({});\n".format(indentstr, gblact, invokelibstr.strip()).replace('[]', ""))
                        # end curly bracket
                        output.write("}\n\n")

                if otherlibprivactions:
                    with open(outputprivfilename, 'w') as tempoutscript:
                        autowrite(otherlibprivactions,
                                gbl_privactions, gbl_privargs, "",tempoutscript)
                outscript.write(
                    "# ================================================================\n")
                outscript.write(
                    "# auto-detected public actions from libraries\n")
                outscript.write(
                    "# ================================================================\n")
                autowrite(otherlibpubactions, gbl_pubactions,
                          gbl_pubargs, "public",outscript)
        
        newText = ""
        
        text_file = open(outputfilename, "r")
        # read whole file to a string
        newText = text_file.read()
        # close file
        text_file.close()

        if otherlibprivactions:
            
            text_file = open(outputprivfilename, "r")
            # read whole file to a string
            privText = text_file.read()
            # close file
            text_file.close()

            newText = newText.replace("#privateactions", privText)

        with open(finaloutputfilename,'w') as file:
                file.write(newText)
        

    # print(gbl_pubactions)
    print("Done! ")
    # print("\t" + outputprivfilename)
    # print("\t" + outputfilename)
    print("\t" + finaloutputfilename)


if __name__ == "__main__":
    main()
