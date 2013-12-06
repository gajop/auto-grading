# -*- coding: utf-8 -*-
from base64 import b64decode
import traceback
import zipfile
import os.path

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from webservice.models import SubmitRequest, StudentAnswer, StudentAnswerFile, StudentAnswerTestResult, Task, TaskFile, User

from django.conf import settings
from webservice.matlab import invoker

def unzipFile(fileName, unzipFolderPath):
    zfile = zipfile.ZipFile(fileName)
    for name in zfile.namelist():
        #print "Decompressing " + name
        fd = open(os.path.join(unzipFolderPath, name), "w")
        fd.write(zfile.read(name))
        fd.close()

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers

import django.contrib.auth as django_auth

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['POST'])
def create_user(request):
    if request.user.is_superuser:
        username = request.DATA['username']
        password = request.DATA['password']
        first_name = request.DATA['first_name']
        last_name = request.DATA['last_name']
        is_active = request.DATA['is_active']
        try:
            user = User.objects.get(username=username)
            user.first_name = first_name
            user.last_name = last_name
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = is_active
        user.save()
        serializer = UserSerializer(user)
        return JSONResponse(serializer.data)

@csrf_exempt
def submit_answer(request):
    submitSuccessful = False
    submitMessage = []
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

        taskID = int(configOptions["task"])
        studentIndex = "".join(configOptions["student"].split()).upper()

        task = Task.objects.get(pk = taskID)
        departmentFromTask = task.courseSession.course.department
        try:
            student = User.objects.get(username = studentIndex)
        except User.DoesNotExist:
            submitMessage.append("Student sa indeksom \"" + str(studentIndex) + "\" nije ubeležen do sada.")
            #FIXME: user has no department field
            student = User(username = studentIndex, department = departmentFromTask)

            student.save()
        studentAnswer = StudentAnswer(student = student, task = task, submitRequest = submitRequest)
        studentAnswer.save()

        #attach all files
        for fileName in os.listdir(unzipFolderPath):
            filePath = os.path.join(unzipFolderPath, fileName)
            studentAnswerFile = StudentAnswerFile(studentAnswer = studentAnswer)
            studentAnswerFile.answerFile.save(fileName, File(open(filePath, "r")))
            studentAnswerFile.save()
            os.remove(filePath)

        print(studentAnswer.id)
        studentAnswerFile = StudentAnswerFile.objects.filter(studentAnswer = studentAnswer)[0]
        print(studentAnswerFile.studentAnswer.id)
        studentAnswerFolder = os.path.abspath(os.path.join(settings.MEDIA_ROOT, studentAnswerFile.answerFile.url, os.pardir))
        print(studentAnswerFolder)
        taskFile = TaskFile.objects.filter(task = task)[0]
        taskFolder = os.path.abspath(os.path.join(settings.MEDIA_ROOT, taskFile.taskFile.url, os.pardir))
        testResult = invoker.doTest(taskFolder, studentAnswerFolder)
        for i, line in enumerate(testResult.split("\n")):
            if "Zadatak netačan" in line:
                submitMessage.append(line)
            elif "Zadatak tačan" in line:
                submitMessage.append(line)
            elif "netačan" in line:
                testResult = StudentAnswerTestResult(studentAnswer = studentAnswer, success = False, resultText = "")
                testResult.save()
            elif "tačan" in line:
                testResult = StudentAnswerTestResult(studentAnswer = studentAnswer, success = True, resultText = "")
                testResult.save()

        submitSuccessful = True
    except Task.DoesNotExist:
        submitMessage.append("Nema zadatka sa tim brojem.")
    except:
        submitMessage.append("Interna greška.")
        traceback.print_exc()

    if not submitSuccessful:
        submitMessage.append("Slanje zadatka nije uspelo.")
    return HttpResponse("\n".join(submitMessage))
