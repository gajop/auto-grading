from base64 import b64decode
import traceback
import zipfile
import os.path
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from models import SubmitRequest, StudentAnswer, StudentAnswerFile, StudentAnswerTestResult, \
        Task, Student

def unzipFile(fileName, unzipFolderPath):
    zfile = zipfile.ZipFile(fileName)
    for name in zfile.namelist():
        #print "Decompressing " + name
        fd = open(os.path.join(unzipFolderPath, name), "w")
        fd.write(zfile.read(name))
        fd.close()

@csrf_exempt
def submit_answer(request):
    submitSuccessful = False
    if request.method != 'POST':
        return HttpResponse(status=404)
    try:
        submitRequest = SubmitRequest()
        submitRequest.save()

        #get file data from POST
        encodedZipFileData = request.POST["zipFile"]
        #print(4 - len(encodedZipFileData) % 4)
        zipFileData = b64decode(encodedZipFileData + '=' * (4 - len(encodedZipFileData) % 4))

        #write file to filesystem
        tmpZipFileName = str(submitRequest.id) + ".zip"
        tmpZipFile = open(tmpZipFileName, "w")
        tmpZipFile.write(zipFileData)
        tmpZipFile.close()

        submitRequest.zipFile.save("task.zip", File(open(tmpZipFileName, "r")))
        submitRequest.save()
        os.remove(tmpZipFileName)

        #unzip file
        unzipFolderPath = os.path.join(os.path.dirname(submitRequest.zipFile.path), str(submitRequest.id))
        if not os.path.exists(unzipFolderPath):
            os.mkdir(unzipFolderPath)
        unzipFile(submitRequest.zipFile.path, unzipFolderPath)

        #parse config to extract student and task
        configFile = open(os.path.join(unzipFolderPath, "config.m"), "r")
        configOptions = {}
        for line in configFile.readlines():
            lineParts = line.strip().rstrip(";").split("=", 2)
            if len(lineParts) == 2:
                key = lineParts[0].strip()
                value = lineParts[1].strip().strip('"').strip()
                configOptions[key] = value

        studentIndex = "".join(configOptions["student"].split()).upper()
        taskID = int(configOptions["task"])

        student = Student.objects.get(studentID = studentIndex)
        task = Task.objects.get(pk = taskID)
        studentAnswer = StudentAnswer(student = student, task = task, submitRequest = submitRequest)
        studentAnswer.save()

        #attach all files
        for fileName in os.listdir(unzipFolderPath):
            filePath = os.path.join(unzipFolderPath, fileName)
            studentAnswerFile = StudentAnswerFile(studentAnswer = studentAnswer)
            studentAnswerFile.answerFile.save(fileName, File(open(filePath, "r")))
            studentAnswerFile.save()
            os.remove(filePath)
        
        submitSuccessful = True
    except:
        traceback.print_exc()
    submitMessage = "Submit failed."
    if submitSuccessful:
        submitMessage = "Submit success."
    return HttpResponse(submitMessage)
