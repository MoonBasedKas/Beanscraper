"test"
import requests
from bs4 import BeautifulSoup

"""
Holds all the data for a single course.
"""
class course:

    def __init__(self, data):
        self.crn = data[0]
        self.Cnumber = data[1]
        self.campus = data[2]
        self.day = data[3]
        self.length = data[4]
        self.time = data[5]
        self.room = data[6]
        self.hrs = data[7]
        self.type = data[8]
        self.name = data[9]
        self.teacher = data[10]
        self.seats = data[11]
        self.limits = data[12]
        self.enroll = data[13]
        self.waitlist = data[14]
        self.fee = data[15]
        self.book = data[16]

"""
Handles all of the courses for a single subject.
"""
class subject:

    def __init__(self, term, sub):

        # url = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+"202420"+"&p_subj="+"SPAN"
        url = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+term+"&p_subj="+sub
	    # print(sub)
        self.courses = []

        # print(sub, term)

        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        classdata = soup.find_all("td")

        courses = []

        string = ""

        data = []

        while len(classdata) > 17:
            string = classdata[0].string
            data = []
            for x in range(17):
                string = classdata[0].string
                if string == "None":
                    string = " "
                data.append(string)
                classdata.pop(0)
            print(data[0:3], "===============", classdata[0].string, string)
            courses.append(data)
            if string == "Bookstore Link":
                classdata.pop(0)



            # for x in range(17):
            #     data.append(cleantext[0])
            #     cleantext.pop(0)
            # print(data[0])
            # self.courses.append(course(data))


        # text = soup.get_text().split("\n")
        # # print(text)

        # cleantext = text

        # # print(cleantext)

        # while cleantext[0] != "Bookstore Link":
        #     print("\""+cleantext[0]+"\"")
        #     if cleantext [0] == "No courses found matching your term and subject":
        #         return None
        #     cleantext.pop(0)


        # data = []
        # print(cleantext)
        # # print(sub)
        # while cleantext[0] != "*Campus":
        #     data = []
        #     for x in range(17):
        #         data.append(cleantext[0])
        #         cleantext.pop(0)
        #     print(data[0])
        #     self.courses.append(course(data))



class SubjectList:
    def __init__(self, date, tags):
        self.subjects = []

        courses = 0

        for tag in tags:
            self.subjects.append(subject(date, tag))

def main():
  
    url = "https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
    
    url1 = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+"202420"+"&p_subj="+"SPAN"
		

    soup = BeautifulSoup(requests.get(url).content, "html.parser")



    z = soup.find_all("option")
    dates = []
    subjects = []

    tag = []

    for elem in z:
        tag = elem.get("value")
        if tag.isnumeric():
            dates.append(tag)
        else:
            subjects.append(tag)
    # print(subjects)

    # subject(dates[-1], "BIOL")
    SubjectList(dates[-1],subjects)

    


if __name__ == "__main__":
    main()