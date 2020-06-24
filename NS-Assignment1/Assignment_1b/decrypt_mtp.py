# ==============================================================================================
# To execute this code : python decrypt_mtp "Name of the cipher text file to be decrypted" "name of file to store plain text"
# e.g. python decrypt_mtp.py ciphertext.txt viola.txt
# ==============================================================================================

from BitVector import *
import sys

if(len(sys.argv) != 3):
    print("The program needs exactly 3 arguments.")
    print("e.g. python decrypt_mtp.py ciphertext.txt viola.txt")
    print("Please try again..")
    sys.exit(0)
    
try:
    f = open(sys.argv[1], "r")
except FileNotFoundError:
    print("Unable to execute as the cipher text file does not exist")
    sys.exit(0)
cipher_text = f.read()

try:
    s = open("otp_secret", 'r')
except FileNotFoundError:
    print("Unable to execute the code as the secret file does not exist.")
    sys.exit(0)
otp = s.read()
cipher = BitVector(hexstring = cipher_text)
otp = BitVector(bitstring = otp)
otp = otp[0:len(cipher)]

plain_text = BitVector( size = len(cipher) )
plain_text = cipher ^ otp
plain_text = plain_text.get_bitvector_in_ascii()

FILEOUT = open(sys.argv[2], 'w')
FILEOUT.write(plain_text)
FILEOUT.close() 
print("Text is decrpyted")

