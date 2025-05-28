#!/usr/bin/python 
import sys

f=open(sys.argv[1], "r")
f1=open(sys.argv[2], "r")

f2=sys.argv[3]

with open(f2, "w") as fp:
    for line in f:
        fp.write(line)
    for line in f1:
        print (line.strip()[1])
        if int(line.split()[1])==0:
            fp.write(line)
