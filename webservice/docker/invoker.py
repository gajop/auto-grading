# -*- coding: utf-8 -*-
import subprocess
import os.path
import os
import json
from base64 import b64decode, b64encode

import api

scriptPath = os.path.realpath(__file__)
MEMORY_LIMIT = "128M"

def doTest(correctPath, submittedPath, tests):
    filesDict = {"correct":{}, "submitted":{}, "tests":tests}
    for f in os.listdir(correctPath):
        fileContent = open(os.path.join(correctPath, f)).read()
        filesDict["correct"][f] = b64encode(fileContent)
    for f in os.listdir(submittedPath):
        fileContent = open(os.path.join(submittedPath, f)).read()
        filesDict["submitted"][f] = b64encode(fileContent)

    result = api.run("grading", "/usr/bin/python", "/invoker.py", stdin=json.dumps(filesDict), m=MEMORY_LIMIT)
    if result:
        try:
            result = json.loads(result)
        except:
            print("Failed to parse json: " + str(result))
    else:
        result = {"success":False, "testResults":[{"msg":"Container failed, sorry!", "success":False}]}
    return result
