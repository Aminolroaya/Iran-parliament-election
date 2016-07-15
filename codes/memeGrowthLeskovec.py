from xlrd import open_workbook
# -*- coding: utf-8 -*-
import numpy
import sys
import scipy;
reload(sys)
sys.setdefaultencoding('UTF8')
book1 = open_workbook('filtered-user-whole.xlsx')
sheet1 = book1.sheet_by_name('Sheet1')
book2 = open_workbook('tags-frequencies-new.xlsx')
sheet2 = book2.sheet_by_name('Sheet1');
outputFile = open("meme-growth-5-hour.txt", 'w');
network=open("Network-growth-5-hour.txt",'w');
tmp=[]
index=0
allTags=[]
tagsPropagationUsers=[]
tagsPropagationTimes=[]
finalTagsPropagationUsers=[]
finalTagsPropagationTimes=[]
selTags=[]
allUsers=[]
follows=[]
lastTags=[]
lastTimeMean=[]
lastTimeLast=[]
lastExpectedFk={}
lastUsers=[]
lastTimeStamps=[]
isExpected={}
all=[]
seen=[]
seenUsers=[]
for line in open("users-mapping-whole.txt"):
    allUsers.append(int(line.split(',')[0]))
for row_index in range(sheet2.nrows):
    selTags.append((str)(sheet2.cell(row_index, 0).value))
for row_index in range(sheet1.nrows):
  time=int(sheet1.cell(row_index, 0).value)
  user=int(sheet1.cell(row_index, 1).value)
  tags=((str)(sheet1.cell(row_index, 2).value).split(','))
  for tag in tags:
        if str(tag).encode('UTF8') in allTags:
            index=allTags.index(str(tag).encode('UTF8'))
            if user in tagsPropagationUsers[index]:
                i=tagsPropagationUsers[index].index(int(user))
                tagsPropagationTimes[index][i]=min(tagsPropagationTimes[index][i],time)

            else:
                tagsPropagationUsers[index].append(int(user))
                tagsPropagationTimes[index].append(time)
        else:
            allTags.append(str(tag).encode('UTF8'))
            index=len(allTags)-1
            tagsPropagationUsers.append([])
            tagsPropagationUsers[index].append(int(user))
            tagsPropagationTimes.append([])
            tagsPropagationTimes[index].append(time)

for i in range(len(allTags)):
  users=numpy.array(tagsPropagationUsers[i])
  times=numpy.array(tagsPropagationTimes[i])
  inds=times.argsort()
  countTimeMean=0
  countTimeLast=0
  users=users[inds]
  times=times[inds]
  meanTimes=scipy.mean(times)
  for k in range(len(times)):
      if(times[k] <= meanTimes):
        countTimeMean=countTimeMean+1
  countTimeLast=len(times)
  if(countTimeLast >=5 and allTags[i] in selTags):
    lastTags.append(allTags[i])
    lastTimeMean.append(countTimeMean)
    lastTimeLast.append(countTimeLast)
    lastUsers.append(list((users)))
    lastTimeStamps.append(list(times))
counter=0
for i in range(len(lastTags)):
    fk=[]
    for j in range(len(lastTimeMean)):
        if(lastTimeMean[j] >= lastTimeMean[i]):
            fk.append(lastTimeLast[j])
    if(numpy.median(numpy.array(fk)) <= lastTimeLast[i]):
        print lastTags[i]
        isExpected[i]=1
        all=all+list(lastUsers[i])
    else:
        isExpected[i]=0
all=list(set(all))
for usr in all:
    ind=allUsers.index(usr)
    outputFile.write(str(ind)+','+str(ind)+'\n');
for i in range(len(lastTags)):
    if isExpected[i]==1:
        a=""
        a=a+str(counter)+';'
        counter=counter+1
        for us in range(len(lastUsers[i])):
            indxs=allUsers.index(lastUsers[i][us])
            a = a +str(indxs) + "," + str((lastTimeStamps[i][us])/(3600)) + ","
        a = a.strip(',');
        outputFile.write(a + '\n');
outputFile.close()
for row_index in range(sheet1.nrows):
  follows=str(sheet1.cell(row_index, 3).value).split(',')
  user=int(sheet1.cell(row_index, 1).value)
  if user not in seenUsers:
   seenUsers.append(user)
   if(user in all and user in allUsers):
      for f in follows:
          if int(f) in all and int(f) in allUsers and str(allUsers.index(int(f)))+","+str(allUsers.index(user)) not in seen:
             tmp=str(allUsers.index(int(f)))+","+str(allUsers.index(user))
             network.write(tmp+"\n")
             seen.append(tmp)
network.close()






