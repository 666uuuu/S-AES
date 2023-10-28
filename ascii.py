# 将连续字符转换为二进制数组
import numpy as np
from AES import *


# 将ASCII字符串转换为二进制字符串
def ascii_to_binary(text):
    iBinary = ""
    for char in text:
        ascii_code = ord(char)
        binary_code = bin(ascii_code)[2:]  # 去掉二进制字符串前面的"0b"前缀
        if len(binary_code) > 8:
            return 0
        binary_code = binary_code.zfill(8)  # 在不足八位的二进制数前面填充零
        iBinary += binary_code
    return iBinary


# 将二进制字符串转换为ASCII字符串
def binary_to_ascii(binary_text):
    ascii_text = ''
    for i in range(0, len(binary_text), 8):
        ascii_char = chr(int(binary_text[i:i+8], 2))
        ascii_text += ascii_char
    return ascii_text


def binary_array_to_int(binary_array):
    if len(binary_array) != 4:
        raise ValueError("二进制数组长度必须为4位")
    decimal_value = 0
    for bit in binary_array:
        decimal_value = (decimal_value << 1) | bit

    return decimal_value


def split_string_by_length(string, length):
    return [int(string[i:i+length], 2) for i in range(0, len(string), length)]


def encrypt_ascii(input_bytes, key):
    e = encrypt(split_string_by_length(ascii_to_binary(input_bytes), 4), spl_bin(key))
    text = ''
    for i in range(len(e)):
        text += str(bin(e[i]))[2:].zfill(4)
    return binary_to_ascii(text)


def decrypt_ascii(input_bytes, key):
    d = decrypt(split_string_by_length(ascii_to_binary(input_bytes), 4), spl_bin(key))
    text = ''
    for i in range(len(d)):
        text += str(bin(d[i]))[2:].zfill(4)
    return binary_to_ascii(text)
