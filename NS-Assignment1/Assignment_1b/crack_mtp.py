# ===========================================================================================================
# To execute the code : python crack_mtp.py
# The file ciphertext.txt contains different equal size cipher texts that were encrypted using the same key.
# ============================================================================================================

import sys
from BitVector import *
import copy

try:
    f = open("ciphertext.txt", "r")
except FileNotFoundError:
    print("Unable to execute as the file with few cipher texts not found")
    sys.exit(0)
text = f.read()
ciphers = text.splitlines()
ciphersInBV = []

# Converting all ciphers to bitvectors
for c in ciphers:
    tmp = BitVector(hexstring = c)
    ciphersInBV.append(tmp)
length = len(ciphersInBV[0])

# Setting threshold for finding the probable space value in the plaintext. 
# Higher the threshold less the values discovered in plaintext but more the accuracy of those values
thresh = len(ciphersInBV)*0.68
keyDiscovered = ['*']*length 

cap_alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
spaceVal = BitVector(textstring =' ')

# Maintain a list for all alphabets when xored with space
valuesForAlphasWithSpace = []
for c in cap_alpha:
    tmp = BitVector(textstring = c)
    tmp = tmp ^ spaceVal
    valuesForAlphasWithSpace.append(tmp)
    tmp = BitVector(textstring = c.lower())
    tmp = tmp ^ spaceVal
    valuesForAlphasWithSpace.append(tmp)

# Xoring two ciphertexts at a time for discovring the probable space values in their respective plaintext
print("The program may take few minutes to run depending on the length of the CTS. Please wait..")
for i,cipher in enumerate(ciphersInBV):
    spaceIndexes = set()
    possibleSpaceLoc = [0]*((length//8) + 1)
    for j,cipher2 in enumerate(ciphersInBV):
        if(i!=j):
            xorRes = cipher ^ cipher2
            for k in range(len(xorRes)//8):
                # Comparing each character value with the once maintained in the list.
                # If matched the count of that index being space is incremented
                if(xorRes[k*8:(k*8)+8] in valuesForAlphasWithSpace):
                    possibleSpaceLoc[k] += 1
            for ind,s in enumerate(possibleSpaceLoc):
                # Only values greater than threshold would be considered as other combinations yielding the same values as in the list above exist.
                if(s > thresh):
                    spaceIndexes.add(ind)
    # Once the position of the space in plain text is discovered, value of space is xored with that
    # location in cipher text to get a part of the key.
    for s in spaceIndexes:
        tmp = cipher[s*8:(s*8)+8]
        key = spaceVal ^ tmp
        keyDiscovered[s*8:(s*8)+8] = list(key)

recoveredTexts = []
for crack in ciphers:
    letC = BitVector(hexstring = crack)
    PTDiscovered = []
    for t in range(length//8):
        if(keyDiscovered[t*8]!='*'):
            letK = BitVector(bitlist = keyDiscovered[t*8:(t*8)+8])
            partCipher = letC[t*8:(t*8)+8]
            tmp = letK^partCipher
            tmp = tmp.get_bitvector_in_ascii()
            PTDiscovered.append(tmp)
        else:
            PTDiscovered.append('*')
    rt = ""
    for t in PTDiscovered:
        rt += t
    recoveredTexts.append(rt)

with open("recoveredtext.txt", "w") as fileptr:
    fileptr.writelines("%s\n" %text for text in recoveredTexts)
print("Results written in recoveredtext.txt file")

