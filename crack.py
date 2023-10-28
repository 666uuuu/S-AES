import time
import AES


# 暴力破解
def int_to_binary_array(n):
    # 将整数转化为二进制字符串，然后填充零以达到指定的位数
    binary_str = bin(n)[2:].zfill(16)
    # 将二进制字符串转化为整数列表
    binary_array = [int(bit) for bit in binary_str]

    return binary_array


def arr_to_int(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i] * pow(2, 4 * (3 - i))
    return sum


def int_to_arr(n):
    arr = []
    for i in range(0, 4):
        arr.append(n // pow(2, 4 * (3 - i)))
        n = n % pow(2, 4 * (3 - i))
    return arr


def binary_search_first_column(sorted_2d_array, target):
    left, right = 0, len(sorted_2d_array) - 1

    while left <= right:
        mid = left + (right - left) // 2  # 防止整数溢出

        if sorted_2d_array[mid][0] == target:
            return mid
        elif sorted_2d_array[mid][0] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # 没有找到目标元素


def find_keys(known_plain, known_cipher):
    possible_keys = []
    encrypt_result = []
    for key1 in range(0, 65536):
        encrypt_result.append([arr_to_int(AES.encrypt(known_plain, int_to_binary_array(key1))), key1])
    sorted_list = sorted(encrypt_result, key=lambda x: x[0])
    for key2 in range(0, 65536):
        encrypt1 = arr_to_int(AES.encrypt(known_cipher, int_to_binary_array(key2)))
        pos = binary_search_first_column(sorted_list, encrypt1)
        if pos != -1:
            possible_keys.append([sorted_list[pos][1], key2])
    return possible_keys


pla = '1111,0000,1111,0000'
cip = '1011,0110,0111,1010'
start = time.time()
possible_keys = find_keys(AES.spl_bin1(pla), AES.spl_bin1(cip))
end = time.time()
key = [5, 15, 0, 10]
k = arr_to_int(key)
# 打印部分，即只打印满足key1的解
print("破解时间：", end - start)
for i in range(len(possible_keys)):
    if possible_keys[i][0] == k:
        print('Key1:'+AES.out(int_to_arr(possible_keys[i][0])),
              'Key2:'+AES.out(int_to_arr(possible_keys[i][1])))