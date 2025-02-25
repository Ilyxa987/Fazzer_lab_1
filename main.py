import sys
from fuzzer import Fuzzer
from Fridacheck import FridaCheck
from DynamoAnalyze import DynamoAnalyze


if __name__ == "__main__":
    # Укажите путь к исполняемому файлу
    #if len(sys.argv) < 2:
    #    print("Usage: python script.py <executable_path>")
    #    sys.exit(1)

    #executable_path = sys.argv[1]
    executable_path = "C:\\Users\\eprig\\Documents\\ProjectsOfMBKS\\lab1\\vuln13.exe"
    #myfuzz = Fuzzer('config_13')
    #myfuzz.fuzz('config_13', executable_path)
    d = DynamoAnalyze()
    d.start(executable_path)