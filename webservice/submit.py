import os

from automatic_grading_ftn import settings

from webservice.models import Task, TaskFile, StudentAnswer, StudentAnswerTestResult, StudentAnswerFile
from webservice.matlab import invoker

#files is a tuple of (filename, file)
def processAnswer(task, student, files):
    studentAnswer = StudentAnswer(task = task, student = student)
    studentAnswer.save()

    #attach all files
    for filename, f in files:
        studentAnswerFile = StudentAnswerFile(studentAnswer = studentAnswer)
        studentAnswerFile.answerFile.save(filename, f)
        studentAnswerFile.save()

    studentAnswerFile = StudentAnswerFile.objects.filter(studentAnswer = studentAnswer)[0]
    studentAnswerFolder = os.path.abspath(os.path.join(settings.MEDIA_ROOT, studentAnswerFile.answerFile.url, os.pardir))

    taskFile = TaskFile.objects.filter(task = task)[0]
    taskFolder = os.path.abspath(os.path.join(settings.MEDIA_ROOT, taskFile.taskFile.url, os.pardir))

    results = {"success":True, "testResults":[]}
    for testTaskFile in TaskFile.objects.filter(task=task, fileType=TaskFile.T_TEST):
        result = invoker.doTest(taskFolder, studentAnswerFolder, testTaskFile.filename())
        if result["success"] != "success":
            results["success"] = False
        results["testResults"].extend(result["testResults"])


    for testResultDict in results["testResults"]:
        testResult = StudentAnswerTestResult(studentAnswer = studentAnswer, success = testResultDict["success"], resultText = "")
        testResult.save()

    return results
