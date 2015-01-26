# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Implementation of a simple database class."""

import random


class Database(object):

    dataArray=[]
    rand=0
    
    def __init__(self, db_file):
        self.db_file = db_file
        
        readFile = open(self.db_file)
        self.dataArray=readFile.read().split('\n%\n')
        self.dataArray.pop()
        
        readFile.close()
        
        pass

    def read(self):
        random.seed()
        self.rand = random.randint(0,len(self.dataArray)-1)
        
        return self.dataArray[self.rand]
        
        pass

    def write(self, fortune):
        
        self.dataArray.append(fortune)
        
        writeFile=open(self.db_file,"a")
        writeFile.write(fortune + "\n%\n")
        writeFile.close()
        
        pass
