from Fridacheck import FridaCheck
class Fuzzer:
    orig : bytes
    frid: FridaCheck

    def __init__(self, filename : str):
        with open(filename, "rb") as f:
            self.orig = f.read()
            self.frid = FridaCheck()

    def fuzz(self, filename: str, exec_path : str):
        for i in range(1, 48):
            jam = list(self.orig)
            jam[i] = 0xff
            with open(filename, "wb") as f:
                f.write(bytes(jam))
            code, eip = self.frid.run_process(exec_path)
            if int(eip, 0) > 0:
                print(code, eip)
                break



