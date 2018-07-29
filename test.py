#!/usr/bin/python
from __future__ import print_function

import os
import random

def getFileSize(filename):
  return os.stat(filename).st_size

def checkIsSorted(filename):
  with open(filename) as f:
    lastNum = int(f.readline())
    for line in f:
      if int(line) < lastNum:
        print('not sorted!')
        return
      lastNum = int(line)
  print('is sorted!')

#took 4:11 to create chunks from 1.5gb file
def createData(chunkSize):
  chunkid = 0
  with open('data.txt','r') as f:
    line = f.readline()
    chunkFP = open('chunk{}.txt'.format(chunkid),'w+')
    currSize = 0
    while line:
      if currSize < chunkSize:
        chunkFP.write(line)
        currSize = chunkFP.tell()
      else:
        chunkFP.close()
        currSize = 0
        chunkid += 1
        chunkFP = open('chunk{}.txt'.format(chunkid),'w+')
      line = f.readline()
  chunkFP.close()


#checkIsSorted('numbers.txt')
#checkIsSorted('data.txt')

#1)split file into separate files
fsize = os.stat('data.txt').st_size
n = 1
while fsize / n > 100000000: n += 1
print('will split into {} chunks of {} size'.format(n,fsize/n))
chunkSize = fsize / n

dataCreated = False
if os.path.exists('chunk0.txt'):
  print('already created data!')
  dataCreated = True

if not dataCreated:
  createData(chunkSize)

#2) sort each individual file
for i in range(n):
  print('sorting chunk {}'.format(i))
  lines = []
  with open('chunk{}.txt'.format(i),'r') as f:
    line = f.readline()
    while line:
      lines.append(int(line))
      line = line.readline()
    sorted(lines)
  with open('chunk{}.txt'.format(i),'w+') as f:
    for line in lines:
      f.write(str(line) + '\n')
