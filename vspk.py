#!/usr/bin/python3

# *********************************************************************************
#
# Nuage VSD Provisioning PoC
#
# Required  : [Python requests,json, base64, urllib3]
#
# @author Muzaffer Kahraman (Muzo)
#
# *********************************************************************************

#!/usr/bin/env python

from vspk import v5_0 as vsdk
import json
import base64
import sys
 
class LabDeploy:

    def __init__(self):

        # Read the creds.json file and assign the variables accordingly
        f=open('creds.json','r')
        creds=json.load(f)
        self.userName=creds["csp_username"]
        self.passWord=creds["csp_password"]
        self.url=creds["url"]
        f.close()
        self.nc=vsdk.NUVSDSession(username=self.userName, password=self.passWord, enterprise='csp', api_url=self.url) 
        self.nc.start()

  

    def listEnterprises(self):  
        
        enterprises=self.nc.user.enterprises.get()
        for ent in enterprises:
            print(ent.name)


    def listDCgatewayTemplates(self):
    
        dcgwtemps=self.nc.user.gateway_templates.get()
        for ent in dcgwtemps:
            print(ent.name)

    def findDCgatewayTemplate(self,name):
    
        DCgatewayTemplate=self.nc.user.gateway_templates.get_first(filter='name=="%s"'%(name))
        temp_id=DCgatewayTemplate.id
        return(temp_id)


    def findEnterprise(self,name):
   
        enterprise=self.nc.user.enterprises.get_first(filter='name=="%s"'%(name))
        ent_id=enterprise.id
        return(ent_id)
    

    


    def createWBX(self,name,temp_id,ports,lags):

        gateway=vsdk.NUGateway()
        gateway.name=name
        gateway.system_id=10010001
        gateway.template_id=temp_id
        gateway.personality="NUAGE_210_WBX_48_S"
        self.nc.user.create_child(gateway)

        gw=self.nc.user.gateways.get_first(filter='name=="%s"'%(name))
        print(gw.id)

        for index in range (0,ports):
            port=vsdk.NUPort()
            port.name="1/1/"+str(index+1)
            port.physical_name="1/1/"+str(index+1)
            port.port_type="ACCESS"
            port.vlan_range="0-4095"
            gw.create_child(port)

        for index in range (0,lags):
            port=vsdk.NUPort()
            port.name="lag-"+str(index+1)
            port.physical_name="lag-"+str(index+1)
            port.port_type="ACCESS"
            port.vlan_range="0-4095"
            gw.create_child(port)

        



    def createWBXtemplate(self,name):

        gatewayT=vsdk.NUGatewayTemplate()
        gatewayT.name=name
        gatewayT.personality="NUAGE_210_WBX_48_S"
        self.nc.user.create_child(gatewayT)

        gwt=self.nc.user.gateway_templates.get_first(filter='name=="%s"'%(name))
        print(gwt.id)
        
        port=vsdk.NUPort()
        port.name="1/1/1"
        port.physical_name="1/1/1"
        port.port_type="ACCESS"
        gwt.create_child(port) # you cannot add ports to gateway temolate w api      
        


if __name__=="__main__":

  instance=LabDeploy()
  # instance.listDCgatewayTemplates()
  temp_id=instance.findDCgatewayTemplate("muzo")
  instance.createWBX("AAAAAA",temp_id,24,8)
  # print(instance.findEnterprise(sys.argv[1]))
  # instance.listWBXs("NCR_MAN")
  # instance.createWBXtemplate("full")

