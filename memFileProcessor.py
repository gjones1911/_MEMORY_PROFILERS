from sys import argv


filename = r'./RF_lblmem2.txt'
if len(argv) > 1: 
    filename= argv[1]

# open the log file and get the lines
f = open(filename, 'r')
lines = f.readlines()
f.close()

# get the total number of lines and the total number of memory for it
print("There are {} tracked memory operations: ".format(len(lines)))


maxsk = 100000
skDict = {}
otherDict = {}

# number of time to disply the results
count = 10
sklearnT,tot,  pytot = 0, 0, 0


for line in lines:
    if count > 0:
        print("line: {}".format(line))
    szif = line[line.find("size="): ]
    szi = line[line.find("size="): ].split(" ")[0].split("=")
    cntr = line[line.find("count=")].split(" ")[0].split("=")
    if count > 0:
        print('size: {}'.format(szi))
        print("Big strings: {}".format(szif))
        print("count: {}".format(cntr))
    if "python" in line:
        
        if count > 0:
            print("python line...")
        if "sklearn" in line:
            pytot += int(szi[1])
            
            if count > 0:
                print("a sklearn line")
            if len(szi) ==2:
                sklearnT += int(szi[1])
    else:
        if count > 0:
            print("some other kind of operation")
    count -=1
    if len(szi) == 2:
        tot += int(szi[1])




print('total: {}, sklearn: {}, python: {}'.format(tot, sklearnT, pytot))
print('% sklearn: {}, python: {}'.format(sklearnT/tot, pytot/tot))
