#!/usr/bin/python

################################################################################
#
# Author:  francois schnell
#          francois.schnell@gmail.com  http://francois.schnell.free.fr
#                      
# This script is released under the GPL license v2
#
# Scans an OSM diff file and extract useful data (a list of Python dictionaries)
# As a result it outputs a KML file to visualize mapping activity of OSM 
# ( It is not intended for mapping, just to give an awareness of the OSM activity ) 
#
################################################################################
# my  todo-list:
# CLI: 
# - add 'genre' or 'kind' CLI params to select the genre of KML desired
# - add verbose and debug params 
# - add help param
# - Others:
# - make a slim down version of the kml for small config PC or big OSM files
# - KML: 2D genre, 3D genre, etc
# - add a time slider option in GE
# - unzip and test for linux and darwin
################################################################################

from xml.etree import ElementTree as ET
from operator import itemgetter
import time

import KML

class OSMaware(object):
    
    """ 
    A class to extract mapping activity as KML from an OSM diff file
    """
    
    def __init__(self,fileOSM,debug=False,verbose=False):
        
        """
        Scan the .osc file and gather informations in lists and dictionaries (see code)
        """
        # Data structure
        self.osmData=[]    # a list to contain them all
        self.osmNodes=[]   # a list to contain data about nodes (python dictionaries)
        self.osmWays=[]    # a list to contain data about ways (python dictionaries)
        self.statsUsers={} # a dict. to contain data about user's stats
        self.osmData.append(self.osmNodes)
        self.osmData.append(self.statsUsers)
        self.osmData.append(self.osmWays)
        # feedback parameters
        self.debug=debug
        self.verbose=verbose

        ## Extracting useful data from the OSM file
        print "Parsing OSM file..."     
        tree=ET.parse(fileOSM)
        root=tree.getroot()
                   
        for tag in root:
            if self.debug: 
                time.sleep(0.1)
                print "Element: ",tag, "Type=", tag.tag
            aNodeList=tag.findall("node")
            if len(aNodeList) !=0: 
                if self.debug: print "Elements of type 'node': ", aNodeList
                
                # Creating nodes list and user's stats
                for i in aNodeList:
                    if self.debug:
                        print "Type=", tag.tag,
                        print "ID node=",i.attrib.get("id"),
                        print "latitude=",i.attrib.get("lat"),
                        print "longitude=",i.attrib.get("lon"),
                        print "timestamp=",i.attrib.get("timestamp"),
                        print repr("user=",i.attrib.get("user"))
                    self.osmNodes.append({
                                 'idNode':i.attrib.get("id"),
                                 'type':tag.tag,
                                 'latitude':i.attrib.get("lat"),
                                 'longitude':i.attrib.get("lon"),
                                 'timestamp':i.attrib.get("timestamp"),
                                 'user':i.attrib.get("user"),
                                 })
                    
                    # Creating user's stats for nodes
                    user=i.attrib.get("user")
                    nodeType=tag.tag
                    if self.statsUsers.has_key(user)==False:
                        self.statsUsers[user]=[0,0,0,0]#total,created,modified,deleted
                    if self.statsUsers.has_key(user):
                        self.statsUsers[user][0]+=1
                        if nodeType=="create": self.statsUsers[user][1]+=1
                        if nodeType=="modify": self.statsUsers[user][2]+=1
                        if nodeType=="delete": self.statsUsers[user][3]+=1                        
            
            # Creating ways list
            aWayList=tag.findall("way")
            if len(aWayList) != 0:
                for i in aWayList:
                    self.osmWays.append({
                                    'type':tag.tag,
                                    'idWay':i.attrib.get("id"),
                                    'timestamp':i.attrib.get("timestamp"),
                                    'user':i.attrib.get("user"),
                                         })
                    #thisWayNodes=i.getiterator(tag="nd")

        print "Number of contributors (users):", len(self.statsUsers)
        print "Number of Nodes created, deleted or modified:", len(self.osmNodes)
    
    def globalStats(self,name="Stats Summary"):
        
        """ 
        Returns an html stats summary (number of users, nodes, ways and a
        table with one raw per user with link to their OSM homepage)
        """
        
        print "Creating global stats..."
        stats=u"Total number of users: "+str(len(self.statsUsers))+"<br>"
        stats+=u"Total number of nodes created, deleted or modified: "+ str(len(self.osmNodes))+"<br>"
        stats+=u"Total number of ways created, deleted or modified: "+ str(len(self.osmWays))+"<br><br>"
        stats+="<table border='1' padding='3' width='600'>"
        stats+="<tr><td>Author</td><td>Total (nodes)</td><td>Created</td><td>Modified</td><td>Deleted</td></tr>"
        
        usersResult=sorted(self.statsUsers.items(), key=itemgetter(1),reverse=True)
        for u in usersResult:
            thisUser=unicode(u[0])
            if thisUser !="None":
                stats+=u'<tr><td><a href="http://www.openstreetmap.org/user/'+thisUser\
                +'">'+thisUser+"</a></td>"
            else:
                stats+="<tr><td>None</td>"
            stats+=u"<td>"+str(u[1][0])+"</td><td>"+str(u[1][1])\
            +"</td><td>"+str(u[1][2])+"</td><td>"+str(u[1][3])+"</tr>"
        
        return stats
                                        
    def createKml(self,kmlFileName="output"):
        """ 
        Creates the KML output
        """
        
        print "Creating KML file..."
        myKml=KML.KML(kmlFileName)
        statsDescription=self.globalStats()
        myKml.placemarkDescriptive(description=statsDescription,name=kmlFileName)
        
        for aType in ["create","modify","delete"]:  
            myKml.folderHead(aType)
            for node in self.osmNodes:
                if node["type"]==aType:
                    if self.verbose==True:
                        print node["latitude"], node["longitude"],node["idNode"],\
                                     node["user"], node["timestamp"],node["type"]
                    if node["user"]==None: node["user"]="None"
                    myKml.placemark(node["latitude"],node["longitude"],node["idNode"],
                            node["user"],node["timestamp"],node["type"])
            myKml.folderTail()
        myKml.close()

if __name__=="__main__":
    
    """
    Command-line version
    Usage: python osmaware.py -i osmfile.osc [- o outputfile]
    """
    
    import os, sys
    from optparse import OptionParser
    
    # Command line parameters
    parser=OptionParser()
    parser.add_option("-i", "--input",dest="osmInput",help="OSM input file (.osc)")
    parser.add_option("-o", "--output",dest="kmlOutput",help="KML output filename (without the .kml extension)")
    (options,args)=parser.parse_args()
    
    # If an OSM HTML location is given in input fetch it first (wget must be in your path or current folder)
    if (options.osmInput.find("http://")!=-1):
        print "Found http input, attempting to retrieve the distant file..."
        if sys.platform == 'darwin':
            os.system('curl -O %s '%options.osmInput)
        else:
            os.system('wget %s '%options.osmInput)
        options.osmInput=os.curdir+"/"+options.osmInput.split("/")[-1]
        print options.osmInput
    
    # If bz2 or gz archive is detected uncompress to osc file (using 7zip CLI on win)
    if (options.osmInput.find(".bz2")>0) or (options.osmInput.find(".BZ2")>0)\
        or (options.osmInput.find(".gz")>0) or (options.osmInput.find(".GZ")>0):
        archiveType=options.osmInput.split(".")[-1]
        print "Trying to uncompress the archive of type ."+archiveType
        if sys.platform == 'win32':
            # 7za.exe must be installed in the app folder
            os.system('7za.exe x -y -o"%s" "%s" ' % (os.path.dirname(options.osmInput),options.osmInput))
        if (sys.platform.find("darwin")!=-1) or (sys.platform.find("linux")!=-1):
            os.system('bzip2 -d "%s"' % options.osmInput)
        
        options.osmInput=options.osmInput.rstrip("."+archiveType)
        print "File uncompressed: ", options.osmInput
        
    if options.kmlOutput==None: options.kmlOutput=os.path.basename(options.osmInput).rstrip(".osc")
        
    myAwareness=OSMaware(options.osmInput,debug=False,verbose=False)
    myAwareness.createKml(options.kmlOutput)
    
    print "Finished"
    