#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:17:05 2019

Abstract of textprocessing
1. splite lines from origin text file and store them in individual text file.
2. generate log for each line.
3. extract labels
 3-1 for each log file, copy "Output label" part as full label and paste it into new ".lab" file. 
 3-2 for each log file, only copy time information and corresponding phonetic information in "Output label" part as mono label then paste them into new ".lab" file.
4.obtain mono label folder and full label folder which waiting for further use in training session

@author: peng_zaizen
"""

import os
import glob
import shutil

class textPreProcessor:
    """

    """   
    def __init__(self, db_name="normal_daily", origin_text_file="../text.txt", label_path="../label/", splited_text_path="../splited_text/", log_path="../log/"):
        self.__db_name = db_name
        self.__origin_text_file = origin_text_file
        self.__splited_text_path = inputAsPath(splited_text_path)
        self.__log_path = inputAsPath(log_path)
        self.__label_path = inputAsPath(label_path)
        self.__monolabel_path = self.__label_path+"mono/"
        self.__fulllable_path = self.__label_path+"full/"
        buildDirectoryAnyway(self.__splited_text_path)
        buildDirectoryAnyway(self.__log_path)
        buildDirectoryAnyway(self.__label_path)
        buildDirectoryAnyway(self.__monolabel_path)
        buildDirectoryAnyway(self.__fulllable_path)
        
    def __spliteScript(self):
        """
        one line in one textfile
        """   
        line = 0
        f = open(self.__origin_text_file,"r")
        for sentence in f:
            output_txt = open(self.__splited_text_path+self.__db_name+str(line+1)+".txt","w")
            output_txt.write(sentence)
            output_txt.close()
            line = line+1            
        f.close()
       
    def __logGeneration(self): 
        """
        
        """    
        text_file = []       
        text_path_list = glob.glob(self.__splited_text_path+"*")   
        for text_path in text_path_list:  # obtain filename and the filename extention and save them respectely 
            file_name = text_path.split("/")[-1].split(".")
            text_file.append(file_name)      
        for file in text_file:           
            open_jtalk = 'open_jtalk '
            log = ' -ot '+self.__log_path+file[0]
            mech = ' -x '+' /usr/local/dic '
            htsvoice = ' -m '+' /usr/local/share/hts_voice/nitech_jp_atr503_m001.htsvoice '
            outwav = ' -ow ' +'1.wav '
            txtfilename = self.__splited_text_path+file[0]+'.txt '               
            cmd=open_jtalk+log+mech+htsvoice+outwav+txtfilename
            os.system(cmd)

    def __monoLabelMaker(self):
        """
        extract monolabels from log
        """       
        labelfile=".lab"
        copyflag=False
        number=1
        while os.path.exists(self.__log_path+self.__db_name+str(number)): 
            copyflag=False
            f=open(self.__log_path+self.__db_name+str(number))
            line=f.readline()
            while line: 
                mark="Output label"
                space_check=line.strip()
                if mark in line:
                    copyflag=True
                elif len(space_check)==0:
                    copyflag=False
                elif copyflag==True:    
                        lab_write=open(self.__monolabel_path+self.__db_name+str(number)+labelfile,"a")
                        linecut=line.split("+")
                        line1=linecut[0]
                        linecut1=line1.split("-")
                        phoneinfo=linecut1[1]
                        line2=linecut1[0]
                        linecut2=line2.split(" ")
                        subtime1=linecut2[0]
                        subtime2=linecut2[1]
                        timeinfo=subtime1+" "+subtime2+" "
                        monolabline=timeinfo+phoneinfo
                        lab_write.writelines(monolabline)
                        lab_write.writelines("\n")
                        lab_write.close()
                line=f.readline()
            f.close()
            number=number+1

       
                
    def __fullLabelMaker(self):
        """
        extract fulllabels from log
        """
        labelfile=".lab"
        copyflag=False
        number=1
        
        while os.path.exists(self.__log_path+self.__db_name+str(number)): 
            copyflag=False
            f=open(self.__log_path+self.__db_name+str(number))
            line=f.readline()
            while line:       
                startmark="Output label"        #開始判定マーク
                space_mark=line.strip()   #空行判定マーク
                if startmark in line:
                    #print("a")
                    copyflag=True
                elif len(space_mark)==0:
                    #print("b")
                    copyflag=False
                elif copyflag==True:
                        lab_write=open(self.__fulllable_path+self.__db_name+str(number)+labelfile,"a")     #
                        lab_write.writelines(line)
                        lab_write.close()
                line=f.readline()
            f.close()
            number=number+1
           
    def labelProduce(self):
        self.__spliteScript()
        self.__logGeneration()
        self.__monoLabelMaker()
        self.__fullLabelMaker()
        
        
def buildDirectory(folder_path="../label/"):
    """
    Build A New Folder.
    If The Path Exists, The Build Fail . 
    """    
    try:
        os.mkdir(folder_path)
        return True
    except FileExistsError as fe:
        print(folder_path+" Already Existed.")
        return False
    
def buildDirectoryAnyway(folder_path="../label/"): 
    """
    Build A New Folder.
    If The Path Exists, Overwrite ALL In The Old Directory . 
    """
    try:
        os.mkdir(folder_path)
        return True
    except FileExistsError as fe:
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        #print("Though "+folder_path+" Already Existed. Overwrite it anyway")
        return True    

def inputAsPath(path_str):
    path = list(path_str)
    if path[-1] is not '/':
        path.extend('/')
    path_str = ''.join(path)
    return path_str 

#==============================================================================
#sample: 
# 
# def main():          
#     
#     a=textPreProcessor(db_name="nobu",origin_text_file="../text.txt",label_path="../label")
#     a.labelProduce()
#     
# if __name__=="__main__":
#      main()
# 
# 
#==============================================================================
          
           

