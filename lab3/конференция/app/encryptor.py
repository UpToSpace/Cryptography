from des import *

class encryptor:
    @staticmethod
    def encrypt(enter: str, key: str, avalanche_effect: bool):
        result = ""
        blocks = des.processing_encode_input(des, enter,
                                             avalanche_effect)
        for block in blocks:
            irb_result = des.init_replace_block(des, block)
            block_result = des.iteration(des, irb_result, key,
                                         is_decode=False)
            block_result = des.end_replace_block(des,
                                                 block_result)
            result += block_result
        return result

    def decrypt(cipher_text: str, key: str):
        result = []
        cipher_text = str(hex(int(cipher_text.encode(), 2)))
        blocks = des.processing_decode_input(cipher_text)
        for block in blocks:
            irb_result = des.init_replace_block(des, block)
            block_result = des.iteration(des, irb_result, key,
                                         is_decode=True)
            block_result = des.end_replace_block(des,
                                                 block_result)
            for i in range(0, len(block_result), 8):
                result.append(block_result[i: i+8])
        return des.bit_decode(result)