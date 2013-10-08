from django.db import models

#course dynamic
class SubmitRequest(models.model):
    taskID = models.IntegerField(null=True, blank=True)
    studentID = models.ForeignKey(Student)

class SubmitRequestTestResult(models.model):
    submitRequestID = models.ForeignKey(SubmitRequest)
    success = models.BooleanField()
    resultText = models.CharField(max_length=1000)

class SubmitRequestFiles(models.model):
    submitRequestID = models.ForeignKey(SubmitRequest)
    file = models.FileField()

#semester dynamic
class StudentEnrollment(models.model):
    startDate = models.DateField()
    studentID = models.ForeignKey(Student)
    courseSessionID = models.ForeignKey(CourseSession)
    finished = models.BooleanField()

class CourseSession(models.model):
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    finished = models.BooleanField()
    courseID = models.ForeignKey(Course)

class Task(models.model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    courseSessionID = models.ForeignKey(CourseSession)

#static
class Department(models.model):
    shortName = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)

class Course(models.model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

class Student(models.model):
    id = models.CharField(max_length=50)
    firstName = models.CharField(blank=True, max_length=50)
    lastName = models.CharField(blank=True, max_length=50)
