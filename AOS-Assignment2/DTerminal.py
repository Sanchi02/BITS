import sys, socket, subprocess
import pickle
import struct

# Sending messages in packets
def sendMessage(conn, msg):
    msg = struct.pack('>I', len(msg)) + msg
    conn.sendall(msg)

# Receving packets and unpacking them
def recvMessage(conn):
    raw_msglen = recvall(conn, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(conn, msglen)

# Helper function for receiving bytes / None in case of end of file
def recvall(conn, n):
    data = bytearray()
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

port = 50104
socksize = 4096

def server():
    host = ''

    # Socket connection code
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host, port))

    print("Server started on port: {}".format(port))
    s.listen(1)
    print("Now listening...\n")

    while True:
        try:
            conn, addr = s.accept()
            print('New connection from {}:{}'.format(addr[0], addr[1]))
            data = recvMessage(conn)
            # Deserializing the dictionary
            data = pickle.loads(data)
            # Extracting output of previous command and command from the dictionary
            dict_cmd = data
            cmd = dict_cmd.get(2)
            # For the first command there won't be any input hence first part would consist on NONE
            if(dict_cmd.get(1) == None):
                try:
                    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as exc:
                    print("Status : FAIL", exc.returncode, exc.output)
                else:
                    tuple1 = proc.communicate()
            else:
                tmp = dict_cmd.get(1)
                # Output of previous command typecasted
                tmp = str(tmp, "utf-8")
                try:
                    proc = subprocess.Popen(cmd,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as exc:
                    print("Status : FAIL", exc.returncode, exc.output)
                else:
                    tuple1 = proc.communicate(input=tmp.encode())
            tuple1 = tuple1[0]
            sendMessage(conn, tuple1)
            conn.close()
        # Error handling code
        except pickle.UnpicklingError as e:
            print("Data too large to handle")
            sendMessage(conn, str(e))
            conn.close()
            continue
        except (AttributeError,  EOFError, ImportError, IndexError) as e:
            print("An error occurred!")
            sendMessage(conn, str(e))
            conn.close()
            continue
        except socket.gaierror as e: 
            print ("Address-related error connecting to server:{}".format(e)) 
            conn.close()
            continue 
        except socket.error as e: 
            print ("Socket error: {}".format(e)) 
            conn.close()
            continue
        except Exception as e:
            print("Some error occured")
            print(e)
            break;

def client():
    # Port number for socket connection and max buffer size  
    try:
        print('Give input in form friend IP>command|| ....')
        shell = input("$")
        print(shell)
        # The command given is split using '||' as a delimiter
        list_of_commands = []
        for cmd in shell.split('||'):
            list_of_commands.append(cmd)
        print(list_of_commands)
        output = ''

        for i in range(len(list_of_commands)):
            cmd_dict = {}        
            command = list_of_commands[i]
            ind = command.find('>')
            friendIp = command[:ind]
            command = command[ind+1:]
            print("IP = {}, command = {}".format(friendIp, command))
            # A dictionary is created consisting of output for previous command and the acutal command
            if (i==0):
                cmd_dict.update({1:None, 2:command})
            else:
                cmd_dict.update({1:output, 2:command})
            try:
                # Socket connection code
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.settimeout(5)
                conn.connect((friendIp, port))
            except socket.error:
                print (" Problem in socket connection. Please check the IP and it's connectivity")
                exit(1)
            # Serializing dictionary to be sent over socket
            to_be_sent = pickle.dumps(cmd_dict)
            sendMessage(conn, to_be_sent)
            output = recvMessage(conn)
            conn.close()
        print(output.decode("utf-8"))
    except Exception as e:
            print("An error has occured")
            print(e)
            
ch = input("The node is to be a server or client?Server(Executes commands)/Client(Sends commands).C/S")
while(ch.lower()!='s' and ch.lower()!='c'):
    print("Invalid option! Try again!!")
    ch = input("The node is to be a server or client?Server(Executes commands)/Client(Sends commands).C/S")
    
if(ch.lower() == 's'):
    server()

elif(ch.lower() == 'c'):
    client()
