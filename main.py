import sys
from fuzzer import Fuzzer
from Fridacheck import FridaCheck


if __name__ == "__main__":
    # Укажите путь к исполняемому файлу
    #if len(sys.argv) < 2:
    #    print("Usage: python script.py <executable_path>")
    #    sys.exit(1)

    #executable_path = sys.argv[1]
    executable_path = r"C:\Users\eprig\Documents\ProjectsOfMBKS\lab1\vuln13.exe"
    myfuzz = Fuzzer('config_13')
    myfuzz.fuzz('config_13', executable_path)
    #frid = FridaCheck()
    #frid.run_process(executable_path)
    #run_process(executable_path)

    #print(exception_code, eip)

    #fuzz('config_13')