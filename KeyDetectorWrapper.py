import os
import ctypes

dll_path = os.path.abspath('./DLLs/KeyDetectorDLL.dll')
keyDetectorDLL = ctypes.CDLL(dll_path)

def getKey():
    return keyDetectorDLL.get_key()