import os, re
from tkinter.filedialog import askopenfile


lexemes_dict = {'^HAI$': 'Code Delimiter',
            '^KTHXBYE$': 'Code Delimiter',
            '^I HAS A$': 'Variable Declaration',
            '^HOW IZ I$': 'Function Declaration',
            '^ITZ$': 'Variable Assignment',
            '^VISIBLE$': 'Output Keyword',
            '^0$|^\\-?[1-9][0-9]*$' : 'Literal',
            '^".*"$' : 'Literal'
            }

identifier = '^[a-zA-Z][a-zA-Z0-9\\_]*$'

lexemes_result = {}

def lexicalAnalyzer(line):
    terms = line.split()                # pinaghihiwalay yung line into separate terms

    var_flag = 0
    func_flag = 0
    loop_flag = 0
    i = 0

    while i < len(terms):

        if var_flag or func_flag or loop_flag:                          # if yung before ng current term ay variable/function/loop declaration
            if var_flag and re.match(identifier, terms[i]):
                lexemes_result[terms[i]] = "Variable Identifier"        # inaadd sa dictionary ng result
                var_flag = 0
            elif func_flag and re.match(identifier, terms[i]):
                lexemes_result[terms[i]] = "Function Identifier"
                func_flag = 0
            elif loop_flag and re.match(identifier, terms[i]):
                lexemes_result[terms[i]] = "Loop Identifier"
                loop_flag = 0

        else:                                                           # if not preceded by a declaration
            matching = 0
            for j in lexemes_dict:                                      # if may kamatch sa dictionary
                if re.match(j, terms[i]):
                    matching += 1
                    break
            
            if matching:
                lexemes_result[terms[i]] = lexemes_dict[j]              # inaadd sa dictionary ng result

                if lexemes_dict[j] == "Variable Declaration":           # if ang current na term ay declaration
                    var_flag += 1
                elif lexemes_dict[j] == "Function Declaration":
                    func_flag += 1
                elif lexemes_dict[j] == "Loop Declaration":
                    loop_flag += 1
            else:                                                                   # if wala sa dictionary (kailangan iconcatenate with mga sumunod na terms)
                temp = [terms[i]]

                for k in range(i+1, len(terms)):
                    temp.append(terms[k])
                    x = " ".join(temp)                                              # pinagdidikit yung mga terms

                    matching = 0
                    for j in lexemes_dict:
                        if re.match(j, x):                                          # if may kamatch na sa dictionary
                            matching += 1
                            break

                    if matching:
                        lexemes_result[x] = lexemes_dict[j]

                        if lexemes_dict[j] == "Variable Declaration":               # if ang current na term ay declaration
                            var_flag += 1
                        elif lexemes_dict[j] == "Function Declaration":
                            func_flag += 1
                        elif lexemes_dict[j] == "Loop Declaration":
                            loop_flag += 1
                        i = i+k
                        break

        i += 1





file = askopenfile(mode ='r', filetypes =[('LOL Files', '*.lol')])              # gets input file

if file is None:
    print("ERROR: Invalid file\n")                                              # exits if invalid
    exit(1)

filepath = os.path.abspath(file.name)
f = open(filepath, "r")                                                         # opens the file for reading
content = f.read()
lines = content.splitlines()
lines = [x.strip() for x in lines]

for line in lines:
    lexicalAnalyzer(line)                           # tinatawag yung function kada line

for x in lexemes_result:
    print(f"{x:<15} {lexemes_result[x]}")           # piniprint yung lexemes with label
