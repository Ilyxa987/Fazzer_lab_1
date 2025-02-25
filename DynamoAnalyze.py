import subprocess
import shlex
import GlobalSettings
import os
import re

class DynamoAnalyze:

    def start(self, filename: str):
        command = [GlobalSettings.path_to_dynamo, '-t', 'drcov', '-dump_text', '-logdir', GlobalSettings.logdir, '--', filename]
        p = subprocess.call(command)
        if len(os.listdir(GlobalSettings.logdir)) == 1:
            print("DynamoRIO create trace")
            dirlist = os.listdir(GlobalSettings.logdir)
            with open(fr"{GlobalSettings.logdir}\{dirlist[0]}") as f:
                arr = f.read()
                trace = self.creatTrace(arr)
            os.remove(fr"{GlobalSettings.logdir}\{dirlist[0]}")
            return trace

    def parse(self, arr : str):
        simple = r"module[[]  [0-1][]]: 0x[0-9a-f]*"
        match = re.finditer(simple, arr)
        return match

    def creatTrace(self, arr):
        match = self.parse(arr)
        trace = []
        for m in match:
            trace.append(m[0].split()[2])
        return trace

