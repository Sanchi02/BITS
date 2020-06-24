from BitVector import *
import sys
import copy

try:
    f = open("ciphertext.txt", "r")
except:
    print("File named ciphertext not found.")
    sys.exit(0)
text = f.read()
cipher_v = BitVector(hexstring = text.strip('\n'))
PassPhrase = "I want to learn cryptograph and network security"
BLOCKSIZE = 64
c_blocks = []
low = 0
keyDiscovered = [0]*BLOCKSIZE

# Converting cipher text to chunks of BLOCKSIZE
for i in range(len(cipher_v)//BLOCKSIZE):
    t = copy.deepcopy(cipher_v[low:low+BLOCKSIZE])
    c_blocks.append(t)
    low +=BLOCKSIZE

bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)

for i in range(0,len(PassPhrase) // 8):
    textstr = PassPhrase[i*8:(i+1)*8]
    bv_iv ^= BitVector( textstring = textstr )

mtp_blocks = []

# Converting the chain block cipher problem to MTP problem
for i in range(len(c_blocks)):
    if(i!=0):
        tmp = c_blocks[i] ^ c_blocks[i-1]
        mtp_blocks.append(tmp)
    else:
        tmp = c_blocks[i] ^ bv_iv
        mtp_blocks.append(tmp)

# Setting threshold for finding the probable space value in the plaintext. 
# Higher the threshold less the values discovered in plaintext but more the accuracy of those values
thresh = len(c_blocks)*0.75
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

print("The code may take few minutes to execute depending on the length of cipher text. Please wait...")
# Xoring two cipherblocks at a time for discovring the probable space values in their respective plaintext
for i, ct in enumerate(mtp_blocks):
    spaceIndexes = set()
    possibleSpaceLoc = [0]*8
    for j, ct2 in enumerate(mtp_blocks):
        if(i!=j):
            xorRes = ct ^ ct2
            low = 0
            # Comparing each character value with the once maintained in the list.
                # If matched the count of that index being space is incremented
            for k in range(len(xorRes)//8):
                if(xorRes[low:low+8] in valuesForAlphasWithSpace):
                    possibleSpaceLoc[k] += 1
                low = low + 8
            for ind,s in enumerate(possibleSpaceLoc):
                # Only values greater than threshold would be considered as other combinations yielding the same values as in the list above exist.
                if(s > thresh):
                    spaceIndexes.add(ind)
    # Once the position of the space in plain text is discovered, value of space is xored with that
    # location in cipher text to get a part of the key.
    for s in spaceIndexes:
        tmp = ct[s*8:(s*8)+8]
        key = spaceVal ^ tmp
        t = copy.deepcopy(list(key))
        keyDiscovered[s*8:(s*8)+8] = t

t = BitVector(bitlist = keyDiscovered)
keyD = t.get_bitvector_in_ascii()

msg_decrypted_bv = BitVector( size = 0 )    
previous_block = bv_iv
low = 0
high = 64
while (high!=(len(cipher_v)+64)):
    bv_read = cipher_v[low:high]
    if len(bv_read) < BLOCKSIZE:
        bv_read += BitVector(size = (BLOCKSIZE - len(bv_read)))
    bv_read ^= t
    bv_read ^= previous_block
    previous_block = cipher_v[low:high].deep_copy()
    msg_decrypted_bv += bv_read
    low = high
    high = high + 64

message = msg_decrypted_bv.get_bitvector_in_ascii()
rt = open("recoveredtext.txt", "w")
rt.write(message)
rt.close()
print("Recovery completed")