# S盒
sbox = [[0x9, 0x4, 0xa, 0xb],
        [0xd, 0x1, 0x8, 0x5],
        [0x6, 0x2, 0x0, 0x3],
        [0xc, 0xe, 0xf, 0x7]]

# 逆S盒
r_sbox = [[0xa, 0x5, 0x9, 0xb],
          [0x1, 0x7, 0x8, 0xf],
          [0x6, 0x0, 0x2, 0x3],
          [0xc, 0x4, 0xd, 0xe]]

# 轮常数
rcon = [[1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0]]

# 轮数
round = 2


# 密钥扩展
def key_expansion(key):
    w0 = key[:8]
    w1 = key[8:]
    # 初始化存储生成密钥的列表
    expanded_key = [w0, w1]
    w_temp = w1[4:] + w1[:4]
    w_x1 = 2 * w_temp[0] + w_temp[1]
    w_y1 = 2 * w_temp[2] + w_temp[3]
    number1 = sbox[w_x1][w_y1]
    binary_str1 = bin(number1)[2:]
    binary_str1 = binary_str1.zfill(4)
    binary_array1 = [int(bit) for bit in binary_str1]
    w_x2 = 2 * w_temp[4] + w_temp[5]
    w_y2 = 2 * w_temp[6] + w_temp[7]
    number2 = sbox[w_x2][w_y2]
    binary_str2 = bin(number2)[2:]
    binary_str2 = binary_str2.zfill(4)
    binary_array2 = [int(bit) for bit in binary_str2]
    binary_array = binary_array1 + binary_array2
    w2 = xor_arrays(xor_arrays(w0, rcon[0]), binary_array)
    w3 = xor_arrays(w2, w1)
    w_temp = w3[4:] + w3[:4]
    w_x1 = 2 * w_temp[0] + w_temp[1]
    w_y1 = 2 * w_temp[2] + w_temp[3]
    number1 = sbox[w_x1][w_y1]
    binary_str1 = bin(number1)[2:]
    binary_str1 = binary_str1.zfill(4)
    binary_array1 = [int(bit) for bit in binary_str1]
    w_x2 = 2 * w_temp[4] + w_temp[5]
    w_y2 = 2 * w_temp[6] + w_temp[7]
    number2 = sbox[w_x2][w_y2]
    binary_str2 = bin(number2)[2:]
    binary_str2 = binary_str2.zfill(4)
    binary_array2 = [int(bit) for bit in binary_str2]
    binary_array = binary_array1 + binary_array2
    w4 = xor_arrays(xor_arrays(w2, rcon[1]), binary_array)
    w5 = xor_arrays(w3, w4)
    expanded_key.append(w2)
    expanded_key.append(w3)
    expanded_key.append(w4)
    expanded_key.append(w5)

    return expanded_key


# 轮密钥加
length = 2  # 密钥长度为2


def add_round_key(state, key_schedule, rnd):
    for col in range(length):
        s0 = state[0][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][:4])
        s1 = state[1][col] ^ binary_array_to_int(key_schedule[2 * rnd + col][4:])

        state[0][col] = s0
        state[1][col] = s1

    return state


# 字节替换
dict = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def sub_bytes(state, inv=False):
    if not inv:
        box = sbox
    else:
        box = r_sbox

    for i in range(len(state)):
        for j in range(len(state[i])):
            binary_str1 = bin(state[i][j])[2:]
            binary_str1 = binary_str1.zfill(4)
            binary_array1 = [int(bit) for bit in binary_str1]
            row = 2 * binary_array1[0] + binary_array1[1]
            col = 2 * binary_array1[2] + binary_array1[3]
            box_elem = box[row][col]
            state[i][j] = box_elem

    return state


# 行移位
def shift_rows(state):
    temp = state[1][0]
    state[1][0] = state[1][1]
    state[1][1] = temp

    return state


# GF(2^4)算法
def gf_4_addition(a, b):
    modulus = 0b10011
    return a ^ b


def gf_4_multiply(a, b):
    modulus = 0b10011  # This is the binary representation of x^4 + x + 1

    result = 0
    for _ in range(4):
        if b & 1:
            result ^= a
        a <<= 1
        if (a & 0b10000) != 0:
            a ^= modulus
        b >>= 1

    return result


# 列混淆
num = 2  # 列数为2

def mix_columns(state, inv=False):
    for i in range(num):  # 2行
        if inv == False:  # 加密阶段
            s0 = gf_4_addition(gf_4_multiply(1, state[0][i]), gf_4_multiply(4, state[1][i]))
            s1 = gf_4_addition(gf_4_multiply(4, state[0][i]), gf_4_multiply(1, state[1][i]))
        else:  # 解密阶段
            s0 = gf_4_addition(gf_4_multiply(9, state[0][i]), gf_4_multiply(2, state[1][i]))
            s1 = gf_4_addition(gf_4_multiply(2, state[0][i]), gf_4_multiply(9, state[1][i]))

        state[0][i] = s0
        state[1][i] = s1

    return state


# 异或操作
def xor_arrays(arr1, arr2):
    # 确保两个数组的长度相同
    if len(arr1) != len(arr2):
        raise ValueError("数组长度不相同")

    # 对数组逐位进行异或操作
    result = [bit1 ^ bit2 for bit1, bit2 in zip(arr1, arr2)]
    return result


# 二进制转整型
def binary_array_to_int(binary_array):
    if len(binary_array) != 4:
        raise ValueError("二进制数组长度必须为4位")

    decimal_value = 0
    for bit in binary_array:
        decimal_value = (decimal_value << 1) | bit

    return decimal_value


# 加密函数
def encrypt(input_bytes, key):
    state = [[input_bytes[0], input_bytes[2]], [input_bytes[1], input_bytes[3]]]
    key_schedule = key_expansion(key)
    state = add_round_key(state, key_schedule, 0)
    rnd = 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, key_schedule, rnd)
    rnd += 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, rnd)
    output = [state[0][0], state[1][0], state[0][1], state[1][1]]

    return output


# 解密函数
def decrypt(cipher, key):
    state = [[cipher[0], cipher[2]], [cipher[1], cipher[3]]]

    key_schedule = key_expansion(key)
    state = add_round_key(state, key_schedule, round)
    rnd = round - 1
    state = shift_rows(state)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, key_schedule, rnd)
    state = mix_columns(state, inv=True)
    rnd -= 1
    state = shift_rows(state)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, key_schedule, rnd)

    output = [state[0][0], state[1][0], state[0][1], state[1][1]]

    return output


# 将二进制密钥转换为数组
def spl_bin(input):
    cip = []
    for i in range(len(input)):
        cip.append(int(input[i]))
    return cip


# 将逗号隔开的文本转换为数组
def spl_bin1(input):
    cip = []
    input = str(input).split(',')
    for i in range(len(input)):
        cip.append(int(input[i], 2))
    return cip


def out(e):
    text = str(bin(e[0]))[2:].zfill(4) + ',' + \
           str(bin(e[1]))[2:].zfill(4) + ',' + \
           str(bin(e[2]))[2:].zfill(4) + ',' + \
           str(bin(e[3]))[2:].zfill(4)
    return text

