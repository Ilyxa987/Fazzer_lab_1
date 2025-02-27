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
        changes = []
        for value in self.values:
            for i in range(1, 48):
                jam = list(self.orig)
                jam[i] = value
                changes.append({i: [list(self.orig)[i], value]})
                with open(filename, "wb") as f:
                    f.write(bytes(jam))
                code, eip = self.frid.run_process(exec_path)
                if int(eip, 0) > 0:
                    print(code, eip)
                    self.log(code, eip, changes)
                    stop = 1
                    break
                new_trace = self.tracer.start(exec_path)
                if new_trace != self.trace:
                    self.orig = bytes(jam)
                else:
                    changes.pop(len(changes) - 1)
            if stop:
                break

    def searchRazdel(self):
        razdels = []
        for i in range(len(self.orig)):
            if self.orig[i] in b"\";=,:":
                razdels.append(i)
        return razdels


    def fuzzField(self, filename : str, exec_path : str):
        razdels = self.searchRazdel()
        print(f"Было найдено {len(razdels) + 1} поля. Какой поле будем фазить?")
        fieldnum = int(input())
        print("Укажите количество символов")
        colvo = int(input())
        if fieldnum < len(razdels):
            index = razdels[fieldnum - 1]
        else:
            index = len(self.orig) - 1
        jam = list(self.orig)
        for i in range(colvo):
            jam.insert(index, self.values[0])
            index += 1
        with open(filename, "wb") as f:
            f.write(bytes(jam))
        code, eip = self.frid.run_process(exec_path)
        if int(eip, 0) > 0:
            print(code, eip)
        else:
            print("Программа не упала")

    def log(self, code, esp, change):
        with open("filelog.txt", "w") as f:
            f.write("Code: " + str(code) + " " + "esp: " + str(esp) + "\n")
            for i in range(len(change)):
                key = list(change[i].keys())[0]
                f.write(str(key) + ": " + str(change[i][key][0]) + " -> " + str(change[i][key][1]) + "\n")


