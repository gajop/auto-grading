from datetime import datetime
from functools import partial
import os
import os.path

from django.db import models
from django.contrib.auth.models import User

def renameUploadedFile(className, dir, instance, fileName):
    if not instance.id:
        instance.save()
    return os.sep.join([className, dir, str(instance.id) + os.path.splitext(fileName)[1]])

def groupFilesForSubmitAnswer(className, dir, instance, fileName):
    parentFolder = os.sep.join([className, dir, str(instance.studentAnswer.id)])
    return os.sep.join([parentFolder, fileName])

def groupFilesForTask(className, dir, instance, fileName):
    parentFolder = os.sep.join([className, dir, str(instance.task.id)])
    return os.sep.join([parentFolder, fileName])


class FileFormat(models.Model):
    name = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name + " " + self.extension

#mostly static
class Department(models.Model):
    name = models.CharField(max_length=200)
    shortName = models.CharField(max_length=10)
    description = models.CharField(max_length=10000, blank=True)
    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    shortName = models.CharField(max_length=10)
    description = models.CharField(max_length=10000, blank=True)
    department = models.ForeignKey(Department, null=True)
    def __unicode__(self):
        return self.name

class CourseFileFormat(models.Model):
    course = models.ForeignKey(Course, related_name="fileFormats")
    fileFormat = models.ForeignKey(FileFormat)
    def __unicode__(self):
        return self.course + " : " + self.fileFormat

#dynamic semester (frequency)
class CourseSession(models.Model):
    startDate = models.DateField(default=datetime.now, blank=True)
    endDate = models.DateField(null=True, blank=True)
    finished = models.BooleanField(default=False, blank=True)
    course = models.ForeignKey(Course)
    def __unicode__(self):
        return self.course.name + " " + unicode(self.startDate)

class CourseSessionTeacher(models.Model):
    courseSession = models.ForeignKey(CourseSession)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return unicode(self.user) + " @ " + unicode(self.courseSession)

class StudentEnrollment(models.Model):
    startDate = models.DateField(default=datetime.now, blank=True)
    student = models.ForeignKey(User)
    courseSession = models.ForeignKey(CourseSession)
    finished = models.BooleanField(default=False, blank=True)
    def __unicode__(self):
        return unicode(self.courseSession) + ": " + unicode(self.student)

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    public = models.BooleanField(default=True, blank=True)
    courseSession = models.ForeignKey(CourseSession)
    def __unicode__(self):
        if self.public:
            return self.name
        else:
            return self.name + " (not public) "

class TaskFile(models.Model):
    task = models.ForeignKey(Task)
    taskFile = models.FileField(blank=False, null=False, upload_to=partial(groupFilesForTask, "task_file", "task_file"))
    fileFormat = models.ForeignKey(FileFormat, null=True)
    
    T_TEST = 1
    T_IMPLEMENTATION = 2
    TYPE_CHOICES = (
        (T_TEST, "Test"),
        (T_IMPLEMENTATION, "Implementation"),
    )
    fileType = models.IntegerField(choices=TYPE_CHOICES, null=True, blank=True)
    public = models.BooleanField(default=True, blank=True)
    def __unicode__(self):
        return unicode(self.task) + " " + unicode(self.taskFile.name) + " Test: " + unicode(self.fileType) + " Public: " + unicode(self.public)
    def filename(self):
        return os.path.basename(self.taskFile.name)

#course dynamic
class SubmitRequest(models.Model):
    zipFile = models.FileField(upload_to=partial(renameUploadedFile, "submit_request", "zip_file"))
    def __unicode__(self):
        return unicode(self.studentAnswer) + " " + unicode(self.zipFile.name)

class StudentAnswer(models.Model):
    task = models.ForeignKey(Task)
    student = models.ForeignKey(User)
    submitRequest = models.ForeignKey(SubmitRequest, blank=True, null=True)
    success = models.BooleanField(default=False, blank=True)
    def __unicode__(self):
        return unicode(self.student) + " " + unicode(self.task)

class StudentAnswerTestResult(models.Model):
    studentAnswer = models.ForeignKey(StudentAnswer)
    success = models.BooleanField()
    resultText = models.CharField(max_length=100000)
    def __unicode__(self):
        return unicode(self.studentAnswer) + " " + unicode(self.success)

class StudentAnswerFile(models.Model):
    studentAnswer = models.ForeignKey(StudentAnswer)
    answerFile = models.FileField(upload_to=partial(groupFilesForSubmitAnswer, "student_answer_file", "answer_file"))
    def __unicode__(self):
        return unicode(self.studentAnswer) + " " + unicode(self.answerFile.name)

#LTI models
class LTIUser(models.Model):
    lti_user_id = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User)

class LTICourse(models.Model):
    context_id = models.CharField(primary_key=True, max_length=100)
    course = models.ForeignKey(Course)
