from Fridacheck import FridaCheck
from DynamoAnalyze import DynamoAnalyze
class Fuzzer:
    orig : bytes
    frid: FridaCheck
    tracer: DynamoAnalyze
    trace: list
    values: list

    def __init__(self, filename : str, exec_path : str):
        with open(filename, "rb") as f:
            self.orig = f.read()
            self.frid = FridaCheck()
            self.tracer = DynamoAnalyze()
            self.trace = self.tracer.start(exec_path)
            self.values = [0xFF, 0x01, 0x7F, 0x80, 0xFE, 0x00]

    def fuzz(self, filename: str, exec_path : str):
        stop = 0
        for value in self.values:
            for i in range(1, 48):
                jam = list(self.orig)
                jam[i] = value
                with open(filename, "wb") as f:
                    f.write(bytes(jam))
                code, eip = self.frid.run_process(exec_path)
                if int(eip, 0) > 0:
                    print(code, eip)
                    stop = 1
                    break
                new_trace = self.tracer.start(exec_path)
                if new_trace != self.trace:
                    self.orig = bytes(jam)
            if stop:
                break



