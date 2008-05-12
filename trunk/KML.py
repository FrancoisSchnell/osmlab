# Author:  francois schnell  (http://francois.schnell.free.fr)
#                      
# Released under the GPL license version 2
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

class KML(object):
    """ 
    Creates a KML file (in particular for the OSMaware app.)
    """
    
    def __init__(self,name="default",
                 lineColor1="cc00ffff", polyColor1="0000ffff",width1="2",
                 lineColor2="ccff0000", polyColor2="00ff0000",width2="3",
                 lineColor3="cc0000ff", polyColor3="000000ff",width3="4",
                 urlIcon1="http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png",
                 urlIcon2="http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png",
                 urlIcon3="http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png"):
        """
        Create and write the KML head 
        Args:
            1: line and polystyle color and width for created nodes
            2: line and polystyle color and width for modified nodes
            3: line and polystyle color and width for deleted nodes
            colors are hexBinary value: aabbggrr 
                                (where aa is alpha value
                                       bb is blue value
                                       gg is green value
                                       rr is red value)   
        """
        
        self.f=open(name+".kml","wb")
    
        # set kml title (get the filename only if a path was given)
        if name.find("\\")>0:
            self.kmlTitle=name.split("\\")[-1:][0]
        elif name.find("/")>0:
            self.kmlTitle=name.split("/")[-1:][0]
        else:
            self.kmlTitle=name
    
        kmlHead_p1=u"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
<Document>
<name>"""+self.kmlTitle+"""</name>"""

        kmlHead_p2="""
<Style id="lineStyleCreated">
<PolyStyle>
<color>"""+polyColor1+"""</color>
</PolyStyle>
<LineStyle>
<color>"""+lineColor1+"""</color>
<width>2</width>
</LineStyle>
</Style>
<Style id="lineStyleModified">
<PolyStyle>
<color>"""+polyColor2+"""</color>
</PolyStyle>
<LineStyle>
<color>"""+lineColor2+"""</color>
<width>3</width>
</LineStyle>
</Style>
<Style id="lineStyleDeleted">
<PolyStyle>
<color>"""+polyColor3+"""</color>
</PolyStyle>
<LineStyle>
<color>"""+lineColor3+"""</color>
<width>4</width>
</LineStyle>
</Style>
<Style id="sh_ylw-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>"""+urlIcon1+"""</href>
</Icon>
<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
</IconStyle>
</Style>
<Style id="sh_blue-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>"""+urlIcon2+"""</href>
</Icon>
<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
</IconStyle>
<ListStyle>
</ListStyle>
</Style> 
<Style id="sh_red-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>"""+urlIcon3+"""</href>
</Icon>
<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
</IconStyle>
<ListStyle>
    </ListStyle>
</Style>
"""
        kmlHead=kmlHead_p1+kmlHead_p2
        self.f.write(kmlHead.encode("utf-8"))
    
    def placemark(self,latitude="0",longitude="0",idNode="0",user="",timestamp="",type=""):
        """ 
        Create and write a placemark at given latitude/longitude
        Args:
            - latitude
            - longitude
            - node id in OSM
            - user name
            - timestamp
            - type of node (created, modified, deleted)
        """
        
        if type=="create": placemarkStyle="sh_ylw-pushpin"
        if type=="modify": placemarkStyle="sh_blue-pushpin"
        if type=="delete": placemarkStyle="sh_red-pushpin"
        if user==None: user="None"
        
        if user!="None": 
            userUrl="<br>Created by <a href='http://www.openstreetmap.org/user/"+user+"'>"+user+"</a>"
        else:
            userUrl="<br>Created by: no user found for this node"
        
        content=u"<Placemark>\n<name>"+user+"</name>"\
        + "<description><![CDATA[Node ID= "+idNode+ "<br> Node type= "+type \
        + userUrl\
        +"<br>timestamp: "+timestamp\
        +"<br><a href='http://www.openstreetmap.org/?lat="+str(latitude)+"&lon="+str(longitude)+"&zoom=17'>"\
        +"See on OpenStreetMap </a> <br> ]]></description>\n"\
        +"<styleUrl>#"+placemarkStyle+"</styleUrl>"\
        + "<Point> <coordinates>"+longitude+","+latitude+",0</coordinates></Point>\n</Placemark>\n"
        self.f.write(content.encode("utf-8"))

    def placemarkSummary(self,latitude="0",longitude="0",user="",type="create",userNodesStat=[0,0,0,0]):
        """
        Create a 'summary' placemark at a given location 
        Args:
            - latitude, longitude, user name, type of node
            - userNodesStat list containing the total number, created, modified, deleted
        """
        if type=="create": placemarkStyle="sh_ylw-pushpin"
        if type=="modify": placemarkStyle="sh_blue-pushpin"
        if type=="delete": placemarkStyle="sh_red-pushpin"
        if user==None: user="None"
        
        if user!="None": 
            userUrl="<a href='http://www.openstreetmap.org/user/"+user+"'>"+user+"</a>"
        else:
            userUrl="<br>Created by: no user found for this node"  
                 
        content=u"<Placemark>\n<name>"+user+"</name>"\
        + "<description><![CDATA[<table border='0' padding='3' width='200' height='170'><tr><td>"\
        +"User: "+userUrl\
        +"<br>Total number of nodes: "+str(userNodesStat[0])\
        +"<br>Nodes created: "+str(userNodesStat[1])\
        +"<br>Nodes modified: "+str(userNodesStat[2])\
        +"<br>Nodes deleted: "+str(userNodesStat[3])\
        +"<br>Last position: "+str(latitude)+" , "+str(longitude)\
        +"<br>See on <a href='http://www.openstreetmap.org/?lat="+str(latitude)+"&lon="+str(longitude)+"&zoom=16'>"\
        +"OSM map</a> <br> </td></tr></table>]]></description>\n"\
        +"<styleUrl>#"+placemarkStyle+"</styleUrl>"\
        + "<Point> <coordinates>"+str(longitude)+","+str(latitude)+",0</coordinates></Point>\n</Placemark>\n"
        self.f.write(content.encode("utf-8"))        
        
    def placemarkDescriptive(self,description="",name="default"):
        """ 
        Create and write a description  with the given
        html content in the description argument (no need for lat/long)
        Args:
            descrition (HTML or text)
            name/title of the description
        """
        content=u"\n<name>"+name+"</name>\n"\
        +"<Snippet maxLines='0'></Snippet>\n"\
        +"<description>\n"\
        +"<![CDATA[\n"\
        +"<table border='1' padding='3' width='600'><tr><td> "+ description\
        + "</td></tr></table>"+"\n]]>\n</description>\n"
        self.f.write(content.encode("utf-8"))
    
    def placemarkPath(self,pathName,coordinates,style="lineStyleCreated"):
        """
        Creates and writes a placemark to show a path (a bunch of coordinates)
        Args:
         pathName: name of the path
         coordinates: a string of the from 'lat,lon,height lat,lon,height ...'
         style: the style to use (see KML head)
        """
        content=u"<Placemark>\n<name>"+unicode(pathName)+"</name>\n"\
        +"<styleUrl>#"+style+"</styleUrl>\n<LineString>\n<tessellate>1</tessellate>\n"\
        +"<altitudeMode>relativeToGround</altitudeMode>\n<extrude>1</extrude>\n"\
        +"<coordinates>"+coordinates+"</coordinates>\n</LineString>\n</Placemark>"
        self.f.write(content.encode("utf-8"))
        
    def folderHead(self,folderName):
        """
        Create and write the beginning of a new folder
        Args:
            folderName: name of the folder
        """
        folderTags=u"\n<Folder>\n<name>"+folderName+"</name>\n"
        self.f.write(folderTags.encode("utf-8"))
    
    def folderTail(self):
        """
        Create and write the head of a folder
        """
        folderTags=u"\n</Folder>\n"
        self.f.write(folderTags.encode("utf-8"))
        
    def close(self):
        """Create and write the end of a kml file"""
        print "Close kml..."
        kmlTail=u"\n</Document>\n</kml>"
        #self.f.write(kmlTail)
        self.f.write(kmlTail.encode("utf-8"))
        self.f.close()
    
if __name__=="__main__":
    print "Engaging kml test..."
    myKml=KML("kmltest")
    myKml.placemark(latitude="47.258",longitude="7.12354",idNode="ID123456",
                    user="toto",timestamp="1erjanvier")
    myKml.close()