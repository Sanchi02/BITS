# ===============================================================================================================
# To execute the code : python encrypt_mtp "PlainText file" "Ciphertext file name to be generated"
# e.g. python encrypt_mtp.py plaintext.txt ciphertext.txt
# ===============================================================================================================
from BitVector import *
import sys

if(len(sys.argv) != 3):
    print("The program needs exactly 3 arguments.")
    print("e.g. python encrypt_mtp.py plaintext.txt ciphertext.txt")
    print("Please try again..")
    sys.exit(0)

try:
    f = open(sys.argv[1], "r")
except FileNotFoundError:
    print("Unable to execute as the plain text file does not exist")
    sys.exit(0)

text = f.read()
text_bv = BitVector(textstring = text)
if(len(text_bv) > 1048575):
    print("The code can encrypt only 2^20 size of plaintext")
    print("Enter PT with characters less than that value")
    sys.exit(0)

try:
    s = open("otp_secret", "r")
except FileNotFoundError:
    print("Key file not found")
    sys.exit(0)

otp = s.read()
otp = BitVector(bitstring = otp)
otp = otp[0:len(text_bv)]

cipher = BitVector( size = len(text_bv) )
cipher = text_bv ^ otp

cipher_text = cipher.get_hex_string_from_bitvector()

FILEOUT = open(sys.argv[2], 'w')
FILEOUT.write(cipher_text)
FILEOUT.close() 
print("Text is encrpyted")