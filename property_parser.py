class Credentials:

    def __init__(self,filename):
          
        f = open(filename,"r")
        A=f.readlines()
        self.url=A[0].partition("=")[2].replace('\n', '')
        self.user=A[1].partition("=")[2].replace('\n', '')
        self.passwd=A[2].partition("=")[2].replace('\n', '')
        self.org=A[3].partition("=")[2].replace('\n', '')
        f.close()
            
    def get_url(self):
        return self.url

    def get_user(self):
        return self.user
 
    def get_passwd(self):
        return self.passwd

    def get_org(self):
        return self.org