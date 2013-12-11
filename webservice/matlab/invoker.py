# -*- coding: utf-8 -*-
import os
import os.path

import subprocess
import sys
import json
from base64 import b64encode, b64decode

#hack that allows command to be imported in both VM and host
try:
    from webservice.command import Command
except:
    from command import Command

scriptPath = os.path.realpath(__file__)

def doTest(correctPath, submittedPath, tests):
    tests = tests.rstrip('.m')
    command = Command(["octave", "--eval", "correctPath = '{0}'; submittedPath = '{1}'; tests='{2}'".format(correctPath, submittedPath, tests), os.path.join(os.path.dirname(scriptPath), "runner.m")])
    status, output, error = command.run(timeout=5, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if status is None:
        result = {"success":False, "testResults":[{"success":False,"msg":"Isteklo vreme"}]}
        return result

    lines = []
    startPrint = False
    stopPrint = False
    for line in str(output).split("\n"):
        if line == "|||STARTPRINT|||":
            startPrint = True
        elif line == "|||ENDPRINT|||":
            startPrint = False
        elif startPrint:
            lines.append(line)

    resultStr = "\n".join(lines)
    result = {"success":False, "testResults":[]};
    for i, line in enumerate(resultStr.split("\n")):
        if "Zadatak netačan" in line:
            result["success"] = False
        elif "Zadatak tačan" in line:
            result["success"] = True
        elif "netačan" in line:
            result["testResults"].append({"success":False, "msg":line.split("||")[1]})
        elif "tačan" in line:
            result["testResults"].append({"success":True, "msg":line.split("||")[1]})

    if error:
        result["error"] = error
    return result

#invoked from docker
if __name__ == '__main__':
    jsonInput = sys.stdin.read()
    inputFiles = json.loads(jsonInput)
    os.mkdir('correct')
    os.mkdir('submitted')
    for filename, fileContent in inputFiles["correct"].iteritems():
        f = open(os.path.join('correct', filename), "w")
        f.write(b64decode(fileContent))
        f.close()
    for filename, fileContent in inputFiles["submitted"].iteritems():
        f = open(os.path.join('submitted', filename), "w")
        f.write(b64decode(fileContent))
        f.close()
    results = doTest('correct', 'submitted', inputFiles["tests"])
    print(json.dumps(results))
