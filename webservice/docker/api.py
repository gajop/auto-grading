from subprocess import Popen, PIPE
import time
import os
import logging

logging = logging.getLogger("webservice.docker.api")

def run(image, command, *args, **kwargs):
    invocation = ["/usr/bin/docker", "run"]
    if "stdin" in kwargs:
        invocation.extend(["-i", "-a", "stdin"])
    invocation.extend([image, command])
    invocation.extend(list(args))

    logging.info("Invocation: " + str(invocation))
    pRun = Popen(invocation, stdin=PIPE, stdout=PIPE)
    processID = pRun.communicate(kwargs["stdin"] if "stdin" in kwargs else "")[0]

    logging.info("ProcessID: " + processID)    
    #pLogs = Popen(["/usr/bin/docker", "logs", processID], stdout=PIPE, stderr=PIPE)
    #retVal = pLogs.communicate()[0]
    for i in range(10): #wait for up to 10s
        retVal = os.popen("".join(["/usr/bin/docker ", "logs ", processID])).read()
        if retVal != "":
            logging.info("Took " + str(i) + " seconds to get result from docker.")
            return retVal
        time.sleep(1)
    return None
