import os
import socket
import pickle
from threading import Thread
import _thread
import sys

'''
If a friend wants to send file he can opt for S. If the peer wants to recieve the file from opt for R
''' 
ch = input("Do you want to send files (S) or recieve files(R)?")
while(ch.lower()!='s' and ch.lower()!='r'):
    print("Invalid option! Try again!!")
    ch = input("Do you want to send files (S) or recieve files(R)?")

#Sender code
if(ch.lower() == 's'):
    #Path of the shared folder that the friend wants to send files from
    workingdir = "Shared/"
    #Socket connection for every thread.
    def new_conn(Content,Address):
        listOfFiles = []
        #Traverse the whole shared folder for sending the list of files. This also includes the nested files(Files inside the folder)
        for subdir, dirs, files in os.walk(workingdir):
            for file in files:
                listOfFiles.append(os.path.join(file))
        data=pickle.dumps(listOfFiles)
        #Sending the list of files to the client
        Content.send(data)
        print(Address)
        bFileFound = 0
        listOfFiles = []
        #Recieving the name of the file client is requesting
        sFileName = Content.recv(1024)
        sFileName = sFileName.decode()
        for subdir, dirs, files in os.walk(workingdir):
            for file in files:
                if file == sFileName:
                    fileLoc = subdir+"/"+sFileName
                    bFileFound = 1
                    break

        if bFileFound == 0:
            print(sFileName + " Not Found On Server")
            Content.send("Error".encode('utf-8'))

        else:
            print(sFileName + " File Found")
            fUploadFile = open(fileLoc, "rb")
            sRead = fUploadFile.read(1024)
            while sRead:
                Content.send(sRead)
                sRead = fUploadFile.read(1024)
            print("Sending Completed")
        Content.close()

    host = ''
    try:
        skServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        skServer.bind((host, 5000))
    except socket.error:
        print("Error creating socket")
        exit(1)
        
    threads = []
    skServer.listen(10)
    print("Server Active")

    fileLoc = ""

#The sender is listening for connections. For each connection received it creates a new thread to handle the connection.
    while True:
        Content, Address = skServer.accept()
        _thread.start_new_thread(new_conn,(Content,Address))

    skServer.close()

#Reciever code
elif(ch.lower() == 'r'):
    friends={}
    #Add and retrieve the list fo friends
    ch = input("Do you want to add a friend? Y/N?")
    print("Your choice is {}".format(ch))
    while(ch.lower()!='y' and ch.lower()!='n'):
        print("Incorrect choice! Try again!")
        ch = input("Do you want to add a friend? Y/N?")
    if(ch.lower()=='y'):
        name = input("Enter the name of your friend: ")
        IP = input("Enter your friend's IP address: ")
        f=open("list.txt", "a+")
        f.write(name+":"+IP+"\n")
        f.close()

    f = open("list.txt", "r")
    while(True):
        print("The list of your friends is : ")
        for x in f:
            key, value = x.split(":")
            friends[key]=value[0:-1]

        for friend in friends:
            print("{} : {}".format(friend,friends.get(friend)))

        fr = input("Enter the name of the friend you want to download files from : ")
        while(fr not in friends):
            print("The friend you mentioned is not in your list. Choose a friend from the list.")
            fr = input("Enter the name of the friend you want to download files from : ")
        print("Requesting file list from : {}".format(friends[fr]))

        #Socket connection code
        try:
            skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            skClient.settimeout(5)
            skClient.connect((friends[fr], 5000))
        except socket.error:
            print (" Problem in socket connection. Please check the IP of your friend and it's connectivity")
            exit(1)
        
        wd = "clientShared/"
        listOfFiles = []
        recvd_data = skClient.recv(1024)
        listOfFiles = pickle.loads(recvd_data)

        print(listOfFiles)
        fName = input("Enter Filename to download from server : ")
        while(fName not in listOfFiles):
            print("No such file exists! Try another file...")
            fName = input("Enter Filename to download from server : ")
        sFileName = str.encode(fName)
        sData = "Temp"
        while True:
            skClient.send(sFileName)
            sData = skClient.recv(1024)
            sFileName = sFileName.decode()
            fDownloadFile = open(wd + sFileName, "wb")
            while sData:
                fDownloadFile.write(sData)
                sData = skClient.recv(1024)
            print("Download Completed")
            skClient.close()
            break
        tada = input("Do you want to receive more files?Y/N")
        if(tada.lower()=='n'):
            break
