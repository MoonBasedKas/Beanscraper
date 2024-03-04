"""
Prototype for NeoBean Scrapper
"""
import requests
from bs4 import BeautifulSoup
# import inspect

"""
Holds all the data for a single course.
"""
class LectureSession:

    def __init__(self, info):
        self.day = ""
        self.location = ""
        self.start = ""
        self.end = ""
        pass



class Course:

    def __init__(self, data):
        self.dlist = data # Raw data.

        self.crn = str(data[0])
        self.Cnumber = str(data[1])
        self.campus = str(data[2])
        self.day = str(data[3]).replace(" ", "")
        self.length = str(data[4])
        self.time = str(data[5])
        self.room = str(data[6])
        self.hrs = str(data[7])
        self.type = str(data[8])
        self.name = str(data[9])
        self.teacher = str(data[10])
        self.seats = str(data[11])
        self.limits = str(data[12])
        self.enroll = str(data[13])
        self.waitlist = str(data[14])
        self.fee = str(data[15])
        self.book = str(data[16])
        # TODO add the section as part of cleaning.
    """
    Gives a list of all the attributes since inputing them all one by one is PAIN.
    """
    def attributeList(self):
            list = []
            list.append(self.crn)
            list.append(self.Cnumber)
            list.append(self.campus) 
            list.append(self.day )
            list.append(self.length)
            list.append(self.time)
            list.append(self.room)
            list.append(self.hrs )
            list.append(self.type)
            list.append(self.name)
            list.append(self.teacher)
            list.append(self.seats )
            list.append(self.limits)
            list.append(self.enroll )
            list.append(self.waitlist)
            list.append(self.fee )
            list.append(self.book) 


"""
Handles all of the courses for a single subject.
"""
class Subject:

    def __init__(self, term, sub):

        url = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+term+"&p_subj="+sub

        self.courses = []
        self.subject = sub


        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        classdata = soup.find_all("td")

        string = ""

        data = []

        while len(classdata) > 17:
            string = classdata[0].string
            data = []
            for x in range(17):
                string = classdata[0].string
                if string == "None":
                    string = "N/A"
                data.append(string)
                classdata.pop(0)
            # print(data[0:3], "===============", classdata[0].string, string)
            self.courses.append(Course(data))
            if string == "Bookstore Link":
                classdata.pop(0)
            
            # cleanSubject()

    """
    Cleans up classes without a crn.
    """
    def cleanSubject(self):
        i = 0
        l = len(self.courses)
        temp = None

        while i < l:
            temp = self.courses[i]
            if temp.crn == "None":
                if temp.campus == "None": # Two professors
                    # print(temp.dlist[9])
                    self.courses[i - 1].teacher += " " + str(temp.dlist[9])
                    # print(self.courses[i - 1].teacher)
                    self.courses.pop(i)
                    i -= 1
                    l -= 1
                else: # Recitations
                    pass
                
            i += 1



"""
Handles all subjects. Current main should be in here.
"""
class Scrapper:
    url = "https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
    subjects = []
    date = ""
    subs = []

    def __init__(self):

        soup = BeautifulSoup(requests.get(self.url).content, "html.parser")


        z = soup.find_all("option")
        dates = []
        self.subs = []

        tag = []

        for elem in z:
            tag = elem.get("value")
            if tag.isnumeric():
                dates.append(tag)
            else:
                self.subs.append(tag)

        temp = None

        self.date = str(dates[-1])
        print(self.date)
        print(self.subjects)

        for tag in self.subs:
            temp = Subject(self.date, str(tag))
            temp.cleanSubject()
            print(tag)
            self.subjects.append(temp)

        # print(self.subjects)

        
    """ 
    TODO: Have it run through each one.
    """
    def cleanSubjects(self):
        pass
    
    """
    Writes to a CVS all subjects. I think I just broke this function.
    TODO Change it to work with the actual values rather than the raw data list.
    """
    def writeCVS(self):
        string = ""
        fp = open("datacheck.csv", "w")
        for subject in self.subjects:
            
            for course in subject.courses:
                string = ""
                
                for val in course.dlist:
                    string = string + str(val) + ","
                print(string)
                string = string[0:-1] + "\n"

                fp.write(string)
        fp.close()
        pass

def main():
  
    # url = "https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
    
    # # url1 = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+"202420"+"&p_subj="+"SPAN"
		

    # soup = BeautifulSoup(requests.get(url).content, "html.parser")



    # z = soup.find_all("option")
    # dates = []
    # subjects = []

    # tag = []

    # for elem in z:
    #     tag = elem.get("value")
    #     if tag.isnumeric():
    #         dates.append(tag)
    #     else:
    #         subjects.append(tag)

    data = Scrapper()


    # data.writeCVS() 

    


if __name__ == "__main__":
    main()