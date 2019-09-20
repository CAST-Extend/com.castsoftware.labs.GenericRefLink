import cast.analysers.ua
from cast.analysers import log as Print, CustomObject



class genlinkExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.name = ""
        self.file = ""    
        self.initial_crc =  None
        self.file_ref=""
        self.extnls=[]
      
        return

    def start_analysis(self):
        Print.info("GenericLink : Running extension code end")
        pass
      
    def end_analysis(self):
       Print.info("GenericLink : Running extension code end") 
       pass
    
   