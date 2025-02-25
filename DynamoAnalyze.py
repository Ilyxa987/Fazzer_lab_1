import subprocess
import shlex
import GlobalSettings
import os

class DynamoAnalyze:

    def start(self, filename: str):
        command = [GlobalSettings.path_to_dynamo, '-t', 'drcov', '-dump_text', '-logdir', GlobalSettings.logdir, '--', filename]
        p = subprocess.call(command)
        if len(os.listdir(GlobalSettings.logdir)) == 1:
            print("DynamoRIO create trace")
            dirlist = os.listdir(GlobalSettings.logdir)
            with open(fr"{GlobalSettings.logdir}\{dirlist[0]}") as f:
                arr = f.read()

            os.remove(fr"{GlobalSettings.logdir}\{dirlist[0]}")


