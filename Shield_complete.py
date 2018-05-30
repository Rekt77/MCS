#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import re
import time
import mcs
import random

continue_reading = True
hex_list = range(0,256)
random.shuffle(hex_list)
keyA = list()
keyB = list()

def end_read(signal,frame):
        
    global continue_reading
    #If KeyboardInterrupt Captured, Stop Reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

if __name__=="__main__":

        
        Shield = mcs.mcs()
        

        # Hook the SIGINT
        signal.signal(signal.SIGINT, end_read)

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()

        # Welcoming message
        print "Welcome to the MFRC522 data read example"
        print "Press Ctrl-C to stop."

        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print "Card read UID: "+hex(uid[0])[2:]+":"+hex(uid[1])[2:]+":"+hex(uid[2])[2:]+":"+hex(uid[3])[2:]
            
                # This is the default keys for authentication
                def_keys = [
                            [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
                            [0xA0,0xB0,0xC0,0xD0,0xE0,0xF0],
                            [0xA1,0xB1,0xC1,0xD1,0xE1,0xF1],
                            [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5],
                            [0x64,0x78,0x69,0x61,0x69,0x6E],
                            [0x61,0x75,0x64,0x64,0x69,0x6E],
                            [0x66,0x77,0x63,0x6F,0x69,0x6E]
                           ]

                KeyListA=[[131, 67, 18, 236, 73, 164],
                          [195, 147, 248, 205, 163, 37],
                          [181, 182, 99, 34, 200, 108],
                          [11, 110, 79, 98, 124, 247],
                          [140, 233, 164, 37, 17, 223],
                          [250, 148, 187, 77, 136, 91],
                          [179, 166, 220, 58, 116, 197],
                          [220, 56, 81, 140, 208, 196],
                          [178, 169, 122, 97, 145, 251],
                          [53, 191, 46, 145, 184, 193],
                          [91, 116, 57, 106, 147, 216],
                          [199, 26, 99, 193, 129, 79],
                          [222, 212, 198, 107, 68, 21],
                          [82, 183, 252, 37, 225, 11],
                          [131, 127, 48, 207, 253, 166],
                          [177, 62, 24, 111, 65, 250]]

                KeyListB=[[128, 205, 67, 75, 180, 124],
                          [124, 135, 3, 135, 142, 203],
                          [9, 186, 30, 210, 107, 98],
                          [134, 158, 239, 12, 148, 144],
                          [191, 228, 208, 93, 65, 11],
                          [166, 213, 132, 196, 211, 8],
                          [139, 159, 96, 53, 236, 41],
                          [114, 171, 78, 6, 30, 50],
                          [13, 171, 254, 34, 35, 198],
                          [86, 144, 12, 216, 40, 248],
                          [3, 7, 215, 95, 149, 168],
                          [14, 2, 120, 174, 188, 216],
                          [134, 14, 30, 146, 27, 228],
                          [101, 200, 204, 198, 248, 35],
                          [198, 84, 30, 50, 75, 249],
                          [132, 123, 178, 220, 77, 238]]

                # Store's key for authentication
                my_keys = [0x77,0x77,0x77,0x77,0x77,0x77]
                
                
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, my_keys, uid)

                if status == MIFAREReader.MI_OK:
                            
                    BackData = MIFAREReader.MFRC522_Read(9)
                    fixedData = re.findall("[0-9]{1,3}",str(BackData))
                            
                    # Compare Stored Value with Calced Value
                    crc32Stored = hex(int(fixedData[14]))[2:]+hex(int(fixedData[15]))[2:]
                    crc32Calced = Shield.CRC32_calc(fixedData)

                    if Shield.ValueCheck(crc32Stored,crc32Calced):
                                
                        MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 10, my_keys, uid)
                        BackData = MIFAREReader.MFRC522_Read(10)
                        md5Stored = re.findall("[0-9]{1,3}",str(BackData))

                        
                        if Shield.ValueCheck("".join(Shield.ListtoMD5(md5Stored)),Shield.MD5_calc(fixedData,uid)):
                            templist= list()
                            # Write log
                            for i in range(0,len(fixedData)) :
                                templist.append(int(fixedData[i]))
                                
                            MIFAREReader.MFRC522_Write(8,templist)

                            originBalance=Shield.XOR_lshift_calc(fixedData)

                            # Value Down
                            fixedData=Shield.ValueChange(4000,originBalance)

                                    
                            # Value Up
                            #fixedData = ValueChange(400,1,XOR_calc(fixedData))       

                            # encode Value
                            Shield.XOR_rshift_calc(fixedData)
                                    
                            # Calculate 4byte CRC32
                            crcValue = Shield.CRC32_calc(fixedData)
                                    
                            # Insert calculated CRC-L
                            fixedData[14] = str(int(crcValue[:2],16))

                            # Insert calculated CRC-R
                            fixedData[15] = str(int(crcValue[2:4],16))


                            templist = list()
                            for i in range(0,len(fixedData)) :
                                templist.append(int(fixedData[i]))


                            # Store at Blk9
                            MIFAREReader.MFRC522_Write(9, templist)

                            # Calculate MD5
                            hashValue = Shield.MD5_calc(fixedData,uid)
                                    
                            # Store at Blk10
                            MIFAREReader.MFRC522_Write(10, Shield.MD5tolist(hashValue))


                            MIFAREReader.MFRC522_StopCrypto1()
                            print "finished"
                            time.sleep(5)
                                    
                        else :       
                            print "hash not even"
                            MIFAREReader.MFRC522_StopCrypto1()
                                    
                    else:       
                        print "CRC not even"
                        MIFAREReader.MFRC522_StopCrypto1()
                        
                else :
                        
                    MIFAREReader.MFRC522_StopCrypto1()

                    # Scan for cards    
                    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                    # Get the UID of the card
                    (status,uid) = MIFAREReader.MFRC522_Anticoll()

                    MIFAREReader.MFRC522_SelectTag(uid)
                    
                    # Default key check
                    for keys in def_keys:
                        # Authenticate
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, keys, uid)

                        
                        if status == MIFAREReader.MI_OK:
                            
                            
                            BackData = MIFAREReader.MFRC522_Read(9)
                            fixedData = re.findall("[0-9]{1,3}",str(BackData))

                            templist = list()
                            print "ORIGINAL DATA : "
                            for i in range(0,len(fixedData)):
                                templist.append(hex(int(fixedData[i]))[2:])
                            print templist
                            
                            
                            # Do XOR with 0x33 and 0xBB
                            Shield.XOR_rshift_calc(fixedData)
                            # Calculate 4byte CRC32
                            crcValue = Shield.CRC32_calc(fixedData)
                            
                            # Insert calculated CRC-L
                            fixedData[14] = str(int(crcValue[:2],16))

                            # Insert calculated CRC-R
                            fixedData[15] = str(int(crcValue[2:4],16))

                            # Do MD5 with given string
                            hashValue = Shield.MD5_calc(fixedData,uid)
                            
                            for i in range(0,16) :
                                #Type Casting to str -> int
                                fixedData[i] = int(fixedData[i])
                                
                            MIFAREReader.MFRC522_Write(9, fixedData)

                            templist = list()
                            print "FIXED DATA : "
                            for i in range(0,len(fixedData)):
                                templist.append(hex(int(fixedData[i]))[2:])
                            print templist

                            hashList = Shield.MD5tolist(hashValue)
                                           
                            templist = list()
                            print "HASH VALUE : "
                            for i in range(0,len(hashList)):
                                templist.append(hex(int(hashList[i]))[2:])
                            print templist
                            
                            MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 10, keys, uid)
                            MIFAREReader.MFRC522_Write(10, hashList)
                            
                            
                            #temp key write
                            #MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 11, keys, uid)
                            #MIFAREReader.MFRC522_Write(i,my_keys+[255,7,128,105]+my_keys)
                            MIFAREReader.MFRC522_StopCrypto1()
                            
                            # Key Change Routine
                            for i in range(3,64,4):
                                print i
                                MIFAREReader = MFRC522.MFRC522()
                                # Scan for cards    
                                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                                # Get the UID of the card
                                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                                MIFAREReader.MFRC522_SelectTag(uid)
                                print KeyListA[(i+1)/4-1], uid , KeyListB[(i+1)/4-1]
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, int(i), keys, uid)
                                if i == 11:
                                        MIFAREReader.MFRC522_Write(i,my_keys+[255,7,128,105]+my_keys)
                                        continue
                                        
                                MIFAREReader.MFRC522_Write(i,KeyListA[(i+1)/4-1]+[255,7,128,105]+KeyListB[(i+1)/4-1])
                                MIFAREReader.MFRC522_StopCrypto1()
                            MIFAREReader.MFRC522_StopCrypto1()
                            
                            break

