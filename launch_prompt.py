#!/usr/bin/python
  
import sys
import ConfigParser
from subprocess import call
 
conf_file = sys.argv[1]
    
Config = ConfigParser.ConfigParser()
print "Reading configuration file from " + conf_file
Config.read(conf_file)
  
def main():
   
    # assign config parameters
    script_dir = ConfigSectionMap("locations")['script_dir']
    sample_dir = ConfigSectionMap("locations")['sample_dir']
    sample_list = ConfigSectionMap("locations")['sample_list']
    tmp_dir = ConfigSectionMap("locations")['tmp_dir']
    blast_db = ConfigSectionMap("locations")['blast_db']
    blast_homology = ConfigSectionMap("parameters")['blast_homology'] 
    core_no = ConfigSectionMap("parameters")['core_no']
    run_mode = ConfigSectionMap("parameters")['run_mode']
    
    #log_file = open(tmp_dir + Run_Log.txt, 'w')
    #log_file.write("##Parameters used in this analysis run##")
    
    if (run_mode == "both") or (run_mode == "processing_only"):
        print "Removing previous abundance and website files"
        call(["rm", "-r",  tmp_dir + "/cdhit_files"])
        call(["rm", "-r",  tmp_dir + "/blast_files"])
        call(["mkdir", tmp_dir + "/cdhit_files"])
        call(["mkdir", tmp_dir + "/blast_files"])

    if (run_mode == "both") or (run_mode == "analysis_only"):
        print "Removing previous abundance and website files"
        call(["rm", "-r",  tmp_dir + "abundance_files"])
        call(["rm", "-r",  tmp_dir + "html_files"])
        call(["mkdir", tmp_dir + "/abundance_files"])
        call(["mkdir", tmp_dir + "/html_files"])
    
    
    open_sample_list = open(sample_list, "rU")
    
    
    for sample in open_sample_list:
        rows = sample.split('\t') 
        sampleID =  rows[0]
    
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Running prompt_sample.py on sample " + sampleID + " (" + rows[1].rstrip() + ")"
        call([script_dir + "prompt_sample.py", sample_dir, sampleID, tmp_dir, blast_db, blast_homology, core_no, script_dir, run_mode])
    
    
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
    
if __name__ == '__main__':
    main()
