inferredOne=[]
inferredTwo=[]
realOne=[]
realTwo=[]
inferred=[];
real=[]
# -*- coding: utf-8 -*-
for line in open("infNet-meme-four-word-followee-hour.txt"):
    inferredOne.append(line.split(',')[0])
    inferredTwo.append(line.split(',')[1].split(',')[0])
    inferred.append(str(line.split(',')[0]+','+line.split(',')[1].split(',')[0]))

for line in open("Network-four-word-hour.txt"):
    realOne.append(line.split(',')[0])
    realTwo.append(line.split(',')[1].split('\n')[0])
    real.append(str(line.split(',')[0]+','+line.split(',')[1].split('\n')[0]))


print (float(len(set(real).intersection(set(inferred))))/len(inferred))
print (float(len(set(real).intersection(set(inferred))))/len(real))
print float(len(set(real).intersection(set(inferred))))
