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
        for i in range(TOTAL_ASCII):
            j = (j + self.S[i] + self.K[i % len_k]) % TOTAL_ASCII
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
            t = (self.S[i] + self.S[j]) % TOTAL_ASCII
            result[idx] = self.S[t] ^ text[idx]
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
        # output dari encyption hanya bisa dalam bentuk base64
        if isString:
            return self.P.decode()
        return self.bytearray_to_base64(self.P).decode()

if __name__ == "__main__":
    r = rc4()
    print(r.encrypt("aku sayang kamu", "a"))

    print("We did it!")