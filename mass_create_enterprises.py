####################################################
'''
VSD Performance Checker 
Mass Enterprise Creation with VSDK API
@author Muzaffer Kahraman 2022
'''
####################################################

#!/usr/bin/env python3
from property_parser import Credentials
from vspk import v5_0 as vsdk
from datetime import date
import logging

class Enterprise:

    def __init__(self,name):
        self.org = vsdk.NUEnterprise(name=name)
       
    def create(self):
        nc.user.create_child(self.org)
                
if __name__=="__main__":
    
    today = date.today()
    logfile = "/var/log/{}_vsd_performance_checker.log".format(str(today))
    logging.basicConfig(filename=logfile,level=logging.INFO,format='%(asctime)s %(levelname)s  %(message)s')
    logging.info("Enterprise Creation Started")

    # Let's parse the config file using the credentials class
    creds=Credentials("credential.properties")
  
    nc = vsdk.NUVSDSession(username=creds.get_user(), password=creds.get_passwd(), enterprise=creds.get_org(), api_url=creds.get_url())
    nc.start()
    
    for i in range (0,10):
        enterprise_name="TestEnterprise_"+str(i)
        ent=Enterprise(enterprise_name)
        ent.create()
        logging.info(enterprise_name+" created")
    
    logging.info("Enterprise Creation Ended")