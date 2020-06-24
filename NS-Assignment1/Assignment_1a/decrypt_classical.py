# ===============================================================================================================
# To execute the code : python decrypt_classical.py "Name of CT" "Name of file to store decrypted text"
# e.g. python decrypt_classical.py ciphertext.txt viola.txt
# ===============================================================================================================
import sys
from BitVector import * 

if(len(sys.argv) != 3):
    print("The program needs exactly 3 arguments.")
    print("e.g. python decrypt_classical.py ciphertext.txt viola.txt")
    print("Please try again..")
    sys.exit(0)

# Expecting cipher text file as cmdline arg
BLOCKSIZE = 64
numbytes = BLOCKSIZE // 8
cipher_v = BitVector(bitlist = [0]*BLOCKSIZE)
PassPhrase = "I want to learn cryptograph and network security"
key = input("Enter the decrpyption key")

try:
    f = open(sys.argv[1], "r")
except FileNotFoundError:
    print("")
text = f.read()
cipher = "{0:08b}".format(int(text, 16))
cipher = str(cipher)

while(len(cipher) % BLOCKSIZE != 0):
    cipher = "0"+cipher
cipher_v = BitVector(bitstring = cipher)

key_bv = BitVector(bitlist = [0]*BLOCKSIZE)
for i in range(0,len(key) // numbytes):
    keyblock = key[i*numbytes:(i+1)*numbytes]
    key_bv ^= BitVector( textstring = keyblock )

bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)      

for i in range(0,len(PassPhrase) // numbytes):
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
    bv_iv ^= BitVector( textstring = textstr )

previous_block = bv_iv 
msg_decrypted_bv = BitVector( size = 0 )    

low = 0
high = 64
while (high!=(len(cipher_v)+64)):
    bv_read = cipher_v[low:high]
    if len(bv_read) < BLOCKSIZE:
        bv_read += BitVector(size = (BLOCKSIZE - len(bv_read)))
    bv_read ^= key_bv
    bv_read ^= previous_block
    previous_block = cipher_v[low:high].deep_copy()
    msg_decrypted_bv += bv_read
    low = high
    high = high + 64

message = msg_decrypted_bv.get_bitvector_in_ascii()
FILEOUT = open(sys.argv[2], 'w')
FILEOUT.write(message)
FILEOUT.close() 