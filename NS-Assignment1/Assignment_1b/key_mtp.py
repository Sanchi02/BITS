from BitVector import *
import secrets


def otpgenerator(length):
    f = open("otp_secret", "w")
    otp = ""
    # Since secrets.randbits function sometimes returns value whose binary value length is less than the required length.
    # If we use that, part of plaintext will directly be present in cipher text as it would be xored with zero.
    while(len(otp) != length):
        otp = secrets.randbits(length)
        otp = BitVector(intVal = otp)
    otp = str(otp)
    f.write(otp)
    f.close()
    return "otp_secret"

otpgenerator(1048576)