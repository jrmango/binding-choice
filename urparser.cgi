#!/usr/bin/env python3

import cgi
import jinja2
import re
import requests

UR_prefix = "https://www.uniprot.org/uniref/UniRef90_"
UR_target = "P00533"
#UR_target = "wrong"
UR_suffix = ".xml"

UR_error_header = 'regexgoeshere'

uniref = ""
ask = ""
delineated = []

def UR_scrape(query):
    #calling str just in case, may be unnecessary
    ask = UR_prefix+str(query)+UR_suffix
    #ask the server for unformatted XML of similar sequences based on a reference
    #Uniref API documentation for programmatic access available at www.uniprot.org
    uniref = requests.get(ask)
    #check to see whether the database has returned a file not found error by calling a quick re.search()
    #to compare with how the UniRef error pages are usually formatted. I've pulled the reference out as a variable
    #just in case someone someday changes all the UniRef error pages to start differently
    if re.search(UR_error_header, uniref.text) == None:
        delineated = re.split('\n',uniref.text)
        return delineated
    else:
        return ["Error", str(query)]

#I am paranoid about type declaration
focus = re.search('dummmy','variable')
UR_IDNT_collector = []
UR_NMBR_collector = []
UR_NAME_collector = []

def UR_parse(UR_XMLlines):
    linecounter = -999
    #the database follows a standard format so I will be accessing lines by numbering them in relation
    #to the last header seen rather than trying to call re.search for every property I want
    count = 0
    #keeping count to cap the pulled entries at 100 for memory reasons
    for line in UR_XMLlines:
        #the first regex will also catch the query, leading to off-by-one errors unless accounted for, hence the addition of
        #dummy entries at the start of UR_NMBR_collector and UR_NAME_collector. These do not count towards the 100 limit
        UR_NMBR_collector.append("")
        UR_NAME_collector.append("")
        focus = re.search('(?<=id=).+',line)
        linecounter += 1
        if focus != None and count < 100:
            UR_IDNT_collector.append(focus.group(0))
            linecounter = 0
        if linecounter == 1:
            focus = re.search('(?<=value=).+',line)
            if focus != None and count < 100:
                UR_NMBR_collector.append(focus.group(0))
        if linecounter == 5:
            focus = re.search('(?<=value=).+',line)
            if focus != None and count < 100:
                UR_NAME_collector.append(focus.group(0))
                #since these come in groups the counter need only be incremented at the end
                count += 1
    return (UR_IDNT_collector), (UR_NMBR_collector), (UR_NAME_collector)

#defined values for IntAct Database access using RESTful API
#https://www.bindingdb.org/bind/BindingDBRESTfulAPI.jsp

IA_prefix = "http://bindingdb.org/axis2/services/BDBService/getLigandsByUniprot?uniprot="
IA_target = "P00533"
IA_suffix = ""

IA_error_header = 'regexgoeshere'

def IA_scrape(query):
    #calling str just in case, may be unnecessary
    ask = IA_prefix+str(query)+IA_suffix
    #ask the server for unformatted XML of similar sequences based on a reference
    binddb = requests.get(ask)
    #same setup as UR_scrape function
    if re.search(IA_error_header, binddb.text) == None:
        delineated = re.split('<bdb:affinities>',binddb.text)
        return delineated
    else:
        return ["Error", str(query)]

IA_mID_collector = []
IA_SML_collector = []

def IA_parse(IA_XMLlines):
    #Capping the scraping at 100 with a counter rather than calling len() a thousand times
    count = 0
    for line in IA_XMLlines:
        focus = re.search('(?<=bdb:monomerid>).+?(?=<)',line)
        if focus != None and count < 100:
            IA_mID_collector.append(focus.group(0))
        focus = re.search('(?<=bdb:smiles>).+?(?=<)',line)
        if focus != None and count < 100:
            IA_SML_collector.append(focus.group(0))
            #I'm only doing this once, these tend to come in pairs
            count += 1
    return IA_mID_collector, IA_SML_collector

BDB_prefix = "http://www.bindingdb.org/axis2/services/BDBService/getTargetByCompound?smiles="
BDB_suffix = "&cutoff=0.85"

def crossref(accquery, smilequery, unirefs):
    BDBask = BDB_prefix+str(smilequery)+BDB_suffix
    matches = requests.get(BDBask)
    binlist = []
    for element in unirefs:
        check = re.search(element,matches)
        if check != None:
            binlist.append(1)
        else:
            binlist.append(0)
    #quick and dirty yes/no output for the top 100 matches that can be assimilated into the final data fed to the HTML template
    #since the first entry of the unirefs list will be the regex-matched Uniprot accession of the user's query,
    #an accession that we already know binds to the ligand of interest, the first entry in the binlist should always
    #be 1 because a match should always be found in the DB. So if it isn't, it's a nice error handling tool.
    if binlist[0] == 1:
        return binlist
    else:
        return [-1]
    

#jinja2 template calling, code lifted from lecture examples with comments since they got the point across well.

# This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader(searchpath=".")

# This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('binding.html')

# => execute queries and output formatted results to HTML template table

MIDS = []
SMILES = []

# main scraping execution

UPquery = request.form.get("accession","");
smilequery = request.form.get("smilesid","")

if UPquery:
    URout = UR_scrape(UPquery)
    URIC, URNC, URNMC = UR_parse(URout)
    IAout = IA_scrape(UPquery)
    MIDS, SMILES = IA_parse(IAout)
    if monomerquery:
        bin_yn = crossref(UPquery, smilequery, URIC)
    else:
        bin_yn = []

("Content-Type: text/html\n\n")
print(template.render(MID=MIDS,
                      IAID=SMILES,
                      URID=URIC,
                      URNUM=URNC,
                      URNAME=URNMC,
                      matches=bin_yn))