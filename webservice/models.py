from django.db import models
from datetime import datetime

#static
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
    department = models.ForeignKey(Department)
    def __unicode__(self):
        return self.name

class Student(models.Model):
    studentID = models.CharField(max_length=50)
    firstName = models.CharField(blank=True, max_length=100)
    lastName = models.CharField(blank=True, max_length=100)
    department = models.ForeignKey(Department)
    def __unicode__(self):
        return self.studentID + ", " + self.firstName + " " + self.lastName

#semester dynamic
class CourseSession(models.Model):
    startDate = models.DateField(default=datetime.now, blank=True)
    endDate = models.DateField(null=True, blank=True)
    finished = models.BooleanField(default=False, blank=True)
    course = models.ForeignKey(Course)
    def __unicode__(self):
        return self.course.name + " " + unicode(self.startDate)

class StudentEnrollment(models.Model):
    startDate = models.DateField(default=datetime.now, blank=True)
    student = models.ForeignKey(Student)
    courseSession = models.ForeignKey(CourseSession)
    finished = models.BooleanField(default=False, blank=True)
    def __unicode__(self):
        return unicode(self.courseSession) + ": " + unicode(self.student)

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    courseSession = models.ForeignKey(CourseSession)
    def __unicode__(self):
        return self.name

#course dynamic
class SubmitRequest(models.Model):
    file = models.FileField(upload_to="submit_requests")
    def __unicode__(self):
        return unicode(self.studentAnswer) + " " + unicode(self.file.name)

class StudentAnswer(models.Model):
    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    submitRequest = models.ForeignKey(SubmitRequest)
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
    file = models.FileField(upload_to="student_answer_files")
    def __unicode__(self):
        return unicode(self.studentAnswer) + " " + unicode(self.file.name)
