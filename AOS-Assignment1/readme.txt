The code is written using Python3. The file transfer takes place using sockets
Dependencies:
    > Python3
Before executing the code:
    > Create a folder named 'clientShared' on the reciever. This is where the files will be downloaded.
    > Ensure port 5000 is available for socket binding
Executing the code:
    > In Linux : sudo python3 fileSharing.py
      In Windows : python fileSharing.py
    > Upon executing the above commands, the user will be presented with a choice for acting as a sender or reciever
    > For sender:
        -The server will start listening for connections.
    > For reciever:
        -If the user wants to add a new friend to the list an option will be provided on execution. The list of all friends is maintained in list.txt file.
        -The user can enter the name and IP of the friends from which it wants to receive the files.
        -From the given list of friends, the user will choose the friend. If the IP is valid and connected the list of all files in shared folder at sender is sent.
        -The reciever can then choose between the list of files and enter the name along with the file extension.
        -If the file is present in the shared folder, it'll be sent over.
    > The code terminates once the reciever successfully downloads the file.
        
Sample output at sender:
    C:\Desktop\Stuff\aosa>python fileSharing.py
    Do you want to send files (S) or recieve files(R)?S
    Enter the path of the shared folderC:\\Desktop\\Stuff\\aosa
    Server Active
    ('127.0.0.1', 52268)
    DP.jpg File Found
    Sending Completed
    ('127.0.0.1', 52276)
    DP.jpg File Found
    Sending Completed
    ('127.0.0.1', 52291)
    DP.jpg File Found
    Sending Completed

Sample output at client:
    C:\Desktop\Stuff\aosa>python fileSharing.py
    Do you want to send files (S) or recieve files(R)?R
    Do you want to add a friend? Y/N?Y
    Your choice is Y
    Enter the name of your friend: me
    Enter your friend's IP address: 127.0.0.1
    The list of your friends is :
    127.0.0.1 : 127.0.0.1
    me : 127.0.0.1
    random : 0.0.0.0
    Enter the name of the friend you want to download files from : me
    Requesting file list from : 127.0.0.1
    ['client.py', 'd.py', 'DP.jpg', 'list.txt', 'readme.txt', 'server.py', 't.pdf', 'DP.jpg']
    Enter Filename to download from server : DP.jpg
    Download Completed

