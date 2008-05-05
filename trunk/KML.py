#!/usr/bin/python

################################################################################
#
# Author: francois.schnell  francois.schnell@gmail.com
#                           http://francois.schnell.free.fr  
# This script is released under the GPL license v2
#
# A module to create a KML (in particular for OSM aware)
################################################################################

class KML(object):
    """ 
    Creates a KML file (in particular for OSMaware script)
    """
    
    def __init__(self,name="default_name"):
        """
        Create and write the KML head 
        """
        self.f=open(name+".kml","wb")
        kmlHead_p1=u"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
<Document>
<name>"""+name+"""</name>"""

        kmlHead_p2="""
<Style id="lineStyleCreated">
<PolyStyle>
<color>4400ffff</color>
</PolyStyle>
<LineStyle>
<color>cc00ffff</color>
<width>2</width>
</LineStyle>
</Style>
<Style id="lineStyleModified">
<PolyStyle>
<color>44ff0000</color>
</PolyStyle>
<LineStyle>
<color>ccff0000</color>
<width>3</width>
</LineStyle>
</Style>
<Style id="lineStyleDeleted">
<PolyStyle>
<color>440000ff</color>
</PolyStyle>
<LineStyle>
<color>cc0000ff</color>
<width>4</width>
</LineStyle>
</Style>
<Style id="sh_ylw-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
</Icon>
<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
</IconStyle>
</Style>
<Style id="sh_red-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
</Icon>
<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
</IconStyle>
<ListStyle>
    </ListStyle>
</Style>
<Style id="sh_blue-pushpin">
<IconStyle>
<scale>1.3</scale>
<Icon>
<href>http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png</href>
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
        """
        
        if type=="create": placemarkStyle="sh_ylw-pushpin"
        if type=="modify": placemarkStyle="sh_blue-pushpin"
        if type=="delete": placemarkStyle="sh_red-pushpin"
        
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
    
    def placemarkDescriptive(self,description="",name="Stats"):
        """ 
        Create and write a description  with the given
        html in the description argument (no need for lat/long) and the name
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
        Creates a placemark to show a path (coordinates)
        """
        
        content=u"<Placemark>\n<name>"+unicode(pathName)+"</name>\n"\
        +"<styleUrl>#"+style+"</styleUrl>\n<LineString>\n<tessellate>1</tessellate>\n"\
        +"<altitudeMode>relativeToGround</altitudeMode>\n<extrude>1</extrude>\n"\
        +"<coordinates>"+coordinates+"</coordinates>\n</LineString>\n</Placemark>"
        self.f.write(content.encode("utf-8"))
        
    def folderHead(self,folderName):
        """
        Begin a new folder
        """
        folderTags=u"\n<Folder>\n<name>"+folderName+"</name>\n"
        self.f.write(folderTags.encode("utf-8"))
    
    def folderTail(self):
        folderTags=u"\n</Folder>\n"
        self.f.write(folderTags.encode("utf-8"))
        
    def close(self):
        """Ending of the kml file"""
        print "Close kml..."
        kmlTail=u"\n</Document>\n</kml>"
        #self.f.write(kmlTail)
        self.f.write(kmlTail.encode("utf-8"))
        self.f.close()
    
if __name__=="__main__":
    print "Engaging..."
    myKml=KML("kmltest")
    myKml.placemark(latitude="47.258",longitude="7.12354",idNode="ID123456",
                    user="toto",timestamp="1erjanvier")
    myKml.close()