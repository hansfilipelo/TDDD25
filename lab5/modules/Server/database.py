# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

#"""Implementation of a simple database class."""

import random
import sys
from Server.Lock.distributedReadWriteLock import DistributedReadWriteLock
from Common.protocols_utilities import DatabaseError

class Database(object):

    dataArray=[]
    rand=0
    rwLock = ""
    
    def __init__(self, db_file, rwLock):
        self.rwLock = rwLock
        self.db_file = db_file
        
        readFile = open(self.db_file)
        self.dataArray=readFile.read().split('\n%\n')
        self.dataArray.pop()
        
        readFile.close()
        
    
    def read(self):
        try:
            self.rwLock.read_acquire()
            
            try:
                random.seed() # Re-seed random number generator
                self.rand = random.randint(0,len(self.dataArray)-1)
                outData = self.dataArray[self.rand] # read
                
                self.rwLock.read_release()
                return outData
            except:
                self.rwLock.read_release()
                raise DatabaseError()
        except:
            raise DatabaseError()
    
    def write(self, fortune):
        try:
            self.dataArray.append(fortune)
            
            writeFile=open(self.db_file,"a")
            writeFile.write(fortune + "\n%\n")
            writeFile.close()
            
        except Exception as e:
            self.rwLock.write_release()
            raise getattr(sys.modules[__name__], type(e).__name__)(e.args)
            
    def write_no_lock(self,fortune):
        try:
            self.dataArray.append(fortune)
            
            writeFile=open(self.db_file,"a")
            writeFile.write(fortune + "\n%\n")
            writeFile.close()
        except:
            raise getattr(sys.modules[__name__], type(e).__name__)(*e.args)
