#!/usr/bin/env python3

import json
import yaml
import sys

tok="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJodHRwOi8vY2lsb2dvbi5vcmcvc2VydmVyQS91c2Vycy84NzE3ODMxIiwiYXVkIjoiY2lsb2dvbjovY2xpZW50X2lkL2QxZTkwMzkyNjA5OTFiYTk1YzI3MGYyNzcyZTdkNTUiLCJpc3MiOiJodHRwczovL2NpbG9nb24ub3JnIiwiZ2l2ZW5fbmFtZSI6Ik1hbnUiLCJmYW1pbHlfbmFtZSI6IlNoYW50aGFyYW0iLCJlbWFpbCI6Im1hbnUuc2hhbnRoYXJhbUBnbWFpbC5jb20iLCJpYXQiOjE2MTA2NDQ2OTQsImV4cCI6MTYxMTUwODY5NH0.zXdAZpkfsAuFAI1do-uuOt6eB97UAXfz5evddT40hu4"

def add_header(fout):
    fout.write("---\n")
 
def add_osc_id(res_json, fout):
    fout.write("# MANDATORY - OSC-ID of the dataset to be updated\n")
    fout.write("OSC-ID: " + res_json['id']+"\n")
    fout.write("\n\n")
    return

def add_token(res_json, fout):
    fout.write("# MANDATORY - You need to login to the portal and copy the token string under My OSC->Profile\n")
    fout.write("# If this field is empty, token must be passed in the command line. Command line token takes precedence\n")
    fout.write("# Include the token after \": \" in the same line\n")        
    fout.write("Token: \n")
    fout.write("\n\n")    
    
def add_files(res_json, fout):
    fout.write("# MANDATORY (One of Files or Directories)\n")
    fout.write("# Current list of contributed files. You can modify the list (to add files start with '- ')\n")
    fout.write("Files:\n")    
    manifest_lst = res_json['manifest']
    for i in manifest_lst:
        fout.write("- " + i['filename'] + "\n")
    
    fout.write("\n\n")  
    return

def add_manifest(res_json, fout):
    fout.write("# List of the current files and their respective hashes. Do not modify any information below\n")
    fout.write("Manifest:\n")
    manifest_lst = res_json['manifest']
    for i in manifest_lst:
        fout.write("- " + i['filename'] + ": " + i['hash'] + "\n")

    fout.write("\n\n")
    return


def add_dummy_placeholders(res_json, fout):    
    fout.write("# List of directories (start with '- ').\n")
    fout.write("# Note that all files and directories within the listed directories will be included recursively\n")
    fout.write("Directories:\n")
    fout.write("\n\n")
    
    fout.write("# A list of files and directories to exclude during contribution (start with '- ')\n")
    fout.write("ExcludeList:\n")
    fout.write("\n\n")
    return

def add_title(res_json, fout):
    fout.write("# MANDATORY - Title of the contribution\n")
    fout.write("# Include the title after \": \" in the same line\n")
    fout.write("Title: " + res_json["title"] + "\n")
    fout.write("\n\n")
    return
    
def add_description(res_json, fout):
    fout.write("# Description of the contribution\n")
    fout.write("# Include the description after \": \" in the same line\n")
    try:
        fout.write("Description: " + res_json["description"] + "\n")
    except:
        fout.write("Description: \n")
    fout.write("\n\n")        
    return
    
def add_keywords(res_json, fout):
    fout.write("# Keywords for identifying the dataset contribution\n")
    fout.write("# Include a comma separate list of keywords after \": \" in the same line\n")
    try:
        fout.write("Keywords: " + res_json["keywords"] + "\n")
    except:
        fout.write("Keywords: \n")
    fout.write("\n\n")
    return
    
def add_doi(res_json, fout):
    fout.write("# MANDATORY (One or both of DOI, URL)\n")
    fout.write("\n")
    fout.write("# DOI for the data (after \": \")\n")
    try:
        fout.write("DOI: " + res_json["doi"] + "\n")
    except:
        fout.write("DOI:\n")
    fout.write("\n\n")
    return
    
def add_url(res_json, fout):
    fout.write("# URL for the data (after \": \")\n")
    try:
        fout.write("URL: " + res_json["url"] + "\n")
    except:
        fout.write("URL:\n")    
    fout.write("\n\n")
    return
    
def add_association(res_json, fout):
    return
    
def add_funding(res_json, fout):
    fout.write("# Funding agency, add \"true\"  after \":\" to select the agency\n")
    fout.write("Funding:\n")    
    lst = ["NASA", "NIH", "NOAA", "NSF"]
    for i in lst:
        if (i in res_json["fundingAgencies"]):
            fout.write(" - " + i + ": true\n")
        else:
            fout.write(" - " + i + ":\n")
    fout.write("\n\n")     
    return
    
def add_ack(res_json, fout):
    fout.write("# Any acknowledgements (after \": \")\n")
    fout.write("# Funding related info ......\n")
    try:
        fout.write("Acknowledgment: " + res_json["acknowledgment"] + "\n")
    except:
        fout.write("Acknowledgment:\n")
    fout.write("\n\n")    
    return

def add_other(res_json, fout):    
    fout.write("#Other associated ID (can be of type AccessionNumber or PDBID)\n")
    fout.write("# Include the associated ID type after\": \" in the same line\n")
    try:
        fout.write("AssociatedID: " + res_json["otherDataIdName"] + "\n")
        fout.write("\n# Include the value of the associated ID after\": \" in the same line\n")
        fout.write("AssociatedIDVal: " + res_json["otherDataIdValue"] + "\n")
    except:
        fout.write("AssociatedID: \n")
        fout.write("\n# Include the value of the associated ID after\": \" in the same line\n")
        fout.write("AssociatedIDVal: \n")
    fout.write("\n\n")    
    return

def update_summary(new_files, old_files, updated_files, deleted_files, id):
  print ("Summary of changes due to this update:")
  print ("Number of new files: ", len(new_files))
  print ("Number of unchanged files: ", len(old_files))
  print ("Number of updated files: ", len(updated_files))
  print ("Number of deleted files: ", len(deleted_files))
  fout = open("changes.txt-"+id,"w")

  if (len(new_files) > 0):
    fout.write("New files:\n")
    for f in new_files:
      fout.write(f+"\n")
    fout.write("\n")

  if (len(updated_files) > 0):
    fout.write("Updated files:\n")                                                                             
    for f in updated_files:
      fout.write(f+"\n") 
    fout.write("\n")

  if (len(old_files) > 0):
    fout.write("Unchanged files:\n")                                                                             
    for f in old_files:
      fout.write(f+"\n") 
    fout.write("\n")

  if (len(deleted_files) > 0):
    fout.write("Deleted files:\n")                                                                             
    for f in deleted_files:
      fout.write(f+"\n") 
    fout.write("\n")

  fout.close() 
  
  print ("Please check 'changes.txt-" + id + "' for details and then continue with the update operation.")
  inp = input("Continue with the update operation (Y/N): ")
  if (inp.lower() != 'y'):
    print ("Aborting the update operation.....")
    sys.exit(-1)    



def print_summary(res):
  print("OSC-ID: {}".format(res['id'])) 
  print("Title: {}".format(res['title'])) 
  print("Description: {}".format(res['description']))
  print("Keywords: {}".format(res['keywords']))


def save_query_result(res_json):
  with open(res_json['id']+".yaml", "w") as fout:
      add_header(fout)
      add_token(res_json, fout)
      add_osc_id(res_json, fout)
      add_files(res_json, fout)
      add_dummy_placeholders(res_json, fout)
      add_title(res_json, fout)   
      add_description(res_json, fout)
      add_keywords(res_json, fout)
      add_doi(res_json, fout)
      add_url(res_json, fout)
      add_funding(res_json, fout)
      add_other(res_json, fout)
      add_ack(res_json, fout)
      add_manifest(res_json, fout)
      fout.close()   
   
# # testing the above functions
# f = open("osc-598ccdc6-9307-4ee5-91d6-3d17c6ef6b23.dat") #osc-c589dc59-38e5-497f-8d0c-d6085771a074.json")
# fout = open("test-out.yaml", "w")
# res_json = json.load(f)
# #yaml.dump(res_json, fout)

# add_header(fout)
# add_token(res_json, fout)
# add_osc_id(res_json, fout)
# add_files(res_json, fout)
# add_dummy_placeholders(res_json, fout)
# add_title(res_json, fout)    
# add_description(res_json, fout)
# add_keywords(res_json, fout)
# add_doi(res_json, fout)
# add_url(res_json, fout)
# add_funding(res_json, fout)
# add_other(res_json, fout)
# add_ack(res_json, fout)
# fout.close()
# f.close()
