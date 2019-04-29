# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:45:15 2018

@author: David
"""
import datetime

file = r'd:/output.rch'
initial_date = datetime.date(2013, 1, 1)

flows = []
reaches = []
dates = []

from_file = open(file, 'r')
lines = from_file.readlines()[9:]
for i in lines:
    line = i.split()
    flows.append(line[6])
    reaches.append(line[1])

geral = [flows, reaches]

iterator = 0
while iterator<len(flows):
    datex = initial_date + datetime.timedelta(days=iterator)
    dates.append(datex)
    iterator = iterator+1

        
        