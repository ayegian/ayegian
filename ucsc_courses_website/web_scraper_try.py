from types import new_class
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


course_list = []
exam_list = set()
prereq_not_counted = set()
possible_restrictions = ['sophomore','junior', 'senior', 'graduate']

class Student:
    def __init__(self, name):
        self.name = name
        self.majors = []
        self.minors = []
        self.classes_taken = []
        self.exam_scores = []
        
        
    
    def add_major(self, new_major):
        self.majors.append(new_major)

    def add_minor(self, new_minor):
        self.minors.append(new_minor)

    def add_class_taken(self, new_class):
        #print("TAKE CLASS: ", new_class)
        self.classes_taken.append(new_class)

    def can_take_class(self, reqs, or_true):
        cond = []
        for x in reqs:
            if(type(x) == list):
                ##print("LIST")
                cond.append(self.can_take_class(x, (not or_true)))
            else:
                cond.append((x in self.classes_taken)or(not x in course_list and not x in exam_list))
        ##print(cond)
        if or_true:
            return True in cond or len(cond) == 0
        else:
            return (not (False in cond)) or len(cond) == 0


class Major:
    def __init__(self, name):
        self.name = name
        self.classes = set()

    def add_class(self, new_class):
        self.classes.add(new_class)

    def can_take_class(self, course):
        for x in course.prereqs:
            print("PREREQ: ", x)
            

class Course:
    def __init__(self, name):
        self.name = name
        self.desc = ""
        self.quarters = []
        self.prereqs = []
        self.instructors = []
        self.credits = 0
        self.ge = []
        self.repeatable = False
        self.restricted = set()
    
    def set_desc(self, desc):
        desc_split = desc.lower().split('.')
        for x in desc_split:
            ##print("DESC SPLIT: ", x)
            if "enrollment is restricted to " in x or "enrollment restricted to " in x:
                for y in possible_restrictions:
                    if y in x:
                        self.restricted.add(y)
        self.desc = desc

    def set_credits(self, credits):
        self.credits = credits

    def add_quarter(self, quarter):
        self.quarters.append(quarter)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)

    def add_prereq(self, prereq):
        self.prereqs.append(prereq)

    def add_ge(self, ge):
        self.ge.append(ge)

    def set_repeatable(self, rep):
        self.repeatable = rep
        
    def print_course(self):
        print("Name: ",self.name,"\nDescription: ",self.desc,"\nGE: ", self.ge,"\nCredits: ", self.credits,"\nQuarters Offered: ",str(self.quarters).strip("[]"),"\nInstructors: ",str(self.instructors).strip("[]"),"\nPrerequisites: ",str(self.prereqs)+"\nRepeatable: ",str(self.repeatable),"\nRestricted: ",str(list(self.restricted)), " Len: ", len(self.restricted))




def split_prereq(pre_bef_split, append_to_list, cur_course, req_list, course_list, restrict_set, started = False, from_and = False):
    #SPLIT ON ORS, 
    ##print("PRE BEF SPLIT: ", pre_bef_split)


    #split_1 = pre_bef_split.split("; or ")




    # split_2 = []
    # for x in split_1:
    #     split_3 = x.split(".")
    #     for y in split_3:
    #         split_2.append(y)
    # split_1 = split_2
    if(started == False):
        ret_list = []
        semi_indexes =  re.finditer(pattern='; or ', string=pre_bef_split)
        semi_indexes = [index.start() for index in semi_indexes]
        split_1 = []
        start_ind = 0
        for x in range(len(semi_indexes)):
            split_1.append(pre_bef_split[start_ind:semi_indexes[x]])
            start_ind = semi_indexes[x] + 5
        split_1.append(pre_bef_split[start_ind:])
        ##print("SPLIT 1 LEN: ", len(split_1))
        for y in split_1:
            if("enrollment is restricted to " in y.lower()):
                #print("ENROLLMENT RESTRICTED 1")
                #print(y)
                for z in possible_restrictions:
                    if z in y.lower():
                        restrict_set.add(z)
                #continue
            # if("placement score of " in y.lower() or "exam score of " in y.lower()):
            #     exam_list.add(y)
            # if "or higher" in y.lower():
            #     exam_list.add(y)
            ##print("Y IN SPLIT ONE")
            new_list = []
            #new_list.append(y)
            new_list2 = []
            split_prereq(y, new_list2, cur_course, new_list, course_list, restrict_set, True)
            ##print("ADD PREREQ: ",new_list)
            #cur_course.add_prereq(new_list
            # for x in new_list:
            #     x = x.strip()
            ret_list.append(new_list)
        return(ret_list)
            #break_flag = True
    else:

        com_indexes =  re.finditer(pattern=', and | and |, |; and ', string=pre_bef_split)
        #com_indexes =  re.finditer(pattern=', and ', string=pre_bef_split)
        #and_indexes =  re.finditer(pattern='(, and | and |, )', string=pre_bef_split)
        and_indexes = [index.span() for index in com_indexes]
        split = []
        start_ind = 0
        ##print("LEN START: ", len(and_indexes))
        for x in range(len(and_indexes)):
            ##print("AND INDEX: ",and_indexes[x])
            split.append(pre_bef_split[start_ind:and_indexes[x][0]])
            #ADD SIZE OF PATTERN MATCHED TO START IND
            start_ind = and_indexes[x][1]
        split.append(pre_bef_split[start_ind:])
        split_2 = []
        split_inds = []
        ##print("SPLIT LIST: ", split)
        for x in range(len(split)-1):
            ##print("SPLIT SPACE 1: ", split[x])
            ##print("SPLIT SPACE 2: ", split[x+1])

            split_spaces_1 = split[x].split(" ")
            split_spaces_2 = split[x+1].split(" ")
            name_1 = ""
            name_2 = ""
            if len(split_spaces_1)>1:
                name_1 = split_spaces_1[-2]+" "+split_spaces_1[-1]
            # else:
            #     #print("SMALL SPLIT: ", split_spaces_1)
            if len(split_spaces_2)>1:
                name_2 = split_spaces_2[0]+" "+split_spaces_2[1]
            # else:
            #     #print("SMALL SPLIT: ",split_spaces_2)
            if not(name_1 in course_list) and not(name_2 in course_list):
                #DONT SPLIT HERE
                ##print("NAME 1: "+name_1)
                ##print("NAME 2: "+name_2)
                prereq_not_counted.add(name_1)
                prereq_not_counted.add(name_2)
                #and_indexes[x-1] = -1
                and_indexes[x] = -1
                              
        while -1 in and_indexes:
            ##print("REMOVE")
            and_indexes.remove(-1)

        split = []
        start_ind = 0
        for x in range(len(and_indexes)):
            split.append(pre_bef_split[start_ind:and_indexes[x][0]])
            start_ind = and_indexes[x][1]
        split.append(pre_bef_split[start_ind:])

        if len(split) > 1:
            ##print("FULL AND SPLIT: ", str(split))
            for x in split:
                if("enrollment is restricted to " in x.lower()):
                    #print("ENROLLMENT RESTRICTED 2")
                    #print(x)
                    for y in possible_restrictions:
                        if y in x.lower():
                            restrict_set.add(y)
                # if "or higher" in x.lower():
                #     exam_list.add(x)
                    #continue
                # if("placement score of " in x.lower() or "exam score of " in x.lower()):
                #     exam_list.add(x)
                ##print("AND SPLIT: ", x)
                new_list = []
                split_prereq(x, new_list, cur_course, req_list, course_list, restrict_set, True, True)
                req_list.append(new_list)
                ##print("LEN NEW LIST: ", len(new_list))


    # else:
    #     split = pre_bef_split.split(' and ')
    #     #print("AFTER SPLIT: ", split)
    #     if len(split) > 1:
    #         for x in split:
    #             new_list = []
    #             split_prereq(x, new_list, cur_course, req_list, course_list)
    #             #print("LEN NEW LIST: ", len(new_list))

        else:
            
            or_indexes =  re.finditer(pattern=' or ', string=pre_bef_split)
            or_indexes = [index.start() for index in or_indexes]
            split = []
            start_ind = 0
            for x in range(len(or_indexes)):
                split.append(pre_bef_split[start_ind:or_indexes[x]])
                start_ind = or_indexes[x] + 4
            split.append(pre_bef_split[start_ind:])
            split_2 = []
            split_inds = []
            for x in range(len(split)-1):
                split_spaces_1 = split[x].split(" ")
                split_spaces_2 = split[x+1].split(" ")
                name_1 = ""
                name_2 = ""
                if len(split_spaces_1)>1:
                    name_1 = split_spaces_1[-2]+" "+split_spaces_1[-1]
                # else:
                #     #print("SMALL SPLIT: ", split_spaces_1)
                if len(split_spaces_2)>1:
                    name_2 = split_spaces_2[0]+" "+split_spaces_2[1]
                # else:
                #     #print("SMALL SPLIT: ",split_spaces_2)
                #DONT SPLIT IF NEITHER NAME 1 OR NAME 2 ARE NOT IN COURSE LIST
                if not(name_1 in course_list) and not(name_2 in course_list):
                    #DONT SPLIT HERE
                    or_indexes[x] = -1
                               
            while -1 in or_indexes:
                or_indexes.remove(-1)

            split = []
            start_ind = 0
            for x in range(len(or_indexes)):
                split.append(pre_bef_split[start_ind:or_indexes[x]])
                start_ind = or_indexes[x] + 4
            split.append(pre_bef_split[start_ind:])
            if len(split) == 0:
                # #print("LENGTH OF OR SPLIT IS 0")
                append_to_list.append(pre_bef_split)
            for x in split:
                if("enrollment is restricted to " in x.lower()):
                    #print("ENROLLMENT RESTRICTED 3")
                    #print(x)
                    for y in possible_restrictions:
                        if y in x.lower():
                            restrict_set.add(y)
                    continue
                #if("placement score of " in x.lower() or "exam score of " in x.lower()) or "placement score of " in x.lower():
                if "or higher" in x.lower():
                    exam_list.add(x)
                  #  continue
                # #print("OR SPLIT: ",x)
                x = x.strip()
                #req_list.append(x)
                if(from_and == False):
                    req_list.append(x)
                else:
                    append_to_list.append(x)
        
        # else:
        #     or_indexes =  re.finditer(pattern=' or ', string=pre_bef_split)
        #     or_indexes = [index.start() for index in or_indexes]
        #     higher_indexes = re.finditer(pattern=' or higher ', string=pre_bef_split)
        #     higher_indexes = [index.start() for index in higher_indexes]
        #     for x in higher_indexes:
        #         if x in or_indexes:
        #             or_indexes.remove(x)
        #     split = []
        #     start_ind = 0
        #     for x in range(len(or_indexes)):
        #         split.append(pre_bef_split[start_ind:or_indexes[x]])
        #         start_ind = or_indexes[x] + 4
        #     split.append(pre_bef_split[start_ind:])
        #     for x in split:
        #         #print("SPLIT: ",x)
        #         req_list.append(x)
num_list = ["one ","two ","three ","four ","five ","six ","seven ","eight ","nine ","ten ","all ", "dc "]

def scrape_majors(course_list):
    url_to_scrape = "https://catalog.ucsc.edu/en/Current/General-Catalog/Academic-Programs/Bachelors-Degrees"
    request_page = urlopen(url_to_scrape)
    page_html = request_page.read()
    request_page.close()
    html_soup = BeautifulSoup(page_html, 'html.parser')
    #for price in html_soup.find_all(“p”, class_=”price_color”):
    #for data in html_soup.select("ul", class_ = "sc-child-item-links"): 
    #    #print("DATA: "+data.get_text()) 
        # for title in data.find_all(‘a’):    
        #     #print(title.get_text())
    ##print("LEN: ",len(data))
    major_list = {}

    for data in html_soup.find_all('div', class_="combinedChild"):
        data = data.next_sibling
        #print(data)
        for major_link in data.find_all('a', href=True):
            #print("MAJOR: ", major_link.get_text())
            major = Major(major_link.get_text())
            major_list[major_link.get_text()] = major
            link = major_link['href']
            #print("MAJOR LINK: ", major_link['href'])
            url_to_scrape = url_to_scrape[0:url_to_scrape.index(link[1:link.index('/',1)])-1]
            url_to_scrape += link
            ##print("URL TO SCRAPE: "+url_to_scrape)
            course_page = urlopen(url_to_scrape)
            course_html = course_page.read()
            course_page.close()
            course_soup = BeautifulSoup(course_html, 'html.parser')
            for section in course_soup.find_all('h5', class_ = "sc-RequiredCoursesHeading3"):
                text = section.get_text().strip().lower()
                #print(text)
                num = -1
                options = 0
                for x in range(len(num_list)):
                    if num_list[x] in text:
                        ##print("X: ", x)
                        num = x
                        break
                #print("NUM: ", num)
                if(" options" in text):
                    options = 1
                if num == -1:
                    continue
                #print(text)
                if options:
                    heading = section.find_next_sibling('h6', class_ = "sc-RequiredCoursesHeading4")
                    if(heading == None):
                        course_table = section.find_next_sibling("table")                                
                        courses = course_table.find_all('td', class_ = "sc-coursenumber")
                        for course in courses:
                            poss_names = course.find_all('a')
                            for poss_name in poss_names:
                                if(poss_name.get_text() in course_list):
                                    #print("COURSE: ", poss_name.get_text())
                                    major.add_class(poss_name.get_text())
                    while heading != None and True:
                        #print("HEADING", heading)
                        course_table = heading.find_next_sibling("table")                                
                        courses = course_table.find_all('td', class_ = "sc-coursenumber")
                        for course in courses:
                            poss_names = course.find_all('a')
                            for poss_name in poss_names:
                                if(poss_name.get_text() in course_list):
                                    #print("COURSE: ", poss_name.get_text())
                                    major.add_class(poss_name.get_text())
                        heading = heading.find_next_sibling('h6', class_ = "sc-RequiredCoursesHeading4")
                        if(heading == None or "Or " not in heading.get_text()):
                            break
                else:
                    course_table = section.find_next_sibling("table")                                
                    courses = course_table.find_all('td', class_ = "sc-coursenumber")
                    for course in courses:
                        poss_names = course.find_all('a')
                        for poss_name in poss_names:
                            if(poss_name.get_text() in course_list):
                                #print("COURSE: ", poss_name.get_text())
                                major.add_class(poss_name.get_text())

                       # else:
                        #    #print("NOT COURSE: ", poss_name.get_text())
            break
        break
    return major_list

def scrape_courses():
    url_to_scrape = "https://catalog.ucsc.edu/Current/General-Catalog/Courses"
    #url_to_scrape = "https://catalog.ucsc.edu/en/Current/General-Catalog/Courses/LALS-Latin-American-and-Latino-Studies"
    request_page = urlopen(url_to_scrape)
    page_html = request_page.read()
    request_page.close()
    html_soup = BeautifulSoup(page_html, 'html.parser')
    #for price in html_soup.find_all(“p”, class_=”price_color”):
    #for data in html_soup.select("ul", class_ = "sc-child-item-links"): 
    #    #print("DATA: "+data.get_text()) 
        # for title in data.find_all(‘a’):    
        #     #print(title.get_text())
    data = html_soup.find_all('ul', class_="sc-child-item-links")
    ##print("LEN: ",len(data))
    course_list = {}

    break_flag = False
    for data in html_soup.find_all('ul', class_="sc-child-item-links"): 
        ##print("DATA: "+data.get_text()) 
        for course_link in data.find_all('a', href = True):
            ##print("LINK: "+ course_link['href'])
            link = course_link['href']
            ##print(link.index('/', 1))
            link = link[link.index('/', 1):]
            ##print("LINK NO EN: ",link)
            ##print("SHOULD BE CURRENT: ",link[1:link.index('/',1)])
            url_to_scrape = url_to_scrape[0:url_to_scrape.index(link[1:link.index('/',1)])-1]
            url_to_scrape += link
            ##print("URL TO SCRAPE: "+url_to_scrape)
            course_page = urlopen(url_to_scrape)
            course_html = course_page.read()
            course_page.close()
            course_soup = BeautifulSoup(course_html, 'html.parser')
                # for course in course_soup.find_all('div', class_="combinedChild"): 
                #     #print("COMBINED CHILD: ",course.get_text())
            text = course_soup.find_all('h2', class_ = "course-name")
            if len(text) == 0:
                break
            text = text[0]
            #print("COURSE NAME: "+text.get_text().strip())



            # course_name = text.get_text().strip()
            # if(course_name.__contains__("LALS 1 ")):
            #     print("LALS 1 HERE")
            # cur_course = Course(course_name)
            # course_split = course_name.split(" ")
            # name = course_split[0]+" "+course_split[1]
            # course_list[name] = cur_course


            first = True

            printStuff = False

            #course_list.append(cur_course)
            while True:

                if printStuff:
                    print("PRINT COURSE")
                    cur_course.print_course()
            #CHECK TO SEE IF THERE IS A NEXT SIBLING, IF NOT BREAK
                if(first):
                    first = False
                else:
                    text = text.next_sibling
            #REMOVE ALL WHITESPACE
                if text is None:
                ##print("TEXT IS NONTYPE")
                    break
                if printStuff:                   
                    print("START:")
                    print(text)
                    print("END:")
                no_white = ''.join(text.get_text().split())
                if(len(no_white) == 0):
                ##print("NOTHING HERE")
                    continue
            ##print("ATTRIBUTE: ",text.attrs['class'][0])
                if(text.attrs['class'][0] == 'course-name'):
                ##print("COURSE NAME: "+text.get_text())
                #cur_course.#print_course()
                    if break_flag:
                        break
                    course_name = text.get_text().strip()
                    #print("COURSE NAME: ", course_name)
                    cur_course = Course(course_name)
                    course_split = course_name.split(" ")
                    name = course_split[0]+" "+course_split[1]
                    # print("NAME: ", name)
                    if name == "LALS 1":
                        printStuff = True
                    elif name == "LALS 5":
                        printStuff = False
                    course_list[name] = cur_course
                if(text.attrs['class'][0] == 'desc'):
                    ##print("DESCRIPTION: "+text.get_text())
                    # if printStuff:
                    #     print("PRINT COURSE")
                    #     cur_course.print_course()
                    #     print("LALS 1 SET DESC: ", text.get_text().strip())
                    cur_course.set_desc(text.get_text().strip())
                    # if printStuff:
                    #     print("PRINT COURSE AFTER")
                    #     cur_course.print_course()
                if(text.attrs['class'][0] == 'sc-credithours'):
                    ##print("CREDIT HOURS: ", text.get_text())
                    children = text.findChildren()
                    for x in children:
                        if(x.name == 'div'):
                            ##print("CREDITS: ",x.get_text().strip())
                            cur_course.set_credits(int(x.get_text().strip()))
                if(text.attrs['class'][0] == 'instructor'):
                    children = text.findChildren()
                    for x in children:
                        if(x.name == 'p'):
                            ##print("INSTRUCTORS: ",x.get_text().strip())
                            instructors = x.get_text().strip().split(',')
                            for y in instructors:
                                cur_course.add_instructor(y.strip())
                if(text.attrs['class'][0] == 'quarter'):
                    children = text.findChildren()
                    for x in children:
                        if(x.name == 'p'):
                            ##print("INSTRUCTORS: ",x.get_text().strip())
                            quarters = x.get_text().strip().split(',')
                            for y in quarters:
                                cur_course.add_quarter(y.strip())
                # if(text.attrs['class'][0] == 'extraFields'):
                #     children = text.findChildren()
                #     for x in children:
                #         if(x.name == 'p'):
                #             if(x.get_text().strip() == "Yes"):
                #                 ##print("REPEATABLE")
                #                 cur_course.set_repeatable(True)
                #             elif(x.get_text().strip().__contains__("Prerequisite")):
                #                 #print("PREREQ: ",x.get_text().strip())
                #                 txt = x.get_text().strip()
                #                 txt = txt[:-1]
                #                 txt = txt.strip("Prerequisite(s): ")
                #                 split_1 = txt.split("; or ")
                #                 for y in split_1:
                #                     #print("Y IN SPLIT ONE")
                #                     new_list = []
                #                     split_prereq(y, new_list, cur_course, new_list)
                #                     #break_flag = True

                if(text.attrs['class'][0] == 'genEd'):
                    children = text.findChildren()
                    for x in children:
                        if(x.name == 'p'):
                            ##print("INSTRUCTORS: ",x.get_text().strip())
                            ge = x.get_text().strip().split(',')
                            for y in ge:
                                cur_course.add_ge(y.strip())
                ##print("PART: "+text.get_text())
            # credits = course_soup.find_all('div', class_ = "credits")
            # #print("CREDITS IS: ", credits[0].get_text())
            # instructors = course_soup.find_all('div', class_="instructor")
            # instructors = instructors[0].get_text().split(',')
            # quarters = course_soup.find_all('div', class_="quarter")
            # if(len(quarters)>0):
            #     quarters = quarters[0].get_text().split(',')
            # #ELSE NO QUARTER SECTION AVAILABLE
            # extraFields = course_soup.find_all('div', class_="extraFields")
            # if(len(extraFields)>0):
            #     #print("EXTRA FEILDS: "+extraFields[0].get_text())
            if break_flag:
                break
    for data in html_soup.find_all('ul', class_="sc-child-item-links"): 
        ##print("DATA: "+data.get_text()) 
        for course_link in data.find_all('a', href = True):
            ##print("LINK: "+ course_link['href'])
            link = course_link['href']
            ##print(link.index('/', 1))
            link = link[link.index('/', 1):]
            ##print("LINK NO EN: ",link)
            ##print("SHOULD BE CURRENT: ",link[1:link.index('/',1)])
            url_to_scrape = url_to_scrape[0:url_to_scrape.index(link[1:link.index('/',1)])-1]
            url_to_scrape += link
            ##print("URL TO SCRAPE: "+url_to_scrape)
            course_page = urlopen(url_to_scrape)
            course_html = course_page.read()
            course_page.close()
            course_soup = BeautifulSoup(course_html, 'html.parser')
                # for course in course_soup.find_all('div', class_="combinedChild"): 
                #     #print("COMBINED CHILD: ",course.get_text())
            text = course_soup.find_all('h2', class_ = "course-name")
            if len(text) == 0:
                break
            text = text[0]
            #print("COURSE NAME: "+text.get_text().strip())


            # course_name = text.get_text().strip()
            # cur_course = Course(course_name)
            # course_split = course_name.split(" ")
            # name = course_split[0]+" "+course_split[1]
            # course_list[name] = cur_course



            first = True

            #course_list.append(cur_course)
            while True:
            #CHECK TO SEE IF THERE IS A NEXT SIBLING, IF NOT BREAK
                if first:
                    first = False
                else:
                    text = text.next_sibling
            #REMOVE ALL WHITESPACE
                if text is None:
                ##print("TEXT IS NONTYPE")
                    break
                no_white = ''.join(text.get_text().split())
                if(len(no_white) == 0):
                ##print("NOTHING HERE")
                    continue
            ##print("ATTRIBUTE: ",text.attrs['class'][0])
                if(text.attrs['class'][0] == 'course-name'):
                ##print("COURSE NAME: "+text.get_text())
                #cur_course.#print_course()
                    if break_flag:
                        break
                    course_name = text.get_text().strip()
                    #cur_course = Course(course_name)
                    course_split = course_name.split(" ")
                    name = course_split[0]+" "+course_split[1]
                    print("COURSE: ", name)
                    cur_course = course_list[name]
                    #print('CUR COURSE: ', name)
                    #cur_course.#print_course()
                # if(text.attrs['class'][0] == 'desc'):
                #     ##print("DESCRIPTION: "+text.get_text())
                #     cur_course.set_desc(text.get_text().strip())
                # if(text.attrs['class'][0] == 'sc-credithours'):
                #     ##print("CREDIT HOURS: ", text.get_text())
                #     children = text.findChildren()
                #     for x in children:
                #         if(x.name == 'div'):
                #             ##print("CREDITS: ",x.get_text().strip())
                #             cur_course.set_credits(int(x.get_text().strip()))
                # if(text.attrs['class'][0] == 'instructor'):
                #     children = text.findChildren()
                #     for x in children:
                #         if(x.name == 'p'):
                #             ##print("INSTRUCTORS: ",x.get_text().strip())
                #             instructors = x.get_text().strip().split(',')
                #             for y in instructors:
                #                 cur_course.add_instructor(y.strip())
                # if(text.attrs['class'][0] == 'quarter'):
                #     children = text.findChildren()
                #     for x in children:
                #         if(x.name == 'p'):
                #             ##print("INSTRUCTORS: ",x.get_text().strip())
                #             quarters = x.get_text().strip().split(',')
                #             for y in quarters:
                #                 cur_course.add_quarter(y.strip())
                if(text.attrs['class'][0] == 'extraFields'):
                    children = text.findChildren()
                    for x in children:
                        if(x.get_text().strip() == "Requirements"):
                            y = x.find_next_sibling("p")
                            #print("Y: ",y)
                            #print("COURSE NAME: ",cur_course.name+"\n\n")
                            txt = y.get_text().strip()
                            txt = txt.strip("Prerequisite(s): ")
                            txt = txt.replace("  ", " ")
                            txt = txt.replace("either ", "")
                            txt = txt[:-1]
                            txt_split = txt.split(".")
                            for f in txt_split:
                                new_list = []
                                restrict_set = set()
                                req_list = split_prereq(f, new_list, cur_course, new_list, course_list, restrict_set)
                                cur_course.prereqs.append(req_list)
                                for l in restrict_set:
                                    cur_course.restricted.add(l)
                                #print("APPEND PREREQS: ", req_list)
                        elif(x.name == 'p'):
                            if(x.get_text().strip() == "Yes"):
                                ##print("REPEATABLE")
                                cur_course.set_repeatable(True)
                            
                            # elif(x.get_text().strip().__contains__("Prerequisite")):
                            #     #print("PREREQ: ",x.get_text().strip())
                            #     txt = x.get_text().strip()
                            #     txt = txt.strip("Prerequisite(s): ")
                            #     txt = txt.replace("  ", " ")
                            #     txt = txt.replace("either ", "")
                            #     txt = txt[:-1]
                            #     txt_split = txt.split(".")
                            #     for f in txt_split:
                            #         new_list = []
                            #         restrict_set = set()
                            #         req_list = split_prereq(f, new_list, cur_course, new_list, course_list, restrict_set)
                            #         cur_course.prereqs.append(req_list)
                            #         for l in restrict_set:
                            #             cur_course.restricted.add(l)
                            #         #print("APPEND PREREQS: ", req_list)



                                # txt = x.get_text().strip()
                                # txt = txt[:-1]
                                # txt = txt.strip("Prerequisite(s): ")
                                # split_1 = txt.split("; or ")
                                # for y in split_1:
                                #     #print("Y IN SPLIT ONE")
                                #     new_list = []
                                #     split_prereq(y, new_list, cur_course, new_list)
                                    #break_flag = True

                # if(text.attrs['class'][0] == 'genEd'):
                #     children = text.findChildren()
                #     for x in children:
                #         if(x.name == 'p'):
                #             ##print("INSTRUCTORS: ",x.get_text().strip())
                #             ge = x.get_text().strip().split(',')
                #             for y in ge:
                #                 cur_course.add_ge(y.strip())
                ##print("PART: "+text.get_text())
            # credits = course_soup.find_all('div', class_ = "credits")
            # #print("CREDITS IS: ", credits[0].get_text())
            # instructors = course_soup.find_all('div', class_="instructor")
            # instructors = instructors[0].get_text().split(',')
            # quarters = course_soup.find_all('div', class_="quarter")
            # if(len(quarters)>0):
            #     quarters = quarters[0].get_text().split(',')
            # #ELSE NO QUARTER SECTION AVAILABLE
            # extraFields = course_soup.find_all('div', class_="extraFields")
            # if(len(extraFields)>0):
            #     #print("EXTRA FEILDS: "+extraFields[0].get_text())
            if break_flag:
                break
    return course_list
    

def scrape_course(url_to_scrape):
    course_list = {}
    course_page = urlopen(url_to_scrape)
    course_html = course_page.read()
    course_page.close()
    course_soup = BeautifulSoup(course_html, 'html.parser')
                # for course in course_soup.find_all('div', class_="combinedChild"): 
                #     #print("COMBINED CHILD: ",course.get_text())
    text = course_soup.find_all('h2', class_ = "course-name")
    text = text[0]
    #print("COURSE NAME: "+text.get_text().strip())
    course_name = text.get_text().strip()
    cur_course = Course(course_name)
    course_split = course_name.split(" ")
    name = course_split[0]+" "+course_split[1]
    course_list[name] = cur_course
    #course_list.append(cur_course)
    while True:
    #CHECK TO SEE IF THERE IS A NEXT SIBLING, IF NOT BREAK
        text = text.next_sibling
    #REMOVE ALL WHITESPACE
        if text is None:
        ##print("TEXT IS NONTYPE")
            break
        no_white = ''.join(text.get_text().split())
        if(len(no_white) == 0):
        ##print("NOTHING HERE")
            continue
    ##print("ATTRIBUTE: ",text.attrs['class'][0])
        if(text.attrs['class'][0] == 'course-name'):
        ##print("COURSE NAME: "+text.get_text())
        #cur_course.#print_course()
            course_name = text.get_text().strip()
            cur_course = Course(course_name)
            course_split = course_name.split(" ")
            name = course_split[0]+" "+course_split[1]
            course_list[name] = cur_course
        if(text.attrs['class'][0] == 'desc'):
            ##print("DESCRIPTION: "+text.get_text())
            cur_course.set_desc(text.get_text().strip())
                
        if(text.attrs['class'][0] == 'sc-credithours'):
            ##print("CREDIT HOURS: ", text.get_text())
            children = text.findChildren()
            for x in children:
                if(x.name == 'div'):
                    ##print("CREDITS: ",x.get_text().strip())
                    cur_course.set_credits(int(x.get_text().strip()))
        if(text.attrs['class'][0] == 'instructor'):
            children = text.findChildren()
            for x in children:
                if(x.name == 'p'):
                            ##print("INSTRUCTORS: ",x.get_text().strip())
                    instructors = x.get_text().strip().split(',')
                    for y in instructors:
                        cur_course.add_instructor(y.strip())
        if(text.attrs['class'][0] == 'quarter'):
            children = text.findChildren()
            for x in children:
                if(x.name == 'p'):
                    ##print("INSTRUCTORS: ",x.get_text().strip())
                    quarters = x.get_text().strip().split(',')
                    for y in quarters:
                        cur_course.add_quarter(y.strip())
        if(text.attrs['class'][0] == 'extraFields'):
            children = text.findChildren()
            for x in children:
                if(x.get_text().strip() == "Requirements"):
                    y = x.find_next_sibling("p")
                    #print("Y: ",y)
                    # print("COURSE NAME: ",cur_course.name+"\n\n")
                    txt = y.get_text().strip()
                    txt = txt.strip("Prerequisite(s): ")
                    txt = txt.replace("  ", " ")
                    txt = txt.replace("either ", "")
                    txt = txt[:-1]
                    txt_split = txt.split(".")
                    for f in txt_split:
                        new_list = []
                        restrict_set = set()
                        req_list = split_prereq(f, new_list, cur_course, new_list, course_list, restrict_set)
                        cur_course.prereqs.append(req_list)
                        for l in restrict_set:
                            cur_course.restricted.add(l)
                        #print("APPEND PREREQS: ", req_list)
                    # txt = txt.strip("Prerequisite(s): ")
                    # txt = txt[:-1]
                    # new_list = []
                    # restrict_set = set()
                    # req_list = split_prereq(txt, new_list, cur_course, new_list, course_list, restrict_set)
                    # cur_course.prereqs.append(req_list)
                elif(x.name == 'p'):
                    if(x.get_text().strip() == "Yes"):
                        ##print("REPEATABLE")
                        cur_course.set_repeatable(True)
                    # elif(x.get_text().strip().__contains__("Prerequisite")):
                    #     ##print("PREREQ: ",x.get_text().strip())
                    #     #print("COURSE NAME: ",cur_course.name+"\n\n")
                    #     txt = x.get_text().strip()
                    #     txt = txt.strip("Prerequisite(s): ")
                    #     txt = txt[:-1]
                    #     new_list = []
                    #     restrict_set = set()
                    #     req_list = split_prereq(txt, new_list, cur_course, new_list, course_list, restrict_set)
                    #     cur_course.prereqs.append(req_list)
                    #     #cur_course.restricted = restrict_set
                    #     # split_1 = txt.split("; or ")
                    #     # for y in split_1:
                    #     #     ##print("Y IN SPLIT ONE")
                    #     #     new_list = []
                    #     #     split_prereq(y, new_list, cur_course)
                    #     #     #break_flag = True

        if(text.attrs['class'][0] == 'genEd'):
            children = text.findChildren()
            for x in children:
                if(x.name == 'p'):
                            ##print("INSTRUCTORS: ",x.get_text().strip())
                    ge = x.get_text().strip().split(',')
                    for y in ge:
                        cur_course.add_ge(y.strip())
    
    return course_list
    

def returnCourseList():
    course_list = {}
    print("SCRAPING COURSES")
    course_list = scrape_courses()
    i = 0
    for x in course_list:
        if(course_list[x].name.__contains__("LALS 1 ")):
            course_list[x].print_course()
            print("\n")
    # for x in course_list:
    #     if len(course_list[x].desc) >= 1000:
    #         #print("MORE THAN 1000")
    #         #print(course_list[x].name)
    return course_list



returnCourseList()


#course_list = scrape_course('https://catalog.ucsc.edu/Current/General-Catalog/Courses/AM-Applied-Mathematics')
# #course_list = scrape_course('https://catalog.ucsc.edu/Current/General-Catalog/Courses/STAT-Statistics')
# i = 0
# for x in course_list:
#     if(len(course_list[x].ge) > 1):
#         #print(course_list[x].ge)
        
    
# #print("done")

# for x in prereq_not_counted:
#     if "examination" in x:
#             #print("NOT COUNTED: ", x)


##print("NOT COUNTED LEN: ", len(prereq_not_counted))
#course_list["MATH 103A"].#print_course()


# course_list.pop("AM 170B")
# #print("\n\n\n\n\n\n")
# cur_course = Course("AM 170B")
# course_list["AM 170B"] = cur_course
# #new_list = []
# txt ="satisfaction of the Entry Level Writing and Composition requirements; and TIM 50 or permission of instructor"
# txt_split = txt.split(".")
# for f in txt_split:
#     new_list = []
#     #print("\n\nSPLIT PREREQ: ", f)
#     req_list = split_prereq(f, new_list, cur_course, new_list, course_list)
#     cur_course.prereqs.append(req_list)

# cur_course.#print_course()


#a = split_prereq(txt, new_list, cur_course, new_list, course_list)
#cur_course.add_prereq(a)
#cur_course.#print_course()

# split_prereq("Enrollment is restricted to juniors and seniors", new_list, cur_course, req_list, course_list)


# course_list["Course"].#print_course()
#Prerequisites:  'Repeatable for credit\r\n\t\tYes'

#majors = scrape_majors(course_list)

##print("DONE")

#test = Student("Alex")
#keys = list(majors.keys())
##print("KEYS: ", keys)
#test.add_major(majors[keys[0]].name)

##print("MAJOR: ", majors[keys[0]].name)

#can_take = []

#for x in test.majors:
#    #print("MAJOR 2: ", x)
#    for y in majors[x].classes:
#        #print("CLASS: ",y)
#    for y in majors[x].classes:
#        allowed = test.can_take_class(course_list[y].prereqs, 1)
#        #print("CAN TAKE ",y,": ", allowed)
#        if(allowed):
#            can_take.append(y)
#can_take.sort()
#for x in can_take:
#    #print("ALLOWED: ", x)

#PREREQ SPLIT: 
#DEFINTE SPLIT ON "AND" "." ";"


#SPLIT ON 'OR' UNLESS ITS 'OR HIGHER'
# def find_req(req_l, req):
#     for x in req:
#         if type(x) == list:
#             find_req(req_l, x)
#         else:
#             req_l.add(x)
        
#for x in course_list:
#    for y in course_list[x].prereqs:
#        req_l = set()
#        find_req(req_l, y)
#        for z in req_l:
#            if z not in course_list:
#                #print("NOT A COURSE: ", z)
# for x in exam_list:
#     #print("EXAM: ", x)