# Author:       francois schnell  (http://francois.schnell.free.fr)
#           
# Contributor: "awp.monkey" for a SAX patch (instead of ElementTree parsing)
#              to allow a smaller memory footprint on big files 
#              (see issue1 on project's website)
#       
# Released under the GPL license version 2
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""
Scans an OSM diff file and extract useful data to create a KML file to visualize
mapping activity of OSM. 
It is not intended for mapping, just to give an awareness of the OSM activity. 
"""

# Python imports
from xml.sax import make_parser
from xml.sax.handler import ContentHandler 
from operator import itemgetter
import time
from datetime import datetime

# Local imports
import KML

class OSMaware(ContentHandler):  
    """ 
    Extracts mapping activity as a KML from an OSM diff file
    (This is the contentHandler for a SAX parser)
    """
    def __init__(self,debug=False,verbose=False,ele="10000",kml_version=0):
        
        """
        Scans an .osc file and gather informations in lists and dictionaries
        
        Args:
            ele: lines elevation used in certain kml (0 to the ground)
        
        Resulting instance properties:
        
            self.osmData=[]    
                a list to contain them allow (see below)
            self.osmNodes=[] (Only for kml v. 1 to minimize memory footprint)
                a list containing nodes data (a dictionary per node with
                the following keys: idNode, type, latitude, 
                 longitude, timestamp, user)
            self.statsUsers={}
                a dict. containing data about the selected user.
                single key = OSM user name
                value=  [a,b,c,d,[[x],[y],[z]]]
                    where:
                    a= total number of nodes from this user
                    b= number of created nodes 
                    c= number of modified nodes
                    d= number of deleted nodes
                    [x]= a list of tuples values (lat,long)  for the created nodes
                    [y]= a list of tuples values (lat,long)  for the modified nodes
                    [z]= a list of tuples values (lat,long)  for the deleted nodes
            self.osmWays=[]
                a list containing basic data about ways (a dict. per way with
                the following keys: type, idWay, timestamp, user
        """
        # elevation used in some kml
        self.linesElevation=ele 
        # Data structure
        self.osmData=[]    # a list to contain them all
        self.osmNodes=[]   # a list to contain data about nodes (python dictionaries)
        self.osmWays=[]    # a list to contain data about ways (python dictionaries)
        self.statsUsers={} # a dict. to contain data about user's stats
        self.osmData.append(self.osmNodes)
        self.osmData.append(self.osmWays)
        self.osmData.append(self.statsUsers)

        self.nodeCount = 0
        self.wayCount = 0
        self.relationCount = 0;
        
        # feedback parameters
        self.debug=debug
        self.verbose=verbose
        self.kml_version = kml_version

    def startElement(self, name, attrs):
        """ Analyse XML element each time it is given by the SAX Parser"""
      
        # If elements of type create, modify or delete found will know the type
        # of next "nodes" element encounter (return)
    	if name == "create" :
    		self.edit_type = "create"
    		return
    	if name == "modify" :
    		self.edit_type = "modify"
    		return
    	if name == "delete" :
    		self.edit_type = "delete"
    		return
  
        # Analyse element of type "node"
    	if name == "node":
            if self.debug:
                print "Type=", self.edit_type,
                print "ID node=",attrs.get("id"),
                print "latitude=",attrs.get("lat"),
                print "longitude=",attrs.get("lon"),
                print "timestamp=",attrs.get("timestamp"),
                print repr("user=",attrs.get("user"))
            if self.kml_version == "1" :
                self.osmNodes.append({
                    'idNode':attrs.get("id"),
                    'type':self.edit_type,
                    'latitude':attrs.get("lat"),
                    'longitude':attrs.get("lon"),
                    'timestamp':attrs.get("timestamp"),
                    'user':attrs.get("user"),
                    })
                    
            # Creating user's stats for nodes
            user=attrs.get("user")
            nodeType=self.edit_type
            if self.statsUsers.has_key(user)==False:
                #total,created,modified,deleted nodes and list of positions for this user
                self.statsUsers[user]=[0,0,0,0,[[],[],[]]]
            if self.statsUsers.has_key(user):
                self.nodeCount += 1
                self.statsUsers[user][0]+=1
                if nodeType=="create": 
                    self.statsUsers[user][1]+=1
                    self.statsUsers[user][4][0].append((attrs.get("lat"),attrs.get("lon")))
                if nodeType=="modify": 
                    self.statsUsers[user][2]+=1
                    self.statsUsers[user][4][1].append((attrs.get("lat"),attrs.get("lon")))
                if nodeType=="delete": 
                    self.statsUsers[user][3]+=1
                    self.statsUsers[user][4][2].append((attrs.get("lat"),attrs.get("lon")))
        if name == "way" :
            self.wayCount += 1
            if (self.kml_version == "1") :
                self.osmWays.append({
                    'type':self.edit_type,
                    'idWay':attrs.get("id"),
                    'timestamp':attrs.get("timestamp"),
                    'user':attrs.get("user"),
                    })
        # Basic stats about the number of relations
        if name == "relation" :
            self.relationCount += 1
    
    def globalStats(self,name="Stats Summary"):
        """ 
        Returns an html stats summary (number of users, nodes, ways and a
        table with one raw per user with link to their OSM homepage)
        """
        print "Creating global stats..."
        stats=u"Total number of users: "+str(len(self.statsUsers))+"<br>"
        stats+=u"Total number of nodes created, deleted or modified: "+ str(self.nodeCount)+"<br>"
        stats+=u"Total number of ways created, deleted or modified: "+ str(self.wayCount)+"<br><br>"
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
                                        
    def createKmlV0(self,kmlFileName="output"):
        """
        The lightest kml version possible with only one "summarized" placemark
        per user representing the last known position. 
        Args:
            kmlFileName: 
                the name of the resulting kml (the osc filename per default)
        Output: 
            Creates a kml file
        """
        print "Creating KML file version 0 ..."
        myKml=KML.KML(kmlFileName)
        statsDescription=self.globalStats()
        myKml.placemarkDescriptive(description=statsDescription,name=myKml.kmlTitle)
        for userName, userStat in sorted(self.statsUsers.iteritems()):
            myKml.folderHead("<![CDATA["+unicode(userName)\
                             +"("+str(self.statsUsers[userName][0])+")]]>")
            thisLat=0
            thisLong=0
            for pathType in [0,1,2]:
                if len(self.statsUsers[userName][4][pathType])!=0:
                    thisLat=self.statsUsers[userName][4][pathType][-1][0]
                    thisLong=self.statsUsers[userName][4][pathType][-1][1]
                    if pathType==0: 
                        lineStyle="lineStyleCreated"
                        type="create"
                    if pathType==1: 
                        lineStyle="lineStyleModified"
                        type="modify"
                    if pathType==2: 
                        lineStyle="lineStyleDeleted"
                        type="delete"
            userNodesStat=[self.statsUsers[userName][0], self.statsUsers[userName][1],
                            self.statsUsers[userName][2], self.statsUsers[userName][3]]             
            myKml.placemarkSummary(thisLat,thisLong,userName,type,userNodesStat)
            myKml.folderTail()
        myKml.close()
        
    def createKmlV1(self,kmlFileName="output"):
        """ 
        Creates a detailed KML output (one placemark per node)
        placed in 3 folders ("created","modified","deleted")
        Suitable only for reasonably small osc files (not days)
        Args: -output name    
        """
        print "Creating KML file..."
        myKml=KML.KML(kmlFileName)
        statsDescription=self.globalStats()
        myKml.placemarkDescriptive(description=statsDescription,name=myKml.kmlTitle)
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
        
    def createKmlV2(self,kmlFileName="output",heightFactor=0,threshold=0.005):
        """
        A version based on lines and polygons instead of placemarks
        Args:
            kmlFileName: 
                the name of the resulting kml (the osc filename per default)
            threshold:
                lat or long detla to link together the nodes (they aer not ways) to 
                better visualize that this nodes belong to the same user. 
        Output:
            Creates a kml file
        """
        
        print "Creating KML file..."
        myKml=KML.KML(kmlFileName)
        statsDescription=self.globalStats()
        myKml.placemarkDescriptive(description=statsDescription,name=myKml.kmlTitle)
        
        for userName, userStat in sorted(self.statsUsers.iteritems()):
            myKml.folderHead("<![CDATA["+unicode(userName)\
                             +"("+str(self.statsUsers[userName][0])+")]]>")
            for pathType in [0,1,2]:
                ## Extract created nodes-"path" for this user  
                # cut subpaths if next node is above the threshold 
                lonThreshold=threshold
                latThreshold=threshold
                #
                paths=[] # list of cut paths
                firstNode=True 
                thisPath=""
                for coordinate in self.statsUsers[userName][4][pathType]:
                    thisLat=coordinate[0]
                    thisLong=coordinate[1]
                    thisNode=thisLong+","+thisLat+","\
                    +str(heightFactor)+" "
                    if firstNode==True:
                        thisPath+=thisNode
                        prevLat=thisLat
                        prevLong=thisLong
                        firstNode=False
                    else:
                        #distanceThreshold=sqrt((thisLat-prevLat)**2 + (thisLong-prevLong)**2) 
                        dLon=abs(float(thisLong)-float(prevLong))
                        dLat=abs(float(thisLat)-float(prevLat))
                        if (dLon > lonThreshold) and (dLat > latThreshold):
                            #print dLat,
                            paths.append(thisPath)
                            thisPath=""
                        elif (dLon < lonThreshold) and (dLat < latThreshold):
                            thisPath+=thisNode
                        prevLat=thisLat
                        prevLong=thisLong
                paths.append(thisPath+thisNode)
                
                #print paths            
                #if len(self.statsUsers[userName][4][0])!=0: pathCreated=pathCreated+thisNode
                if pathType==0: 
                    lineStyle="lineStyleCreated"
                    genre="Created"
                if pathType==1: 
                    lineStyle="lineStyleModified"
                    genre="Modified"
                if pathType==2: 
                    lineStyle="lineStyleDeleted"
                    genre="Deleted"
                trackCut=1
                for path in paths:
                    if path!="":
                        myKml.placemarkPath(pathName=genre+"P"+str(trackCut),
                                            coordinates=path,style=lineStyle)
                        trackCut+=1
            #if userName ==None: print "Anonymous users detected"
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
    parser.add_option("-o", "--output",dest="kmlOutput",
                      help="KML output filename (without the .kml extension)")
    parser.add_option("-k", "--kmlversion",dest="kmlVersion",
                      help="KML version desired (characterized by a number, see website)")
    parser.add_option("-e", "--elevation",dest="linesElevation",
                      help="Elevation desired for certain kml genre (lines)")
    (options,args)=parser.parse_args()
    if options.osmInput==None:
        print "I need an .osc file, type -h for help"
        sys.exit(1)
    # if no elevations is given lets assume 10 km per default for v2 kml    
    if options.linesElevation==None: options.linesElevation="100000"
        
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
        print "*",options.osmInput,"*"
        archiveType=options.osmInput.split(".")[-1]
        print "Trying to uncompress the archive of type ."+archiveType
        if sys.platform == 'win32':
            # 7za.exe must be installed in the app folder
            if os.path.dirname(options.osmInput)=="":
                os.system('7za.exe x -y "%s"' % (options.osmInput))
            else:
                os.system('7za.exe x -y "%s" -o"%s"  ' % (options.osmInput,os.path.dirname(options.osmInput)))
        if (sys.platform.find("darwin")!=-1) or (sys.platform.find("linux")!=-1):
            if archiveType=="gz" or archiveType=="GZ":
                os.system('gunzip "%s"' % options.osmInput)
            elif archiveType=="bz2" or archiveType=="BZ2":
                os.system('bzip2 -d "%s"' % options.osmInput)
        
        options.osmInput=options.osmInput.rstrip("."+archiveType)
        print "File uncompressed: ", options.osmInput
        
    if options.kmlOutput==None: options.kmlOutput=os.path.basename(options.osmInput).rstrip(".osc")
    if options.kmlVersion==None: options.kmlVersion="1"
    
    myAwareness=OSMaware(debug=False,verbose=False,ele=options.linesElevation, kml_version=options.kmlVersion)
    parser = make_parser()
    parser.setContentHandler(myAwareness)
    t0=datetime.now()
    print "Starting parsing OSM file..."
    parser.parse(options.osmInput)

    #for userName, userStat in self.statsUsers.iteritems(): print userName, userStat
    print "Number of contributors (users):", len(myAwareness.statsUsers)
    print "Number of Nodes created, deleted or modified:", myAwareness.nodeCount
    print "Number of Ways created, deleted or modified:", myAwareness.wayCount
    print "Number of Realations created, deleted or modified:", myAwareness.relationCount
  
    if options.kmlVersion=="2":
        myAwareness.createKmlV2(options.kmlOutput,heightFactor=myAwareness.linesElevation)
    if options.kmlVersion=="1":
        myAwareness.createKmlV1(options.kmlOutput)
    if options.kmlVersion=="0":
        myAwareness.createKmlV0(options.kmlOutput)
    
    print "Finished (took",(datetime.now()-t0).seconds,"seconds)"