from database_test import *
from web_scraper_try import *

# initTable()

def runShit():
    (cursor, db) = getDatabase()
    print("GOT DB")
    initTable()
    courseList = returnCourseList()
    print("GOT COURSES")
    addCourses(courseList, cursor, db)
    print("ADDED COURSES")

def runTest():
    (cursor, db) = getDatabase()
    print("GOT DB")
    testAdd(cursor, db)
    print("ADDED COURSES")

print("START")
courseList = returnCourseList()
# courseList.sort(key = lambda x: x.name)

print("BEGIN")
runShit()

print("FINISH")