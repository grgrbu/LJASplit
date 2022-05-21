fin = open("final_dbg.gfa", "r")
fout = open("final_dbg_2.gfa", "w")

dict_ch = dict()
dict_ch["A"] = "04"
dict_ch["C"] = "00"
dict_ch["G"] = "06"
dict_ch["T"] = "01"

print("@")

for line in fin.readlines():
    check_digit = False
    check_let = False
    for s in line:
        if '0' <= s <= '9':
            check_digit = True
        if check_digit and (not check_let) and (s in ['A', 'T', 'G', 'C']):
            fout.write(dict_ch[s])
            check_let = True
        else:
            fout.write(s)

print("!")