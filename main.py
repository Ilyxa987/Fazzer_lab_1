from fuzzer import Fuzzer



if __name__ == "__main__":
    executable_path = "C:\\Users\\eprig\\Documents\\ProjectsOfMBKS\\lab1\\vuln13.exe"
    myfuzz = Fuzzer('config_13', executable_path)
    print("1 - автоматический фаззинг\n2 - фаззинг полей\nВыберите режим:")
    mode = int(input())
    if mode == 1:
        myfuzz.fuzz('config_13', executable_path)
    if mode == 2:
        myfuzz.fuzzField('config_13', executable_path)