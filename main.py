"test"
import requests
from bs4 import BeautifulSoup

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


class subject:

    def __init__(self, term, sub):

        # url1 = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+"202420"+"&p_subj="+"SPAN"
        url1 = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+term+"&p_subj="+sub
		

        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        content = soup.get_text().split("\n")
        # print(content)
        cleancontent = []
        for x in content:
            if x != content[0]:
                cleancontent.append(x)

        for x in range(19):
            cleancontent.pop(0)
            cleancontent.pop(-1)
        cleancontent.pop(0)
        data = cleancontent # I don't want to bother overwriting cleancontent as data rn.
        print(cleancontent)
        # courses(cleancontent)

        cdata = []
        self.courselist = []

        while data != []:
            cdata = []
            for x in range(17):
                cdata.append(data[0])
                data.pop(0)
            self.courselist.append(course(cdata))


class SubjectList:
    def __init__():
        pass

def main():
  
    url = "https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
    
    url1 = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term="+"202420"+"&p_subj="+"SPAN"
		

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    content = soup.get_text().split("\n")
    # print(content)
    cleancontent = []
    for x in content:
        if x != content[0]:
            cleancontent.append(x)
    print(soup.select) # Course tags.
    # print(soup.tr)     # Semesters.

    


if __name__ == "__main__":
    main()