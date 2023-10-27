import tables
import random

class des:
    def __init__(self):
        self.child_keys = []

    def avalanche_effect(binary_str: str, changed_bit_position: int) -> str:
        chunks, chunk_size = len(binary_str), 64 # изменяем один бит в каждом блоке
        byte_array = [binary_str[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        for i, b in enumerate(byte_array):
            b_list = list(b)
            b_list[changed_bit_position] = '1' if b_list[changed_bit_position] == '0' else '0'
            byte_array[i] = ''.join(b_list)
        return "".join(byte_array)

    @staticmethod
    def bit_encode(s: str) -> str:
        # Convert the string to bytes using UTF-8 encoding
        bytes_arr = s.encode('utf-8')
        # Convert each byte to its binary representation and join them
        binary_str = ''.join([f'{byte:08b}' for byte in bytes_arr])
        return binary_str

    @staticmethod
    def bit_decode(s: list) -> str:
        decoded = []
        for b in s:
            if(b != "00000000"):
                decimal_value = int(b, 2)
                character = chr(decimal_value)
                decoded.append(character)
        return ''.join(decoded)

    @staticmethod
    def replace_block(block: str, replace_table: tuple) -> str:
        """
                 Заменить отдельный блок
        Args:
                         block: str, 64-битная строка 01 для преобразования
                         replace_table: таблица преобразования
        Return:
                         Вернуть преобразованную строку
        """
        result = ""
        for i in replace_table:
            try:
                result += block[i - 1]
            except IndexError:
                print(i)
                raise
        return result

    def processing_encode_input(self, enter: str, avalanche_effect: bool) -> list:  # переводим в двоичку и добиваем нулями
        result = []
        bit_string = self.bit_encode(enter)
        # Если длина не делится на 64, добавить ноль
        if len(bit_string) % 64 != 0:
            bit_string += '0' * (64 - len(bit_string) % 64)
        print("Исходный открытый текст преобразован в двоичный:\n" + bit_string)
        if (avalanche_effect):
            bit_string = self.avalanche_effect(bit_string, 9)
            print("Сообщение с измененными битами: \n" + bit_string)
        result = [bit_string[i:i+64] for i in range(0, len(bit_string), 64)]
        return result

    @staticmethod
    def processing_decode_input(enter: str) -> list:
        result = []
        try:
            input_list = enter.split("0x")[1:]
            int_list = [int("0x" + i, 16) for i in input_list]
            for i in int_list:
                bin_data = str(bin(i))[2:]
                while len(bin_data) < 64:
                    bin_data = '0' + bin_data
                result.append(bin_data)
            return result
        except Exception as e:
            raise

    def key_conversion(self, key: str):
        """
                 Преобразуйте 64-битный исходный ключ в 56-битный ключ и выполните замену
        """
        key = self.bit_encode(key)
        while len(key) < 64:
            key += '0'
        first_key = key[:64]
        return self.replace_block(first_key, tables.key_conversion_table)

    def spin_key(self, key: str):
        """
                 Поверните, чтобы получить подключ
        """
        kc = self.key_conversion(self, key)
        first, second = kc[0: 28], kc[28: 56]
        for i in range(1, 17):
            first_after_spin = first[tables.spin_key_table[i - 1]:] + first[:tables.spin_key_table[i - 1]]
            second_after_spin = second[tables.spin_key_table[i - 1]:] + second[:tables.spin_key_table[i - 1]]
            yield first_after_spin + second_after_spin

    def key_selection_replacement(self, key: str):
        """
                 Получите 48-битный подключ, выбрав перестановку
        """
        # Сначала оставьте пустым
        self.child_keys = []
        for child_key56 in self.spin_key(self, key):
            self.child_keys.append(self.replace_block(child_key56, tables.key_selection_replacement_table))

    def init_replace_block(self, block: str):
        """
                 Выполнить замену начального состояния на блоке
        """
        return self.replace_block(block, tables.init_replace_block_table)

    def end_replace_block(self, block: str) -> str:
        """
                 Конвертация конечного состояния блока
        """
        return self.replace_block(block, tables.end_replace_block_table)

    @staticmethod
    def block_extend(block: str) -> str:
        """
                 Расширенная замена
        """
        extended_block = ""
        for i in tables.block_extend_table:
            extended_block += block[i - 1]
        return extended_block

    @staticmethod
    def not_or(a: str, b: str) -> str:
        """
                 XOR двух строк
        """
        result = ""
        size = len(a) if len(a) < len(a) else len(b)
        for i in range(size):
            result += '0' if a[i] == b[i] else '1'
        return result

    def s_box_replace(self, block48: str) -> str:
        """
        Замена блока S, преобразование 48-битного ввода в 32-битный вывод
        """
        result = ""
        for i in range(0, 48, 6):
            row = int(block48[i] + block48[i + 5], 2)
            col = int(block48[i + 1:i + 5], 2)
            data = tables.s_box_replace_table[i // 6][row][col]
            result += bin(data)[2:].zfill(4)
        return result

    def s_box_compression(self, num: int, block48: str) -> str:
        """
                 После расширения и замены сжатие S-блока выполняется на 48-битной строке 01. Состоит из двух частей:
                     1. XOR с ключом
                     2. Согласно таблице сжатия S-блока, 48 бит сжимаются до 36 бит.
        Args:
                         число: первая итерация
            block48: right
        Return:
                         Вернуть 32-битную строку 01, сжатую блоком S
        """
        result_not_or = self.not_or(block48, self.child_keys[num])
        return self.s_box_replace(self, result_not_or)

    def p_box_replacement(self, block32: str) -> str:
        """
                 Замена коробки P
        Return:
                         Вернуть 32-битную строку 01 после замены блока P
        """
        return self.replace_block(block32, tables.p_box_replacement_table)

    def f_function(self, right: str, is_decode: bool, num: int):
        right = self.block_extend(right)
        if is_decode:
            sbc_result = self.s_box_compression(self, 15 - num, right)
        else:
            sbc_result = self.s_box_compression(self, num, right)
        # print (f "Сжатый результат блока s: {sbc_result}")
        return self.p_box_replacement(self, sbc_result)

    def iteration(self, block: str, key: str, is_decode: bool) -> str: # 16 раундов шифрования
        self.key_selection_replacement(self, key)
        for i in range(16):
            left, right = block[0: 32], block[32: 64]
            next_left = right
            f_result = self.f_function(self, right, is_decode, i)
            right = self.not_or(left, f_result)
            block = next_left + right
            print("Раунд " + str(i + 1) + " значение блока: " + block[:32] + " " + block[32:])
        return block[32:] + block[:32]
