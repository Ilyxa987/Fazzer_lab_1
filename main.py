import frida
import sys
from time import sleep

exception_code = 0
eip = 0

# JavaScript-код для перехвата исключений
js_code = """
Process.setExceptionHandler(function (exception) {
    // Получаем код исключения
    var exceptionCode = exception.type;
    // Получаем значение регистра RIP (или EIP на 32-битных системах)
    var rip = exception.context.esp;
    var backtrace = Memory.readByteArray(rip, 64);

    // Выводим информацию об исключении
    send({
        type: 'exception',
        exceptionCode: exceptionCode,
        rip: rip,
        backtrace: backtrace
    });

    // Продолжаем выполнение процесса
    return false;
});
"""

# Обработчик сообщений от Frida
def on_message(message, data):
    global exception_code, eip
    if message['type'] == 'send':
        payload = message['payload']
        if payload['type'] == 'exception':
            print(f"Exception occurred! Code: {payload['exceptionCode']}, RIP: {payload['rip']}")
            print(payload['backtrace'])
            exception_code = payload['exceptionCode']
            eip = payload['rip']
    else:
        print(message)

def print_hex_dump(data):
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_values = " ".join(f"{b:02X}" for b in chunk)
        ascii_values = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        print(f"{i:08x}  {hex_values.ljust(47)}  {ascii_values}")

def run_process(executable_path):
    try:
        # Запускаем процесс с помощью Frida
        pid = frida.spawn(executable_path)
        session = frida.attach(pid)

        # Внедряем JavaScript-код
        script = session.create_script(js_code)
        script.on('message', on_message)
        script.load()

        # Продолжаем выполнение процесса
        frida.resume(pid)

        # Ожидаем завершения процесса
        print(f"Process started with PID: {pid}")
        print("Press Ctrl+C to stop...")
        #sys.stdin.read()  # Ожидаем ввода, чтобы процесс не завершился сразу
        sleep(0.2)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Отсоединяемся от процесса
        if 'session' in locals():
            session.detach()

if __name__ == "__main__":
    # Укажите путь к исполняемому файлу
    if len(sys.argv) < 2:
        print("Usage: python script.py <executable_path>")
        sys.exit(1)

    executable_path = sys.argv[1]
    run_process(executable_path)

    print(exception_code, eip)