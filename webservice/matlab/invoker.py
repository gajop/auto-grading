import subprocess
import os.path

scriptPath = os.path.realpath(__file__)

def doTest(correctPath, submittedPath):
    output = subprocess.call(["octave", "--eval", \
        "correctPath = '{0}'; submittedPath = '{1}';".format(correctPath, submittedPath),
        os.path.join(os.path.dirname(scriptPath), "runner.m")])
    output = subprocess.check_output(["octave", "--eval", \
        "correctPath = '{0}'; submittedPath = '{1}';".format(correctPath, submittedPath),
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
    return "\n".join(lines)

if __name__ == "__main__":
    correctPath = "/home/gajop/automatic-grading-ftn/uploads/task_file/task_file/1"
    submittedPath = "/home/gajop/automatic-grading-ftn/uploads/student_answer_file/answer_file/1"
    print(doTest(correctPath, submittedPath))
