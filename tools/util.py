import requests, base64
import json

url=""
username = ""
password = ""

### RPC ###
def removeObject(url):
    r = requests.delete(url, auth=(username, password))
    data = r.json()
    return data

# student #
def portalTest():
    r = requests.get(url + "/rest/users/", auth=(username, password))
    data = r.json()
    print(data)

def getAllStudents():
    r = requests.get(url + "/rest/users/", auth=(username, password))
    data = r.json()
    return data

def addStudent(studentID, firstName, lastName, department):
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url + "/rest/create_user/", data=json.dumps({
            "username":studentID,
            "password":studentID,
            "first_name":firstName,
            "last_name":lastName,
            "is_active":False,
        }),
        auth=(username, password), headers=headers)
    data = r.json()
    return data

# task #
def addTask(name, description, courseSessionURL):
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url + "/rest/tasks/", data=json.dumps({
            "name":name,
            "description":description,
            "courseSessionURL":courseSessionURL
        }),
        auth=(username, password), headers=headers)
    data = r.json()
    return data


def getAllTasks():
    r = requests.get(url + "/rest/tasks/", auth=(username, password))
    data = r.json()
    return data

# department #
def getAllDepartments():
    r = requests.get(url + "/rest/departments/", auth=(username, password))
    data = r.json()
    return data

# course #
def getAllCourses():
    r = requests.get(url + "/rest/courses/", auth=(username, password))
    data = r.json()
    return data

# course session #
def getAllCourseSessions():
    r = requests.get(url + "/rest/courseSessions/", auth=(username, password))
    data = r.json()
    return data

# student enrollment #
def getAllStudentEnrollments():
    r = requests.get(url + "/rest/studentEnrollments/", auth=(username, password))
    data = r.json()
    return data

def enrollStudent(studentID, courseSessionID):
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url + "/rest/studentEnrollments/", data=json.dumps({
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
