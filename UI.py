import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkbootstrap import Style
from AES import decrypt, encrypt, spl_bin1, spl_bin, out
from ascii import encrypt_ascii, decrypt_ascii
from CBC import generate, encrypt_cbc, decrypt_cbc, text_to_string


# 居中
def center_window(r, w, h):
    # 获取屏幕 宽、高
    ws = r.winfo_screenwidth()
    hs = r.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    r.geometry('%dx%d+%d+%d' % (w, h, x, y))


# 判断明文密文是否是否符合要求
def is_binary_text(bit_number, string):
    b = {'0', '1', ','}
    t = set(string)
    if b != t and t != {'0', ','} and t != {'1', ','}:
        return False
    if len(string) == bit_number:
        return True
    else:
        return False


# 判断密钥是否符号要求
def is_binary_key(bit_number, string):
    b = {'0', '1'}
    t = set(string)
    if b != t and t != {'0'} and t != {'1'}:
        return False
    if len(string) == bit_number:
        return True
    else:
        return False


# 判断CBC明密文是否符号要求
def is_cbc_text(text_array):
    text_array = [string for string in text_array if string]
    for i in range(len(text_array)):
        if not is_binary_text(19, text_array[i]):
            print(text_array[i])
            return False
    return True


# 主窗口
def main_window():
    # 基础测试和ascii扩展功能窗口
    def bin_and_ascii_window():
        # 定义按钮点击事件
        def encryption():
            plaintext = message_entry.get()
            key = key_entry.get()
            encode = combo.get()
            if not is_binary_key(16, key):
                tkinter.messagebox.showwarning('警告', '请输入 16bit 密钥！')
                return
            if encode == "--请选择输入编码语言--":
                tkinter.messagebox.showinfo('提示', '请选择输入编码语言')
                return
            elif encode == "Binary":
                if not is_binary_text(19, plaintext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 明文！每4bit用英文逗号隔开')
                    return
                ciphertext = out(encrypt(spl_bin1(plaintext), spl_bin(key)))
            else:
                if not all(ord(c) < 256 for c in plaintext) or len(plaintext) != 2:
                    print(len(plaintext))
                    tkinter.messagebox.showwarning('警告', '请输入 2Byte ASCII 明文！')
                    return
                ciphertext = encrypt_ascii(plaintext, key)
            output_text.delete('1.0', tk.END)
            output_text.insert(END, '密文：' + ciphertext + "\n")

        def decryption():
            ciphertext = message_entry.get()
            key = key_entry.get()
            encode = combo.get()
            if not is_binary_key(16, key):
                tkinter.messagebox.showwarning('警告', '请输入 16bit 密钥！')
                return
            if encode == "--请选择输入编码语言--":
                tkinter.messagebox.showinfo('提示', '请选择输入编码语言')
                return
            elif encode == "Binary":
                if not is_binary_text(19, ciphertext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 密文！每4bit用英文逗号隔开')
                    return
                plaintext = out(decrypt(spl_bin1(ciphertext), spl_bin(key)))
            else:
                if not all(ord(c) < 256 for c in ciphertext) or len(ciphertext) != 2:
                    tkinter.messagebox.showwarning('警告', '请输入 2Byte ASCII 密文！')
                    return
                plaintext = decrypt_ascii(ciphertext, key)
            plaintext_str = [str(i) for i in plaintext]
            output_text.delete('1.0', tk.END)
            output_text.insert(END, '明文：' + ''.join(plaintext_str) + "\n")

        root_bin_and_ascii = tk.Toplevel(root)
        root_bin_and_ascii.title("S-AES二进制及ASCII加密解密")

        center_window(root_bin_and_ascii, 500, 300)

        # 创建中心标题
        title_label = tk.Label(root_bin_and_ascii, text='S-AES', font=("Times", 30, "bold"))
        title_label.place(relx=.5, y=40, anchor='center')

        # 创建下拉框
        combo = ttk.Combobox(root_bin_and_ascii, values=["--请选择输入编码语言--", "Binary", "ASCII"])
        combo.current(0)
        combo.place(relx=.5, y=86, anchor='center')

        # 创建明文文本框及输入框
        message_label = tk.Label(root_bin_and_ascii, text="输入:")
        message_label.place(x=130, rely=.4, anchor='center')
        message_entry = tk.Entry(root_bin_and_ascii)
        message_entry.place(relx=.5, rely=.4, anchor='center')

        # 创建密钥文本框及输入框
        key_label = tk.Label(root_bin_and_ascii, text="密钥:")
        key_label.place(x=130, rely=.5, anchor='center')
        key_entry = tk.Entry(root_bin_and_ascii)
        key_entry.place(relx=.5, rely=.5, anchor='center')

        # 创建按钮
        encryption_button = tk.Button(root_bin_and_ascii, text="确认加密", command=encryption)
        encryption_button.place(relx=.4, y=190, anchor='center')
        decryption_button = tk.Button(root_bin_and_ascii, text="确认解密", command=decryption)
        decryption_button.place(relx=.6, y=190, anchor='center')

        # 创建输出框控件
        output_text = tk.Text(root_bin_and_ascii, height=2, width=30)
        output_text.place(relx=.5, rely=.8, anchor='center')

        root_bin_and_ascii.mainloop()

    # 多重加密解密窗口
    def multiple_encryption_window():
        # 双重加密窗口
        def double_encryption_window():
            # 定义按钮点击事件
            def encryption():
                plaintext = message_entry.get()
                key = str(key_entry.get("1.0","end")).split('\n')
                if not is_binary_text(19, plaintext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 明文！每4bit用英文逗号隔开')
                    return
                for i in range(2):
                    if not is_binary_key(16, key[i]):
                        tkinter.messagebox.showwarning('警告', '请输入 32bit 密钥，16bit 之后换行！')
                        return
                ciphertext = encrypt(spl_bin1(plaintext), spl_bin(key[0]))
                ciphertext = out(encrypt(ciphertext, spl_bin(key[1])))
                output_text.delete('1.0', tk.END)
                output_text.insert(END, '密文：' + ciphertext + "\n")

            def decryption():
                ciphertext = message_entry.get()
                key = str(key_entry.get("1.0","end")).split('\n')
                if not is_binary_text(19, ciphertext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 密文！每4bit用英文逗号隔开')
                    return
                for i in range(2):
                    if not is_binary_key(16, key[i]):
                        tkinter.messagebox.showwarning('警告', '请输入 32bit 密钥，16bit 之后换行！')
                        return
                plaintext = decrypt(spl_bin1(ciphertext), spl_bin(key[1]))
                plaintext = out(decrypt(plaintext, spl_bin(key[0])))
                plaintext_str = [str(i) for i in plaintext]
                output_text.delete('1.0', tk.END)
                output_text.insert(END, '明文：' + ''.join(plaintext_str) + "\n")

            root_double_encrypt = tk.Toplevel(root_multiple_encrypt)
            root_double_encrypt.title('S-AES双重加密解密')

            center_window(root_double_encrypt, 500, 300)

            # 创建明文文本框及输入框
            message_label = tk.Label(root_double_encrypt, text="输入:")
            message_label.place(x=150, rely=.2, anchor='center')
            message_entry = tk.Entry(root_double_encrypt)
            message_entry.place(relx=.5, rely=.2, anchor='center')

            # 创建密钥文本框及输入框
            key_label = tk.Label(root_double_encrypt, text="密钥:")
            key_label.place(x=150, y=103, anchor='center')
            key_entry = tk.Text(root_double_encrypt, height=2, width=19)
            key_entry.place(relx=.5, rely=.4, anchor='center')

            # 创建按钮
            encryption_button = tk.Button(root_double_encrypt, text="确认加密", command=encryption)
            encryption_button.place(x=215, y=180, anchor='center')
            decryption_button = tk.Button(root_double_encrypt, text="确认解密", command=decryption)
            decryption_button.place(x=285, y=180, anchor='center')

            # 创建输出框控件
            output_text = tk.Text(root_double_encrypt, height=2, width=30)
            output_text.place(relx=.5, y=230, anchor='center')

            root_double_encrypt.mainloop()

        # 三重加密窗口
        def triple_encryption_window():
            # 定义按钮点击事件
            def encryption():
                plaintext = message_entry.get()
                key = str(key_entry.get("1.0","end")).split('\n')
                if not is_binary_text(19, plaintext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 明文！每4bit用英文逗号隔开')
                    return
                for i in range(3):
                    if not is_binary_key(16, key[i]):
                        tkinter.messagebox.showwarning('警告', '请输入 32bit 密钥，16bit 之后换行！')
                        return
                ciphertext = encrypt(spl_bin1(plaintext), spl_bin(key[0]))
                ciphertext = decrypt(ciphertext, spl_bin(key[1]))
                ciphertext = out(encrypt(ciphertext, spl_bin(key[2])))
                output_text.delete('1.0', tk.END)
                output_text.insert(END, '密文：' + ciphertext + "\n")

            def decryption():
                ciphertext = message_entry.get()
                key = str(key_entry.get("1.0","end")).split('\n')
                if not is_binary_text(19, ciphertext):
                    tkinter.messagebox.showwarning('警告', '请输入 16bit 密文！每4bit用英文逗号隔开')
                    return
                for i in range(3):
                    if not is_binary_key(16, key[i]):
                        tkinter.messagebox.showwarning('警告', '请输入 32bit 密钥，16bit 之后换行！')
                        return
                plaintext = decrypt(spl_bin1(ciphertext), spl_bin(key[2]))
                plaintext = encrypt(plaintext, spl_bin(key[1]))
                plaintext = out(decrypt(plaintext, spl_bin(key[0])))
                plaintext_str = [str(i) for i in plaintext]
                output_text.delete('1.0', tk.END)
                output_text.insert(END, '明文：' + ''.join(plaintext_str) + "\n")

            root_triple_encryption = tk.Toplevel(root_multiple_encrypt)
            root_triple_encryption.title('S-AES三重加密解密')

            center_window(root_triple_encryption, 500, 300)

            # 创建明文文本框及输入框
            message_label = tk.Label(root_triple_encryption, text="输入:")
            message_label.place(x=150, rely=.2, anchor='center')
            message_entry = tk.Entry(root_triple_encryption)
            message_entry.place(relx=.5, rely=.2, anchor='center')

            # 创建密钥文本框及输入框
            key_label = tk.Label(root_triple_encryption, text="密钥:")
            key_label.place(x=150, y=95, anchor='center')
            key_entry = tk.Text(root_triple_encryption, height=3, width=19)
            key_entry.place(relx=.5, rely=.4, anchor='center')

            # 创建按钮
            encryption_button = tk.Button(root_triple_encryption, text="确认加密", command=encryption)
            encryption_button.place(x=215, y=180, anchor='center')
            decryption_button = tk.Button(root_triple_encryption, text="确认解密", command=decryption)
            decryption_button.place(x=285, y=180, anchor='center')

            # 创建输出框控件
            output_text = tk.Text(root_triple_encryption, height=2, width=30)
            output_text.place(relx=.5, y=230, anchor='center')

            root_triple_encryption.mainloop()

        root_multiple_encrypt = tk.Toplevel(root)
        root_multiple_encrypt.title("S-AES多重加密解密")

        center_window(root_multiple_encrypt, 350, 200)

        double_encryption_button = tk.Button(root_multiple_encrypt, text="双重加密", command=double_encryption_window,
                                             height=2, width=25)
        double_encryption_button.place(relx=.5, y=60, anchor='center')
        triple_encryption_button = tk.Button(root_multiple_encrypt, text="三重加密", command=triple_encryption_window,
                                             height=2, width=25)
        triple_encryption_button.place(relx=.5, y=130, anchor='center')

        root_multiple_encrypt.mainloop()

    # CBC加密窗口
    def cbc_window():
        def generate_text():
            def generate_text_display():
                row_num = int(row_num_entry.get())
                open_text.delete('1.0', tk.END)
                open_text.insert(END, generate(row_num))
                root_generate_text.destroy()

            root_generate_text = tk.Toplevel(root_cbc)
            root_generate_text.title('随机生成明密文')

            center_window(root_generate_text, 280, 150)

            # 创建明文文本框及输入框
            row_num_label = tk.Label(root_generate_text, text="请输入行数:")
            row_num_label.place(relx=.2, y=50, anchor='center')
            row_num_entry = tk.Entry(root_generate_text, width=18)
            row_num_entry.place(x=160, y=50, anchor='center')

            # 创建按钮
            row_num_button = tk.Button(root_generate_text, text='确认', command=generate_text_display, width=8)
            row_num_button.place(x=115, y=90)

            root_generate_text.mainloop()

        def open_text():
            with open(filedialog.askopenfilename(), 'r') as file:
                content = file.read()
                open_text.delete('1.0', tk.END)
                open_text.insert(END, content)

        def encryption():
            iv = str(iv_entry.get())
            key = str(key_entry.get())
            plain_array = open_text.get('1.0', END).split('\n')
            plain_array = [string for string in plain_array if string]
            if not is_binary_key(16, key):
                tkinter.messagebox.showwarning('警告', '请输入 16bit 密钥！')
                return
            if not is_binary_key(16, iv):
                tkinter.messagebox.showwarning('警告', '请输入 16bit IV！')
                return
            if not is_cbc_text(plain_array):
                tkinter.messagebox.showwarning('警告', '请注意明文格式！')
                return
            plaintexts = [spl_bin1(plain_array[i]) for i in range(len(plain_array) - 1)]
            ciphertexts = encrypt_cbc(plaintexts, spl_bin(key), spl_bin(iv))
            output_text.delete('1.0', tk.END)
            output_text.insert(END, text_to_string(ciphertexts))

        def decryption():
            iv = str(iv_entry.get())
            key = str(key_entry.get())
            cipher_array = open_text.get('1.0', END).split('\n')
            cipher_array = [string for string in cipher_array if string]
            if not is_binary_key(16, key):
                tkinter.messagebox.showwarning('警告', '请输入 16bit 密钥！')
                return
            if not is_binary_key(16, iv):
                tkinter.messagebox.showwarning('警告', '请输入 16bit IV！')
                return
            if not is_cbc_text(cipher_array):
                tkinter.messagebox.showwarning('警告', '请注意密文格式！')
                return
            ciphertexts = [spl_bin1(cipher_array[i]) for i in range(len(cipher_array) - 1)]
            plaintexts = decrypt_cbc(ciphertexts, spl_bin(key), spl_bin(iv))
            output_text.delete('1.0', tk.END)
            output_text.insert(END, text_to_string(plaintexts))

        def save_text():
            global file_path
            global file_text
            file_path = filedialog.asksaveasfilename(title=u'保存文件')
            print('保存文件：', file_path)
            file_text = output_text.get('1.0', tk.END)
            if file_path is not None:
                with open(file=file_path, mode='w+', encoding='utf-8') as file:
                    file.write(file_text)
                output_text.delete('1.0', tk.END)
                tkinter.messagebox.showinfo(title='文件保存', message='保存成功')
                print('保存完成')

        # 创建Tkinter根窗口对象
        root_cbc = tk.Toplevel(root)
        root_cbc.title('CBC加密解密')

        center_window(root_cbc, 400, 510)

        # 创建密钥文本框及输入框
        key_label = tk.Label(root_cbc, text="密钥:")
        key_label.place(relx=.2, y=50, anchor='center')
        key_entry = tk.Entry(root_cbc)
        key_entry.place(relx=.5, y=50, anchor='center')

        # 创建IV文本框及输入框
        iv_label = tk.Label(root_cbc, text="初始化向量:")
        iv_label.place(x=70, y=80, anchor='center')
        iv_entry = tk.Entry(root_cbc)
        iv_entry.place(relx=.5, y=80, anchor='center')

        # 创建生成文件和读取文件按钮
        generate_text_button = tk.Button(root_cbc, text="随机生成明密文", command=generate_text)
        generate_text_button.place(relx=.5, y=120, anchor='center')
        open_text_button = tk.Button(root_cbc, text="读取明密文文件", command=open_text)
        open_text_button.place(relx=.5, y=160, anchor='center')

        # 创建文本框显示读取的文件内容
        open_text = tk.Text(root_cbc, height=5, width=30)
        open_text.place(relx=.5, y=235, anchor='center')

        # 创建加密解密按钮
        encryption_button = tk.Button(root_cbc, text="确认加密", command=encryption, width=10)
        encryption_button.place(x=145, y=310, anchor='center')
        decryption_button = tk.Button(root_cbc, text="确认解密", command=decryption, width=10)
        decryption_button.place(x=255, y=310, anchor='center')

        # 创建输出框控件
        output_text = tk.Text(root_cbc, height=5, width=30)
        output_text.place(relx=.5, y=385, anchor='center')

        # 创建保存按钮
        save_file_button = tk.Button(root_cbc, text="保存结果", command=save_text, width=10)
        save_file_button.place(relx=.5, y=465, anchor='center')

        root_cbc.mainloop()

    root = tk.Tk()
    root.title("S-AES加密解密")

    Style(theme='sandstone')

    center_window(root, 300, 350)

    # 创建中心标题
    title_label = tk.Label(root, text='S-AES', font=("Times", 30, "bold"))
    title_label.place(relx=.5, y=40, anchor='center')

    # 创建按钮
    bin_and_ascii_button = tk.Button(root, text="基础及ASCII扩展功能", command=bin_and_ascii_window,
                                     height=2, width=23)
    bin_and_ascii_button.place(relx=.5, y=120, anchor='center')
    multiple_encryption_button = tk.Button(root, text="多重加密解密", command=multiple_encryption_window,
                                           height=2, width=23)
    multiple_encryption_button.place(relx=.5, y=200, anchor='center')
    cbc_button = tk.Button(root, text="CBC加密解密", command=cbc_window, height=2, width=23)
    cbc_button.place(relx=.5, y=280, anchor='center')

    root.mainloop()


if __name__ == '__main__':
    main_window()

