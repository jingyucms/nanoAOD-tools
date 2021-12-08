import json
import os

infile = 'datasamples_2018.json'
#infile = 'mcsamples_2018.json'

with open(infile) as json_file:

   data = json.load(json_file)
   
   for p in data:
      f = open("./crabSubmits/"+p['name']+".py","w+")
      
      f.write("from WMCore.Configuration import Configuration\n")
      f.write("from CRABClient.UserUtilities import config\n")

      f.write("config = config()\n")
      f.write("\n")
      
      f.write("config.section_('General')\n")
      f.write("config.General.requestName = 'cmsdas_"+p['name']+"'\n")
      f.write("config.General.workArea = 'crab_projects'\n")
      f.write("config.General.transferOutputs = True\n")
      f.write("config.General.transferLogs = True\n")
      f.write("\n")
      
      f.write("config.section_('JobType')\n")
      f.write("config.JobType.pluginName = 'Analysis'\n")
      f.write("config.JobType.psetName = 'PSet.py'\n")
      f.write("config.JobType.scriptExe = 'crab_script.sh'\n")
      if ('xs' in p) and ('nEvents' in p):
          w = eval(p['xs'])/eval(p['nEvents'])
          scriptArgs = "['arg1=%d', 'arg2=%s']" % (int(p['year']), w)
      else :
          scriptArgs = "['arg1=%d']" % int(p['year'])
      f.write("config.JobType.scriptArgs = %s\n" % scriptArgs)
      f.write("config.JobType.inputFiles = ['keep_and_drop.txt', 'crab_script.py', '../scripts/haddnano.py']\n")
      #f.write("config.JobType.inputFiles = ['crab_script.py', '../scripts/haddnano.py']\n")
      f.write("config.JobType.sendPythonFolder = True\n")
      f.write("config.JobType.allowUndistributedCMSSW = True\n")
      f.write("\n")
   
      f.write("config.section_('Data')\n")
      if 'lumiMask' in p:
         f.write("config.Data.lumiMask='"+p['lumiMask']+"'\n")
      f.write("config.Data.inputDataset = '"+p['inputDataset']+"'\n")
      f.write("config.Data.inputDBS='global'\n")
      #f.write("config.Data.splitting='Automatic'\n")
      f.write("config.Data.splitting = 'FileBased'\n")
      f.write("config.Data.unitsPerJob = 1\n")
      f.write("config.Data.outLFNDirBase = '/store/user/fjensen/cmsdas_07122021/'\n")
      f.write("config.Data.publication = False\n")
      f.write("\n")

      f.write("config.section_('Site')\n")
      f.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
      f.write("\n")
    
      f.close()

      #actually submit jobs or not
      os.system("crab submit -c " + f.name)
      #break

