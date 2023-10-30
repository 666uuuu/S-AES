# S_DES
## 作业报告
#### 第一关：基本测试

GUI界面设计：

菜单界面：  

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img.png>
</div>
​
<p align="center">图1 菜单界面</p>

点击第一个按钮后进入基础界面：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_1.png>
</div>
​
<p align="center">图2 基础界面</p>

当输入和密钥不符合规范时，会报错并提示重新输入（图3，图4，图5）：

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_2.png>
</div>
​<p align="center">图3 输入明密文</p>

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_3.png>
</div>
<p align="center">图4 明密文不合规</p>

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_4.png>
</div>
<p align="center">图5 密钥不合规</p>


测试明文：1111,0000,1111,0000     密钥：1010101010101010  
加密测试：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_5.png>
</div>
<p align="center">图6 加密测试</p>

生成密文：0011,0001,0010,0011  
解密测试：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_6.png>
</div>
<p align="center">图7 解密测试</p>

生成明文：1111,0000,1111,0000  
加解密结果匹配！

#### 第二关 交叉测试

我们组的二进制明文加密测试：  

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_7.png>
</div>
​														<p align="center">图8 我方二进制加密</p>


交叉测试组的加密结果：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_8.png>
</div>
​													<p align="center">图9 对方二进制加密</p>

9,15,9,8 即指 1001,1111,1001,1000,故密文相同  
交叉测试通过！



#### 第三关 扩展功能

我们的程序允许输入2Bytes的ASCII码字符串，并给出对应的ASCII码字符串密文(明文)，密钥要求是16bit二进制

密钥：1111111111

测试明文：cd 

<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_9.png>
</div>
​													<p align="center">图10 ASCII码字符串加密</p>
故测试明文 cd 生成密文：n¾ 

测试密文： n¾
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_10.png>
</div>
​													<p align="center">图11 ASCII字符串解密</p>
故测试密文 n¾ 生成明文： cd

加解密结果匹配

  

#### 第四关 多重加密

GUI界面：
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_11.png>
</div>
​										<p align="center">图12 多重加密界面</p>


###### 双重加密：   
输入16bits明密文和32bits密钥，密钥每16bits需换行    
测试明文：  
1111,0000,1111,0000  
密钥：  
1100110011001100  
0011001100110011
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_12.png>
</div>
​										<p align="center">图13 双重加密测试</p>

生成密文：1100,1011,1000,0110  
用该密文解密：
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_13.png>
</div>
​										<p align="center">图14 双重解密测试</p>
生成明文：1111,0000,1111,0000  

加解密结果匹配

###### 中间相遇攻击： 

我们组使用一组明密文对进行破解：  
明文：1111,0000,1111,0000  
密文：1011,0110,0111,1010  
找到的密钥较多，故只打印输出前16bits为0101111100001010的密钥  
破解时间及密钥为：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_14.png>
</div>
​										<p align="center">图15 输出结果</p>


###### 三重加密：  
我们组采用的是48bits模式(K1+K2+K3)    

输入格式要求：  
16bits明密文和48bits密钥，明密文每4bits用英文逗号隔开，密钥每16bits需换行

测试明文：  
1111,0000,1111,0000  
密钥：  
1100110011001100  
0011001100110011  
1010101010101010
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_15.png>
</div>
​										<p align="center">图16 三重加密测试</p>
生成密文：1001,0000,1000,0101

用该密文解密：
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_16.png>
</div>
​										<p align="center">图17 三重解密测试</p>

生成明文：1111,0000,1111,0000  


加解密结果匹配




#### 第五关：工作模式

GUI界面：
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_17.png>
</div>
​											<p align="center">图18 CBC加解密界面</p>

可通过三种方式输入明密文：  
1.直接在第一个文本框输入  
2.选择随机生成明密文，指定行数后会自动在第一个文本框随机生成相应行数的明密文  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_18.png>
</div>
​											<p align="center">图19 输入行数</p>
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_19.png>
</div>
​											<p align="center">图20 在文本框随机生成</p>
3.选择读取文件，在文本框中显示文件内容  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_20.png>
</div>​											
<p align="center">图21 选择文件</p>
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_21.png>
</div>
​											<p align="center">图22 在文本框显示</p>

加解密结束后可将文本框显示的结果保存为文件，方便后续操作  

测试：  
采用随机生成的明文进行测试  
密钥：111100001111000  
初始化向量：1010010110100101  
加密后将密文保存在ciphertexts文件中  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_22.png>
</div>
​											<p align="center">图23 CBC加密</p>  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_23.png>
</div>
​											<p align="center">图24 保存结果</p>  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_24.png>
</div>
​											<p align="center">图25 保存成功</p>  

读取ciphertexts文件输入文本框进行解密，并将生成的明文保存在plaintexts中：  
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_25.png>
</div>
​											<p align="center">图26 CBC解密</p>  
  
从（图23，图26）中可看出解密得到的结果与一开始随机生成的密文相同  

CBC加解密结果一致

在此基础上，把第一行的密文从1010,1011,1011,1101改为1111,0000,1111,0000进行解密：
<div align=center>
  <img src=https://github.com/666uuuu/S-AES/blob/main/images/img_26.png>
</div>
​											<p align="center">图27 修改密文后解密</p>  

从解密结果可以看出，图26与图27相比，明文结果只有前2行发生了变化
由此初步得出结论，对密文的部分修改并不会完全改变解密结果



# 用户指南


#### 1. 程序运行

运行`UI.py`文件或者命令行输入`python UI.py`




#### 2. 界面介绍

- 选择加解密模式：
- 基础及ASCII扩展功能
  - 选择明文编码语言：
    - Binary：当选择了Binary时，明密文应该输入**16位**的二进制字符，每4位用逗号隔开。
    - ASCLL：当选择了ASCLL时，明密文应该输入**2Byte**的字符
  - 密钥输入框：输入的密钥应该为**16位**的二进制数字。
  - 输出框：这里会显示加解密的结果，
  - 加密：则会以输入分别为明文和密钥，输出是对应密文。
- 多重加密解密：
  - 双重加密
  - 密钥输入框：输入的密钥应该为**16位**的二进制数字。
  - 输出框：这里会显示加解密的结果。
  - 多重加密
  - 密钥输入框：输入的密钥应该为**16位**的二进制数字。
  - 输出框：这里会显示加解密的结果。
- CBC加密解密：
  - 密钥输入框：输入的密钥应该为**16位**的二进制数字
  - 初始化向量输入框：输入的IV应该为**16位**的二进制数字
  - 输出框：这里会显示加解密的结果。


###### **案例**

- **案例1**：二进制，明文为：0101,0101,0101,0101，密钥为：0000000000000000，进行加解密。
- 输出结果：密文：1101,0001,1100,1000


- **案例2**：字符，明文为：aa，密钥为：0000000000000000，进行加解密。
- 输出结果：密文：


# 开发手册

**文件说明**

```tex
- AES.py：主要功能函数
        - key_expansion ：密钥扩展
	- add_round_key ：轮密钥加
	- sub_bytes ：字节替换
	- shift_rows ：行位移
	- gf_4_multiply ：GF(2^4)算法
	- mix_columns ：列混淆
	- xor_arrays ：异或操作
	- encrypt ：加密函数
	- decrypt ：解密函数
	
- ascii.py：ASCII码部分
	- binary_array_to_int ：将二进制数组转整型
	 
	
- crack.py：暴力破解部分函数，主要函数如下
	- find_keys ：破解函数
	
- CBC.py：CBC模式下的加解密
        - encrypt_cbc ：加密函数
        - decrypt_cbc ：解密函数 

	
- UI.py：UI界面实现部分

```



    
