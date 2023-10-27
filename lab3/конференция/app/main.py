from encryptor import *

if __name__ == '__main__':
     key = "cryptkey"
     text = "aveffect"
     ciphered = encryptor.encrypt(text, key, avalanche_effect=False)
     ciphered2 = encryptor.encrypt(text, key, avalanche_effect=True)
     plain = encryptor.decrypt(ciphered, key)
     print ("Сообщение: ", plain)
     print ("Шифротекст %r" % ciphered)
     print ("Шифротекст с измененным битом %r" % ciphered2)

     # 1. text = "hiworld"
     # 2. text = "byeworld"
     # 3. text = "desdes"
     # 4. text = "science"
     # 5. text = "computer"