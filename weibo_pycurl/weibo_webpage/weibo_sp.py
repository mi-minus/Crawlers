#coding:utf-8
import rsa
import binascii

def get_sp_rsa(passwd, servertime, nonce):
    # ���ֵ������prelogin�õ�,��Ϊ�ǹ̶�ֵ,����д��������
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
   
    
    weibo_rsa_e = 65537  # 10001��Ӧ��10����
    message = str(servertime) + '\t' + str(nonce) + '\n' + passwd
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    encropy_pwd = rsa.encrypt(message, key)
    return binascii.b2a_hex(encropy_pwd)
    
if __name__ =='__main__':
    print get_sp_rsa('123456',1459347244,"H1G2GP")