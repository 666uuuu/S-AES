import random

import AES
def encrypt_cbc(plain_text, key, iv):
    ciphertext = []
    previous_block = iv
    for block in plain_text:
        # CBC模式下，每个明文块先与前一个密文块异或
        block = [a ^ b for a, b in zip(block, previous_block)]
        # 然后使用密钥进行加密
        encrypted_block = AES.encrypt(block, key)
        # 密文块添加到结果中
        ciphertext.append(encrypted_block)
        # 更新前一个密文块
        previous_block = encrypted_block

    return ciphertext


# 解密函数（CBC模式）
def decrypt_cbc(ciphertext, key, iv):
    plain_text = []
    previous_block = iv

    for block in ciphertext:
        # 使用密钥进行解密
        decrypted_block = AES.decrypt(block, key)
        # 在CBC模式下，解密后的块再与前一个密文块异或
        plain_block = [a ^ b for a, b in zip(decrypted_block, previous_block)]
        # 明文块添加到结果中
        plain_text.append(plain_block)
        # 更新前一个密文块
        previous_block = block

    return plain_text


# 随机生成明密文文件
def generate(row_num):
    binary_num = ''
    for j in range(row_num):
        for i in range(4):
            if i == 3:
                binary_num += bin(random.randint(0, 15))[2:].zfill(4)
                break
            binary_num += bin(random.randint(0, 15))[2:].zfill(4) + ','
        binary_num += '\n'
    return binary_num


# 把解密或者加密的结果数组转化成二进制
def text_to_string(ciphertext):
    c_out = [AES.out(ciphertext[i]) for i in range(len(ciphertext))]
    c_out_string = ''
    for i in range(len(c_out)):
        c_out_string += c_out[i] + '\n'
    return c_out_string
