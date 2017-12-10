#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import binascii
import hashlib


class mcs:


    def XOR_rshift_calc(self, DataList):

        balance = ""
        if isinstance(DataList[0],str):
            if len(hex(int(DataList[1]))) == 4 and len(hex(int(DataList[0]))) == 4:
                balance = hex(int(DataList[1]))[2:]+hex(int(DataList[0]))[2:]
                
            elif len(DataList[1]) == 3:
                balance = hex(int(DataList[1]))[2:]+"0"+hex(int(DataList[0]))[2:]

            elif len(DataList[0]) == 3:
                balance = "0"+hex(int(DataList[1]))[2:]+hex(int(DataList[0]))[2:]
                
            else :
                balance = "0"+hex(int(DataList[1]))[2:]+"0"+hex(int(DataList[0]))[2:]
            
        else :
            if len(hex(DataList[1])) == 4 and len(hex(DataList[0])) == 4:
                balance = hex(DataList[1])[2:]+hex(DataList[0])[2:]
                
            elif len(hex(DataList[1])) == 3:
                balance = hex(DataList[1])[2:]+"0"+hex(DataList[0])[2:]

            elif len(hex(DataList[0])) == 3:
                balance = "0"+hex(DataList[1])[2:]+hex(DataList[0])[2:]
                
            else :
                balance = "0"+hex(DataList[1])+ "0"+hex(DataList[0])


        
        balance = hex((int(balance,16)>>5)^0x88)[2:]

        if len(balance) == 3 :

            DataList[0] = str(int(balance[1:],16))
            DataList[1] = str(int(balance[0],16))

        else :
            DataList[0] = str(int(balance[2:],16))
            DataList[1] = str(int(balance[:2],16))


    def XOR_lshift_calc(self, DataList):

        DataList[0] = hex(int(DataList[0]))
        print DataList
        DataList[1] = hex(int(DataList[1]))
        print DataList
        balance = ""
        if len(DataList[0])==4 and len(DataList[1])==4 :
            balance = DataList[1][2:]+DataList[0][2:]
            
        elif len(DataList[1])==4 :
            balance = DataList[1][2:]+"0"+DataList[0][2:]
            
        elif len(DataList[0])==4 :
            balance = "0"+DataList[1][2:]+DataList[0][2:]
            
        else :
            balance = "0"+DataList[1][2:]+"0"+DataList[0][2:]
        print balance
        balance = hex(((((int(balance,16)^0x88)<<5)+32)/100)*100)[2:]


        return balance

        
    def CRC32_calc(self, DataList):

        if isinstance(DataList[0],int):
            for i in range(0,len(DataList)):
                DataList[i] = str(DataList[i])

        CrcString = "".join(DataList[:14])
        Crc = hex(binascii.crc32(CrcString)^0xFFFFFFFF)

        # If signbit is 0
        if len(Crc) == 11:
            return Crc[2:-1][:4]


        # If signbit is 1
        elif len(Crc) == 12:    
            return Crc[3:-1][:4]

    def ValueCheck(self, Calced,Stored):

        return Calced == Stored


    def MD5_calc(self, Datalist,uid):

        StringUid = ""
        
        for i in range(0,len(uid)):
            temp = hex(uid[i])[2:]
            if len(temp) == 1:
                temp = "0"+temp
            StringUid+= temp
            
        return hashlib.md5("".join(Datalist)+StringUid).hexdigest()

    def MD5tolist(self, hash_):
        
        emptyBucket = list()
        
        for i in range(0,len(hash_),2):
            emptyBucket.append(int(hash_[i:i+2],16))
        return emptyBucket

    def ListtoMD5(self, DataList):
        hashString = ""
        
        for i in range(0,len(DataList)):
            temp=hex(int(DataList[i]))[2:]
            if len(temp)==1:
                temp = "0"+temp
            hashString += temp

        return hashString

    def ValueChange(self, value,balance):

        dummyList = ["0"]*16
        
        balance = int(balance,16)
        if balance-value >= 0 :
            #hex balance
            balance = hex(balance-value)[2:]
            
            if len(balance) == 3:

                dummyList[0] = str(int(balance[1:],16))
                dummyList[1] = str(int(balance[0],16))

                return dummyList

            else :
                    
                dummyList[0] = str(int(balance[2:],16))
                dummyList[1] = str(int(balance[:2],16))

                return dummyList
