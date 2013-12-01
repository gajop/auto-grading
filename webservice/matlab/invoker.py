# -*- coding: utf-8 -*-
import subprocess
import os.path

scriptPath = os.path.realpath(__file__)

def doTest(correctPath, submittedPath, tests):
    tests = tests.rstrip('.m')
    output = subprocess.call(["octave", "--eval", \
        "correctPath = '{0}'; submittedPath = '{1}'; tests='{2}'".format(correctPath, submittedPath, tests),
        os.path.join(os.path.dirname(scriptPath), "runner.m")])
    output = subprocess.check_output(["octave", "--eval", \
        "correctPath = '{0}'; submittedPath = '{1}'; tests='{2}'".format(correctPath, submittedPath, tests),
        os.path.join(os.path.dirname(scriptPath), "runner.m")])

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
            #submitMessage.append(line)
        elif "Zadatak tačan" in line:
            result["success"] = True
            #submitMessage.append(line)
        elif "netačan" in line:
            result["testResults"].append({"success":False, "msg":line})
        elif "tačan" in line:
            result["testResults"].append({"success":True, "msg":line})
    return result
