from xlrd import open_workbook
# -*- coding: utf-8 -*-
import numpy
import sys
import scipy;
reload(sys)
all=[]
allUsers=[]
selTags=[]
allTags=[]
counter=0
tagsPropagationUsers=[]
tagsPropagationTimes=[]
finalTagsPropagationUsers=[]
finalTagsPropagationTimes=[]
follows=[]
lastTags=[]
lastTimeMean=[]
lastTimeLast=[]
lastExpectedFk={}
lastUsers=[]
lastTimeStamps=[]
isFourWord={}
seen=[]
seenUsers=[]
timeFormat=3600
underScoreNum=3
sys.setdefaultencoding('UTF8')
book1 = open_workbook('filtered-user-whole.xlsx')
sheet1 = book1.sheet_by_name('Sheet1')
book2 = open_workbook('tags-frequencies.xlsx')
sheet2 = book2.sheet_by_name('Sheet1');
outputFile = open("meme-four-word-fan-hour.txt", 'w');
network=open("Network-four-word-fan-hour.txt",'w');
for line in open("users-mapping-whole.txt"):
    allUsers.append(int(line.split(',')[0]))
for row_index in range(sheet2.nrows):
    if((str)(sheet2.cell(row_index, 0).value).count('_') >= underScoreNum):
      selTags.append((str)(sheet2.cell(row_index, 0).value))
for row_index in range(sheet1.nrows):
  time=int(sheet1.cell(row_index, 0).value)
  user=int(sheet1.cell(row_index, 1).value)
  tags=((str)(sheet1.cell(row_index, 2).value).split(','))
  for tag in tags:
      if(tag in selTags):
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
  users=users[inds]
  times=times[inds]
  if(len(users) >=2 ):
    all=all+list(users)
    lastTags.append(allTags[i])
    lastUsers.append(list((users)))
    lastTimeStamps.append(list(times))
all=list(set(all))
for usr in all:
    ind=allUsers.index(usr)
    outputFile.write(str(ind)+','+str(ind)+'\n')
outputFile.write('\n')
for i in range(len(lastTags)):
        a=""
        a=a+str(counter)+';'
        counter=counter+1
        for us in range(len(lastUsers[i])):
            indxs=allUsers.index(lastUsers[i][us])
            a = a +str(indxs) + "," + str((lastTimeStamps[i][us])/(timeFormat)) + ","
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
             for h in range(len(lastTags)):
                 if int(f) in lastUsers[h] and user in lastUsers[h]:
                     indxFol=lastUsers[h].index(int(f))
                     indxUser=lastUsers[h].index(user)
                     if lastTimeStamps[indxFol] <= lastTimeStamps[indxUser]:
                        tmp=str(allUsers.index(int(f)))+","+str(allUsers.index(user))
                        network.write(tmp+"\n")
                        seen.append(tmp)
                        break
network.close()
