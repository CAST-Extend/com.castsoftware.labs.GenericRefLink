import cast_upgrade_1_5_11 # @UnusedImport
from cast.application import ApplicationLevelExtension,create_link,  ReferenceFinder
import logging
import cast.application
import xml.etree.ElementTree as ET
import sys, os

class GenRefLinkExtensionApplication(cast.application.ApplicationLevelExtension):

    def __init__(self): 
       
        
        pass     
    
       
        
        
    def end_application(self, application):
        logging.info("GenericRefLink : Running extension code at the end of an application")
        
     
        # list all files saved 
        try:
            
            #fpath="C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.labs.GenRefLink.1.0.0\Generic.xml"
            fpath=self.Castpath.get_drive()+ "ProgramData\CAST\CAST\Extensions\com.castsoftware.labs.GenericRefLink.1.1.0\Generic.xml"
            logging.info(str(fpath))
             
            if (os.path.isfile(fpath)):
                    tree = ET.parse(fpath, ET.XMLParser(encoding="UTF-8"))
                    root=tree.getroot()
                    cnt=0
                   
                    for group in root.findall('Search'):
                        sbefore = group.find('RegexPatternBefore').text
                        safter = group.find('RegexPatternAfter').text
                        sregex = group.find('RegexPattern').text
                        sfileext = group.find('RefFileExtension').text
                        sfilecategory = group.find('RefFileCastCatergory').text
                        nb_links = 0 
                        links = [] 
                        files=[]
                        rf = ReferenceFinder()
                        cnt = cnt+1
                        
                        if sbefore is None:
                         sbefore=""
                        if  safter is None:
                         safter =""
                        if sfileext is not None:
                           sfileext=sfileext.replace(".", "")
                        logging.debug(str(sbefore)+"---"+str(sregex)+ "---"+str(safter))
                        rf.add_pattern('Search'+sfileext +str(cnt), before=sbefore, element = sregex, after=safter)
                       
                                       
                        # list all files saved 
                        try:
                            
                            fileCount = sum(1 for x in application.get_files([sfilecategory]))
                            files = application.get_files([sfilecategory])
                            self.findpattern(application, files, group, links,rf)
                      
                        except Exception as e:
                            logging.error(": Error getting source  file set : %s", str(e))
                           
                                                  
                        # 3. Create the links
                        for link in links:
                            logging.info("Creating link between " + str(link[1]) + " and " + str(link[2]))
                            create_link(*link)
                            nb_links = nb_links + 1 
                        links=[]        
                        logging.info("Nb of links created " + str(nb_links)) 
                        
        except Exception as e:
            logging.error(": Error Generic ref link extension  set : %s", str(e))
                
    def findpattern(self, application, files, group, links, rf):
         #looping through Files
                       
                        for o in files:
                            greferences = []
                            extfile = group.find('RefFileExtension').text
                            
                            if o.get_name().find(extfile) is not -1:
                                #   check if file is analyzed source code, or if it generated (Unknown)
                               
                                logging.debug("GenericRefLink :" + extfile )                             
                                #   check if file is a program , skip the headers
                               
                                greferences += [reference for reference in rf.find_references_in_file(o)]
                                for ref in greferences:
                                    sobjcat = group.find('TargetObjectCategory').text
                                    sobjname = group.find('TargetObjectname').text 
                                    if sobjname is None:
                                            logging.debug("GenericRefLink :" + extfile +  "application")
                                            for callpgm in application.search_objects(category=sobjcat,  load_properties=False):
                                                    strreforg = str(ref.value)
                                                    strjvclsorg = callpgm.get_name()
                                                    if strreforg.find(strjvclsorg) is not -1:
                                                        slinktyp = group.find('LinkType').text
                                                        sorgin = group.find('LinkOrginRef').text
                                                        if sorgin.lower() == 'true':
                                                         links.append((slinktyp, ref.object, callpgm, ref.bookmark))
                                                        else:
                                                         links.append((slinktyp, callpgm,  ref.object,  ref.bookmark))
                                                    else:
                                                        Notfound = False
                                    else:
                                               
                                            for javaclass in application.search_objects(category=sobjcat, name =sobjname, load_properties=False):
                                                strreforg = str(ref.value)
                                                strjvclsorg = javaclass.get_fullname()
                                                if strreforg.find(strjvclsorg) is not -1:
                                                    slinktyp = group.find('LinkType').text
                                                    sorgin = group.find('LinkOrginRef').text
                                                    if sorgin.lower() == 'true':
                                                     links.append((slinktyp, ref.object, javaclass, ref.bookmark))
                                                    else:
                                                     links.append((slinktyp, javaclass, ref.object,  ref.bookmark))
                                                else:
                                                    Notfound = False
                            else:
                                 
                                logging.debug('outside' + str(o.get_name()))
                                
    class Castpath():  
    
        @staticmethod                            
        def get_drive():
            path = sys.executable
            while os.path.split(path)[1]:
                path = os.path.split(path)[0]
            return path
                                   
   