sub_bytes_matrix = [
    ["63", "7c", "77", "7b", "12", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
    ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
    ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
    ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
    ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
    ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
    ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
    ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
    ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
    ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
    ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
    ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
    ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
    ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
    ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
    ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]
]
d = {
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
}

mix_columns_matrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
]

rcon_consts = {
    4: "01000000",
    8: "02000000",
    12: "04000000",
    16: "08000000",
    20: "10000000",
    24: "20000000",
    28: "40000000",
    32: "80000000",
    36: "1b000000",
    40: "36000000",
}


class Aes:
    def gf28_multiply(self, a, b, poly=0x11B):
        result = 0

        while b > 0:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:
                a ^= poly
            a &= 0xFF
            b >>= 1
        return result

    def xor_hex_numbers(self, hex1, hex2):
        num1 = int(hex1, 16)
        num2 = int(hex2, 16)

        result = num1 ^ num2

        return f"{result:08x}"

    def find_after_subword(self, tmp: str, is_simple: bool = True):
        after_subword = ''
        if not is_simple:
            after_rotword = tmp[2:] + tmp[:2]  # "5a5fd"
        else:
            after_rotword = tmp
        for a in range(1, len(after_rotword), 2):
            if after_rotword[a - 1].isalpha() and after_rotword[a].isdigit():
                after_subword += sub_bytes_matrix[d[after_rotword[a - 1]]][int(after_rotword[a])]
            elif after_rotword[a - 1].isdigit() and after_rotword[a].isalpha():
                after_subword += sub_bytes_matrix[int(after_rotword[a - 1])][d[after_rotword[a]]]
            elif after_rotword[a - 1].isalpha() and after_rotword[a].isalpha():
                after_subword += sub_bytes_matrix[d[after_rotword[a - 1]]][d[after_rotword[a]]]
            else:
                after_subword += sub_bytes_matrix[int(after_rotword[a - 1])][int(after_rotword[a])]
        return after_subword

    def after_subBytes_matrix(self, after_subBytes):
        res = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                res[j][i] = after_subBytes[j]
            after_subBytes = after_subBytes[j + 1:]
        return res

    def gen_key(self, input_key: str, cipher_key: str):
        db = {}
        # input_key = '3243f6a8885a308d313198a2e0370734'
        # cipher_key = '2b7e151628aed2a6abf7158809cf4f3c'  # ''.join([hex(ord(k))[2:] for k in key])
        w = [cipher_key[:8], cipher_key[8:16], cipher_key[16:24], cipher_key[24:32]]
        tmp = w[-1]
        for j in range(4, 44):
            if j % 4 == 0:
                after_rotword = tmp[2:] + tmp[:2]
                db.update({j - 3: {
                    "i": j,
                    "temp": tmp,
                    "after_rotword": after_rotword,
                    "after_subword": self.find_after_subword(tmp, False),
                    "rcon_const": rcon_consts[j],
                    "after_xor_with_rcon": self.xor_hex_numbers(self.find_after_subword(tmp, False), rcon_consts[j]),
                    "w_i_nk": w[j - 4 * (j // 4)],
                    "last_xor": self.xor_hex_numbers(
                        self.xor_hex_numbers(self.find_after_subword(tmp, False), rcon_consts[j]),
                        w[j - 4 * (j // 4)])
                }})
                tmp = db[j - 3]['last_xor']
                w[j - 4 * (j // 4)] = tmp
            else:
                db.update({j - 3: {
                    "i": j,
                    "temp": tmp,
                    "after_rotword": '',
                    "after_subword": '',
                    "rcon_const": '',
                    "after_xor_with_rcon": '',
                    "w_i_nk": w[j - 4 * (j // 4)],
                    "last_xor": self.xor_hex_numbers(tmp, w[j - 4 * (j // 4)])
                }})
                tmp = db[j - 3]['last_xor']
                w[j - 4 * (j // 4)] = tmp
        return db

    def create_after_shiftRows(self, after_subBytes_matrix_version):
        for i in range(4):
            after_subBytes_matrix_version[i] = after_subBytes_matrix_version[i][i:] + after_subBytes_matrix_version[i][
                                                                                      :i]
        return after_subBytes_matrix_version

    def make_separate_value(self, after_subBytes):
        seperated = ''.join(
            [f'{after_subBytes[i]} ' if i & 1 and i != 0 else after_subBytes[i] for i in range(len(after_subBytes))])
        return seperated.split()

    def make_mixColumn(self, after_subBytes_matrix_version, mix_columns_matrix):
        res = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                r = 0
                for k in range(4):
                    a = int(after_subBytes_matrix_version[k][j], 16)
                    b = mix_columns_matrix[i][k]

                    r ^= self.gf28_multiply(a, b)
                res[j][i] = f'{r:02x}'
        return res

    def make_matrix(self, s: str):
        return self.after_subBytes_matrix(self.make_separate_value(s))

    def encryption(self, tmp_start_of_round, tmp_round_key_value):
        encrypt_res = []
        for i in range(2):
            temp_round_key = ""
            for j in list(self.gen_key(tmp_start_of_round, tmp_round_key_value).values())[:4]:
                temp_round_key += j['last_xor']
            if i == 0:
                encrypt_res.append({
                    "start_of_round": self.make_matrix(tmp_start_of_round),
                    "round_key_matrix": self.make_matrix(tmp_round_key_value)
                })
            else:
                start_of_round = self.xor_hex_numbers(tmp_start_of_round, tmp_round_key_value)
                after_subBytes = self.find_after_subword(start_of_round)
                after_subBytes_matrix_version = self.make_matrix(after_subBytes)
                after_shiftRows = self.create_after_shiftRows(after_subBytes_matrix_version)
                after_MixColumn = self.make_mixColumn(after_shiftRows, mix_columns_matrix)
                start_of_round_second = self.after_subBytes_matrix(
                    self.make_separate_value(self.xor_hex_numbers(''.join(sum(after_MixColumn, [])), temp_round_key)))
                res_mix_column = [[0 for _ in range(4)] for _ in range(4)]
                for i in range(len(after_MixColumn)):
                    for j in range(len(after_MixColumn[i])):
                        res_mix_column[j][i] = after_MixColumn[i][j]
                encrypt_res.append({
                    "start_of_round": self.make_matrix(start_of_round),
                    "after_subBytes": self.make_matrix(after_subBytes),
                    "after_shiftRows": after_shiftRows,
                    "after_MixColumn": res_mix_column,
                    "round_key_matrix": self.make_matrix(temp_round_key),
                })
            print(encrypt_res)
        encrypt_res.append(
            {"start_of_round": start_of_round_second,
             "after_subBytes": self.make_matrix(self.find_after_subword(
                 self.xor_hex_numbers(''.join(sum(after_MixColumn, [])), temp_round_key)))
             })
        return {
            "ciphertext": start_of_round_second,
            "encrypting": encrypt_res
        }

# print(Aes().encryption("3243f6a8885a308d313198a2e0370734", "2b7e151628aed2a6abf7158809cf4f3c"))
