from __future__ import print_function
import sys
import util
import argparse
import operator

courses = util.getAllCourses()
courseSessions = util.getAllCourseSessions()

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

class Task:
    def __init__(self, name, path, files, testFiles, courseShortName):
        self.name = name
        self.path = path
        self.files = files
        self.testFiles = testFiles
        self.courseShortName = courseShortName

    def __unicode__(self):
        return self.name + ", " + self.path + " files: " + str(self.files) + " testFiles: " + str(self.testFiles) + " course: " + self.courseShortName

    def __str__(self):
        return unicode(self).encode('utf-8')

tasks = []

import os

def parseDirStructure(topDir):
    blockedDirs = [ ".git", ".svn", ".cvs" ]
    for dirName, dirNames, fileNames in os.walk(topDir):
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        for blockedDir in blockedDirs:
            if blockedDir in dirNames:
                dirNames.remove(blockedDir)

        # print path to all filenames.
        for fileName in fileNames:
            if fileName == "config.py":
                configFile = {}
                exec(open(os.path.join(dirName, fileName)).read(), configFile)
                taskName = os.path.basename(dirName)
                courseShortName = os.path.basename(os.path.join(dirName, os.pardir))
                task = Task(taskName, dirName, configFile["files"],
                    configFile["testFiles"], courseShortName)
                tasks.append(task)

def getCourseSession(courses, courseShortName):
    for c in courses:
        if c["shortName"] == courseShortName:
            course = c
            for cs in courseSessions:
                if cs["course"] == course["url"]:
                    if not cs["finished"] and (courseSession is None or courseSession["startDate"] < cs["startDate"]):
                        courseSession = cs
            return courseSession



def syncTasks():
    courseNameSessionMap = {}
    tasksFromSite = util.getAllTasks()
    for taskFromSite in tasksFromSite:
        existsLocally = False
        for task in tasks:
            if task.name == taskFromSite["name"]:
                existsLocally = True
                break
        if not existsLocally:
            print("Removing " + taskFromSite["name"])
            util.removeObject(taskFromSite["url"])

    for task in tasks:
        existsOnSite = False
        for taskFromSite in tasksFromSite:
            if task.name == taskFromSite["name"]:
                existsOnSite = True
                break
        if not existsonSite:
            print("Adding " + task.name])
            util.addTask(task.name, task.description, courseSessionURL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize webservice tasks.')
    parser.add_argument('DIR', help="directory to sync", action="store")
    util.addArguments(parser)
    args = vars(parser.parse_args())
    util.parseArguments(args)

    print(util.getAllTasks())

    parseDirStructure(args["DIR"])
    syncTasks()
