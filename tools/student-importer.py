from __future__ import print_function
from bs4 import BeautifulSoup, NavigableString
import sys
import util
import argparse
import operator

global courseShortName
courseShortName = ""
class Student:
    def __init__(self, firstName, lastName, studentID, department):
        self.firstName = firstName
        self.lastName = lastName
        self.studentID = studentID
        self.department = department

    def __unicode__(self):
        return self.studentID + ", " + self.firstName + " " + self.lastName

    def __str__(self):
        return unicode(self).encode('utf-8')

def parseHTMLString(htmlString):
    soup = BeautifulSoup(htmlString)
    redniBrojTDTags = soup.find_all("td", text="Redni br.")
    students = []
    for redniBrojTDTag in redniBrojTDTags:
        redniBrojImePrezimeTR = redniBrojTDTag.parent
        studijskiProgramStr = redniBrojImePrezimeTR.parent.find("b").contents[0]
        studijskiProgramStr = studijskiProgramStr.split(":")[1].strip()

        studentTD = redniBrojImePrezimeTR.next_sibling
        while studentTD is not None:
            if not isinstance(studentTD, NavigableString):
                studentFields = studentTD.find_all("td")
                redniBrojStr = unicode(studentFields[0].contents[0])
                indexStr = unicode(studentFields[1].contents[0])
                indexStr = "".join(indexStr.split()).replace("\\","/")
                prezimeStr = unicode(studentFields[2].contents[0]).strip()
                imeStr = unicode(studentFields[3].contents[0]).strip()

                student = Student(imeStr, prezimeStr, indexStr, studijskiProgramStr)
                students.append(student)
            studentTD = studentTD.next_sibling

    return students

def uploadStudentsToSite(students):
    departments = util.getAllDepartments()

    courses = util.getAllCourses()
    courseSessions = util.getAllCourseSessions()
    course = None
    courseSession = None
    if courseShortName != "":
        for c in courses:
            if c["shortName"] == courseShortName:
                course = c
                for cs in courseSessions:
                    if cs["course"] == course["url"]:
                        if not cs["finished"] and (courseSession is None or courseSession["startDate"] < cs["startDate"]):
                            courseSession = cs
                break

    uploadedNumber = 0
    currentStudents = util.getAllStudents()
    for student in students:
        #checks if student already exists
        if len(currentStudents) > 0:
            studentExists = reduce(operator.add,
                    [ student.studentID == currentStudent["studentID"]
                        for currentStudent in currentStudents])
        else:
            studentExists = False
        if not studentExists or True:
            departmentID = None
            for department in departments:
                if department["name"].lower() == student.department.lower():
                    departmentID = department["url"]
                    break
            departmentIDFromCourse = course["department"] if course is not None else None
            if departmentID is None and departmentIDFromCourse is None:
                print("Cannot add student: " + unicode(student) + " with department (" + unicode(student.department) + ") because no valid course is specified or department doesn't match any of the predefined ones.")
                continue
            newStudent = util.addStudent(student.studentID, student.firstName, student.lastName, departmentID if departmentID is not None else departmentIDFromCourse)
            uploadedNumber += 1

            if departmentID != departmentIDFromCourse and departmentID is not None and departmentIDFromCourse is not None:
                print("Student's department doesn't belong to the course's department, student won't be linked to this course.")
                continue
            if course is None:
                print("Course isn't specified or is invalid.")
                continue
            if courseSession is None:
                print("No active course session found>")
                continue
            util.enrollStudent(newStudent["url"], courseSession["url"])

    return uploadedNumber

def importFromHTMLFile(f):
    htmlString = f.read()
    importFromHTMLString(htmlString)

def importFromHTMLString(htmlString):
    students = parseHTMLString(htmlString)
    print("Total students in HTML: " + str(len(students)))
    uploadedNumber = uploadStudentsToSite(students)
    print("Uploaded students: " + str(uploadedNumber))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse student list HTML files and populate the site.')
    parser.add_argument('FILE', nargs='+', type=argparse.FileType('r'))
    parser.add_argument('-c', '--course', default="", help="short name of the course")
    util.addArguments(parser)

    args = vars(parser.parse_args())
    util.parseArguments(args)
    files = args['FILE']
    courseShortName = args['course']

    for f in files:
        importFromHTMLFile(f)
