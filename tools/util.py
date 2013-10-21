import requests, base64
import json

url=""
username = ""
password = ""

### RPC ###
# student #
def portalTest():
    r = requests.get(url + "/students/", auth=(username, password))
    data = r.json()
    print(data)

def getAllStudents():
    r = requests.get(url + "/students/", auth=(username, password))
    data = r.json()
    return data

def addStudent(studentID, firstName, lastName, department):
    headers = {'Content-type': 'application/json'}
    r = requests.post(url + "/students/", data=json.dumps({
            "studentID":studentID,
            "firstName":firstName,
            "lastName":lastName,
            "department":department
        }),
        auth=(username, password), headers=headers)
    data = r.json()
    return data

# department #
def getAllDepartments():
    r = requests.get(url + "/departments/", auth=(username, password))
    data = r.json()
    return data

# course #
def getAllCourses():
    r = requests.get(url + "/courses/", auth=(username, password))
    data = r.json()
    return data

# course session #
def getAllCourseSessions():
    r = requests.get(url + "/courseSessions/", auth=(username, password))
    data = r.json()
    return data

# student enrollment #
def getAllStudentEnrollments():
    r = requests.get(url + "/studentEnrollments/", auth=(username, password))
    data = r.json()
    return data

def enrollStudent(studentID, courseSessionID):
    headers = {'Content-type': 'application/json'}
    r = requests.post(url + "/studentEnrollments/", data=json.dumps({
            "student":studentID,
            "courseSession":courseSessionID
        }),
        auth=(username, password), headers=headers)
    data = r.json()
    return data

### ARGS ###
def addArguments(parser):
    parser.add_argument('-u', '--username', default="")
    parser.add_argument('-p', '--password', default="")
    parser.add_argument('-l', '--url', default="http://localhost:8000")

def parseArguments(args):
    global username, password, url
    username = args['username']
    password = args['password']
    url = args['url']


if __name__ == "__main__":
    portalTest()
