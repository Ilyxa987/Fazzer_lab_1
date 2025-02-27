import frida
from time import sleep


class FridaCheck:
    exception_code: str
    eip: str
    js_code: str

    def __init__(self):
        self.exception_code = "No"
        self.eip = hex(0)
        # JavaScript-код для перехвата исключений
        self.js_code = """
            Process.setExceptionHandler(function (exception) {
                // Получаем код исключения
                var exceptionCode = exception.type;
                // Получаем значение регистра RIP (или EIP на 32-битных системах)
                var rip = exception.context.esp;
                var backtrace = Memory.readByteArray(rip, 64);
                //const process = Process.enumerateThreads()[0]; // Получаем первый поток
                //const backtrace = Context.context(); // Читаем стек
                

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
    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            if payload['type'] == 'exception':
                print(f"Exception occurred! Code: {payload['exceptionCode']}, RIP: {payload['rip']}")
                print(payload['backtrace'])
                self.exception_code = payload['exceptionCode']
                self.eip = payload['rip']
        else:
            print(message)

    def run_process(self, executable_path):
        try:
            # Запускаем процесс с помощью Frida
            pid = frida.spawn(executable_path)
            session = frida.attach(pid)

            # Внедряем JavaScript-код
            script = session.create_script(self.js_code)
            script.on('message', self.on_message)
            script.load()

            # Продолжаем выполнение процесса
            frida.resume(pid)

            # Ожидаем завершения процесса
            print(f"Process started with PID: {pid}")
            print("Press Ctrl+C to stop...")
            # sys.stdin.read()  # Ожидаем ввода, чтобы процесс не завершился сразу
            sleep(0.2)
            return self.exception_code, self.eip

        except Exception as e:
            print(f"An error occurred: {e}")
            return self.exception_code, self.eip
        finally:
            # Отсоединяемся от процесса
            if 'session' in locals():
                session.detach()
            return self.exception_code, self.eip
