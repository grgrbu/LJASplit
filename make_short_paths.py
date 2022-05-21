fin = open("./paths.als", "r")
fout = open("./paths_short.als", "w")

i = 0
for line in fin.readlines():
    i += 1
    fout.write(line)
    print(line)
    if i > 105:
        break