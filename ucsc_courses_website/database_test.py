from email.mime import base
import mysql.connector




def getDatabase():
  mycursor = None
  try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="AsswordPay69",
      database = "UCSC_courses"
    )
    mycursor = mydb.cursor()
  except:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="AsswordPay69"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE UCSC_courses")
  return(mycursor, mydb)

def initTable():
  mycursor = None
  try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="AsswordPay69",
      database = "UCSC_courses"
    )
    mycursor = mydb.cursor()
  except:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="AsswordPay69"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE UCSC_courses")
  try:
    mycursor.execute("DROP TABLE COURSES2")
  except:
    print("TABLE ALREADY GONE")
  #mycursor.execute("CREATE TABLE COURSES (ID INT AUTO_INCREMENT PRIMARY KEY, Name varchar (255))")
  mycursor.execute("CREATE TABLE COURSES2 (ID INT AUTO_INCREMENT PRIMARY KEY, Name varchar (255), Class_Desc varchar (10000), Quarters varchar (255), Prereqs varchar (1000), Instructors varchar (1000), Credits int, GE VARCHAR (255), Repeatable int)")
  print("FINISHED")
# self.name = name
# self.desc = ""
# self.quarters = []
# self.prereqs = []
# self.instructors = []
# self.credits = 0
# self.ge = []
# self.repeatable = False

def testAdd(mycursor, mydb):
  print("ADD COURSE START")
  # base_insert_statement = "insert into COURSES (Name, Class_Desc, Quarters, Prereqs, Instructors, Credits, GE, Repeatable) values (%s, %s, %s, %s, %s, %d, %s, %d)"
  base_insert_statement = "insert into COURSES2 (Name) values (%s)"
  insertVal = ["TEST"]
  mycursor.execute(base_insert_statement, insertVal)  
  mydb.commit()
  mycursor.execute("SELECT * FROM COURSES2")
  allRows = mycursor.fetchall()
  for row in allRows:
    print(row)  


def testSelect(mycursor, mydb):
  mycursor.execute("SELECT Name FROM COURSES WHERE GE LIKE '%PR%' AND Name LIKE '%OAKS%'")
  allRows = mycursor.fetchall()
  for row in allRows:
    print(row)  
  print("NUMBER OF GE CLASSES: ", len(allRows))



def addCourses(courseList, mycursor, mydb):
  print("ADD COURSE START")
  base_insert_statement = "insert into COURSES2 (Name, Class_Desc, Quarters, Prereqs, Instructors, Credits, GE, Repeatable) values (%s, %s, %s, %s, %s, %s, %s, %s)"
  #base_insert_statement = "insert into COURSES (Name, Class_Desc, Quarters, Prereqs, Instructors, GE) values (%s, %s, %s, %s, %s, %s)"
  #base_insert_statement = "insert into COURSES (Name) values (%s)"
  for x in courseList:
    print("ADD COURSE")
    course = courseList[x]
    quarters = str(course.quarters).strip('[]')
    prereqs = str(course.prereqs).strip('[]')
    instructors = str(course.instructors).strip('[]')
    ge = str(course.ge).strip('[]')
    repeatable = 1 if course.repeatable else 0
    #insertVal = [course.name]
    #insertVal = [course.name, course.desc, quarters, prereqs, instructors, ge]
    insertVal = [course.name, course.desc, quarters, prereqs, instructors, str(course.credits), ge, str(repeatable)]
    mycursor.execute(base_insert_statement, insertVal)  
    mydb.commit()
  mycursor.execute("SELECT * FROM COURSES2")
  allRows = mycursor.fetchall()
  for row in allRows:
    print(row)
