"""
Prototype for NeoBean Scrapper
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

"""
Holds all the data for a single course.
"""
class LectureSession:

    def __init__(self, info):
        self.day = info[0]
        self.location = info[1]
        self.start = info[2]
        self.end = info[3]
        pass

    def jsonify(self):
        data = {}
        data["Day"] = self.day
        data["Location"] = self.location
        data["StartTime"] = self.start
        data["EndTime"] = self.end
        return data



class Course:

   

    # Adds everything 
    def __init__(self, data, subject):
        self.dlist = data                           # Raw data.
        self.Sessions = []

        self.subject = subject
        self.crn = str(data[0])
        self.Cnumber = str(data[1])
        self.campus = str(data[2])
        self.day = str(data[3]).replace(" ", "")    # Merges into Sessions
        self.length = str(data[4])                  # Merges into Sessions
        self.time = str(data[5])                    # Merges into Sessions
        self.room = str(data[6])                    # Merges into Sessions
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
        now = datetime.now()

        self.lastUpdated = now.strftime("%D:%H:%M:%S")
        self.buildSessions()


    def buildSessions(self):
        times = self.time.split("-")
        if len(times) != 2:
            return -1
        
        info = ["", self.room, times[0], times[1]]
        for x in self.day:
            info[0] = x 
            self.Sessions.append(LectureSession(info))
        return 0


    """
    Adds additional attached sessions.
    """
    def addSessions(self, info):
        times = info[-1].split("-")
        info[2] = times[0]
        info.append(times[1])
        self.Sessions.append(LectureSession(info))


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
    Final step in cleaning process. Does any type conversions as N/A's cause problems on this.
    """
    def dataPrep(self):
        self.section = self.Cnumber.split("-")[1] # Can't be a integer due to section numbers containing letters.
        self.seats = int(self.waitlist)
        self.limits = int(self.waitlist)
        self.enroll = int(self.waitlist)
        self.waitlist = int(self.waitlist)
        self.hrs = int(self.hrs)
        self.Cnumber = self.Cnumber.split(" ")[1].split("-")[0] # Can't be integer due to labs.

        if self.fee != "N/A":
            self.fee = float(self.fee[1:])
        else:
            self.fee = 0.0


    """
    Returns a dictionary that can easily be exported.
    """
    def jsonify(self):
        jdict = {}
        jdict["Title"] = self.name
        jdict["Subject"] = self.subject
        jdict["CourseNumber"] = self.Cnumber
        jdict["CRN"] = self.crn
        jdict["Section"] = self.section

        jdict["Campus"] = self.campus
        jdict["CreditHours"] = self.hrs
        # jdict["classType"] = self.type
        jdict["Professor"] = self.teacher

        jdict["Seats"] = self.seats
        jdict["SeatCapacity"] = self.limits
        jdict["Enrolled"] = self.enroll
        jdict["Waitlist"] = self.waitlist
        jdict["CourseFee"] = self.fee

        jdict["BookStore"] = self.book



        meetings = []
        for meet in self.Sessions:
            meetings.append(meet.jsonify())

        jdict["Sessions"] = meetings
        jdict["LastUpdated"] = self.lastUpdated

        return jdict



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

            self.courses.append(Course(data, sub))
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
        info = []

        while i < l:
            temp = self.courses[i]
            if temp.crn == "None":
                if temp.campus == "None": # Two professors

                    self.courses[i - 1].teacher += " " + str(temp.dlist[9])

                else: # Recitations
                    info.append(temp.dlist[2])
                    info.append(temp.dlist[5])
                    info.append(temp.dlist[4])
                    info = []
                self.courses.pop(i)
                i -= 1
                l -= 1
                
            i += 1
        

        for C in self.courses:
            C.dataPrep()



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

        for tag in self.subs:
            temp = Subject(self.date, str(tag))
            temp.cleanSubject()
            self.subjects.append(temp)



        
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

                string = string[0:-1] + "\n"

                fp.write(string)
        fp.close()
    

    def writeJson(self):
        jsonData = {}

        for sub in self.subjects:
            for course in sub.courses:
                jsonData[course.crn] = course.jsonify()

        json_object = json.dumps(jsonData, indent=4)
        

        with open("CourseList.json", "w") as outfile:
            outfile.write(json_object)


        

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

    Scrapper.subjects[0].courses[0].jsonify()


    data.writeJson() 

    


if __name__ == "__main__":
    main()