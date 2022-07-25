import os
import sys


def encode(a):
    a = bytearray(a)
    for i in range(len(a)):
        if i % 5 == 0:
            a[i] ^= 12
        elif i % 3 == 0:
            a[i] ^= 6
        else:
            a[i] ^= 3
    return a

def pe2shc(pe_name):
    shc_name = pe_name.replace(".exe", "")+"_bak.txt"
    os.system(f"pe2shc {pe_name} {shc_name}")
    return shc_name



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[WRONG] input the pe file")
    else:
        try:
            shc_name = pe2shc(sys.argv[1])
            new_shc_name = shc_name.replace("_bak.txt", "") + ".txt"
            new_shc_file = open(new_shc_name, "wb")
            shellcode = open(shc_name, "rb").read()
            en_shellcode = (encode(shellcode))
            new_shc_file.write(en_shellcode)
            print(f"[SUCCESS] encoded shellfile: {new_shc_name}")
            os.remove(shc_name)
        except Exception as e:
            print(e)
