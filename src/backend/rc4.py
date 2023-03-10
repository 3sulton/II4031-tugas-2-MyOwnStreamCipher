import base64
TOTAL_ASCII = 256

class rc4:
    def __init__(self) -> None:
        pass

    def init(self, P="", K="", C=""):
        # delete \n in end of character
        if P.endswith("\n"):
            P = P[:-1]
        if K.endswith("\n"):
            K = K[:-1]
        if C.endswith("\n"):
            C = C[:-1]
        # conver to byte array
        self.P = bytearray(P, "utf-8")
        self.K = bytearray(K, "utf-8")
        self.C = bytearray(C, "utf-8")

    def KSA(self):
        self.init_S()
        self.shuffle_S()

    def init_S(self):
        self.S = [i for i in range(TOTAL_ASCII)]

    def shuffle_S(self):
        len_k = len(self.K)
        j     = 0
        for k in range(len_k):
            for i in range(TOTAL_ASCII):
                j = (j + self.S[i] + self.K[i % len_k] + i) % TOTAL_ASCII
                self.S[i], self.S[j] = self.S[j], self.S[i]

    def PRGA(self, type):
        if type == "e":
            text = self.P
            result = self.P
        elif type == "d":
            text = self.C
            result = self.C
        i   = 0
        j   = 0
        idx = 0
        for idx in range (len(text)):
            i = (i + 1) % TOTAL_ASCII
            j = (j + self.S[i]) % TOTAL_ASCII
            self.S[i], self.S[j] = self.S[j], self.S[i]
            t1 = (self.S[i] + self.S[j]) % TOTAL_ASCII
            # extended vigenere cipher with len_k shift
            len_k = len(self.K)
            t2 = (t1 + len_k) % TOTAL_ASCII
            t3 = (self.S[(i >> 3) % TOTAL_ASCII] + self.S[j]) % TOTAL_ASCII
            t4 = (self.S[i] + self.S[(j << 5) % TOTAL_ASCII]) % TOTAL_ASCII
            result[idx] = ((((t1 ^ t2) % TOTAL_ASCII) + ((t3 + t4) % TOTAL_ASCII)) % TOTAL_ASCII) ^ text[idx] ^ j
        return result

    def bytearray_to_base64(self, text):
        return base64.b64encode(text)

    def base64_to_bytearray(self, text):
        return base64.b64decode(text)

    def encrypt(self, P, K):
        self.init(P=P, K=K)
        self.KSA()
        self.C = self.PRGA("e")
        # output dari encyption hanya bisa dalam bentuk base64
        return self.bytearray_to_base64(self.C).decode()

    def decrypt(self, C, K, isString=True):
        self.init(C=C, K=K)
        self.C = bytearray(self.base64_to_bytearray(self.C))
        self.KSA()
        self.P = self.PRGA("d")
        # output dari decrypt bisa berupa string atau base64
        # meskipun sebenarnya yang diharapkan pasti string sih
        try:
            if isString:
                return self.P.decode()
            return self.bytearray_to_base64(self.P).decode()
        except Exception as e:
            raise e

    def encrypt_file(self, file_path, K):
        self.init(K=K)
        with open(file_path, "rb") as file:
            self.P = bytearray(file.read())
        self.KSA()
        return self.PRGA("e")

    def decrypt_file(self, file_path, K):
        self.init(K=K)
        with open(file_path, "rb") as file:
            self.C = bytearray(file.read())
        self.KSA()
        return self.PRGA("d")

if __name__ == "__main__":
    r = rc4()
    assert r.encrypt("aku sayang kamu", "a") == "cdftPjG4/CpACo1MPXGw"
    print("We did it!")