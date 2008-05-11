# Author:  francois schnell  (http://francois.schnell.free.fr)
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
from xml.etree import ElementTree as ET
from operator import itemgetter
import time

# Local imports
import KML

class OSMaware(object):
    
    """ 
    Extracts mapping activity as a KML from an OSM diff file
    """
    
    def __init__(self,fileOSM,debug=False,verbose=False,ele="10000"):
        
        """
        Scans an .osc file and gather informations in lists and dictionaries
        
        Args:
            An .osc file
            ele: lines elevation used in certain kml (0 to the ground)
        
        Resulting instance properties:
        
            self.osmData=[]    
                a list to contain them allow (see below)
            self.osmNodes=[]
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
        
        # feedback parameters
        self.debug=debug
        self.verbose=verbose

        # Extracting useful data from the OSM file
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
                        #total,created,modified,deleted nodes and list of positions for this user
                        self.statsUsers[user]=[0,0,0,0,[[],[],[]]]
                    if self.statsUsers.has_key(user):
                        self.statsUsers[user][0]+=1
                        if nodeType=="create": 
                            self.statsUsers[user][1]+=1
                            self.statsUsers[user][4][0].append((i.attrib.get("lat"),i.attrib.get("lon")))
                        if nodeType=="modify": 
                            self.statsUsers[user][2]+=1
                            self.statsUsers[user][4][1].append((i.attrib.get("lat"),i.attrib.get("lon")))
                        if nodeType=="delete": 
                            self.statsUsers[user][3]+=1
                            self.statsUsers[user][4][2].append((i.attrib.get("lat"),i.attrib.get("lon")))
                                                
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

        #for userName, userStat in self.statsUsers.iteritems(): print userName, userStat
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
                                        
    def createKmlV1(self,kmlFileName="output"):
        """ 
        Creates a detailed KML output (one placemark per node)
        placed in 3 folders ("created","modified","deleted")
        Suitable only for reasonably small osc files (not days)
        Args:
            
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
        
    def createKmlV2(self,kmlFileName="output",heightFactor=10000,threshold=0.005):
        """
        A 'lighter' kml version focused on users and polygons
        Args:
            kmlFileName: 
                the name of the resulting kml (the osc filename per default)
            heightFactor:
                artifical altitude of the nodes (to see them better when far away)
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
            os.system('bzip2 -d "%s"' % options.osmInput)
        
        options.osmInput=options.osmInput.rstrip("."+archiveType)
        print "File uncompressed: ", options.osmInput
        
    if options.kmlOutput==None: options.kmlOutput=os.path.basename(options.osmInput).rstrip(".osc")
        
    myAwareness=OSMaware(options.osmInput,debug=False,verbose=False,ele=options.linesElevation)
    
    if options.kmlVersion=="2":
        myAwareness.createKmlV2(options.kmlOutput,heightFactor=myAwareness.linesElevation)
    else:
        myAwareness.createKmlV1(options.kmlOutput)
    
    print "Finished"
    