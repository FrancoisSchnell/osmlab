As of 2008: OSMaware is a Python command-line tool  which takes an OSM .osc file (a change set in OSM map over time) and produces a KML file of the mappers activity.

KMLs are available in three versions: 
* V0 shows only one placemark per user with summary informations and are mainly intended for big files like world day or hour changes.
* V1 is the most detailed version with one placemark per node but produces big KMLs.
* V2 shows all the nodes but in the form of polygons instead of placemarks and is "lighter" than V1.

<a href="http://farm3.static.flickr.com/2291/2486256508_c2ca194763_m.jpg"><img  src="http://farm3.static.flickr.com/2291/2486256508_c2ca194763_m.jpg" width="230" height="150">  </a>
<a href="http://farm3.static.flickr.com/2253/2460169592_b9532d4cc8_m.jpg"><img src="http://farm3.static.flickr.com/2253/2460169592_b9532d4cc8_m.jpg" width="230" height="150">  </a>
<a href="http://farm4.static.flickr.com/3288/2493493984_77cd3ba75b_m.jpg"><img src="http://farm4.static.flickr.com/3288/2493493984_77cd3ba75b_m.jpg" width="230" height="150">  </a>

<a href="http://farm4.static.flickr.com/3082/2475990682_6f3398ff9e_m.jpg" width="210" ><img src="http://farm4.static.flickr.com/3082/2475990682_6f3398ff9e_m.jpg">  </a> <a href="http://farm3.static.flickr.com/2162/2475990354_73d978eeb9_m.jpg" width="210"><img src="http://farm3.static.flickr.com/2162/2475990354_73d978eeb9_m.jpg">  </a><a href="http://farm4.static.flickr.com/3074/2509007109_de174267ca_m.jpg" width="210"><img src="http://farm4.static.flickr.com/3074/2509007109_de174267ca_m.jpg">  </a>

Usage:

python osmaware.py -i inputfile [-k kmlversion] [-e elevation] [- o outputfile]

* inputfile is the .osc file or archive (gz or bz2) or an http link to a distant file or archive. If you want to directly use archives and/or distant files on Windows you'll have to put 7zip and/or wget in your folder or path first. Some osc files can be found here.
* outputfile is an optional name for the output kml (without the .kml extension). By default the kml name as the same name as the .osc file
* kmlversion is a number which characterized the type of kml produced. 1 (a placemark per node, BIG, default), 2 ("lines",lighter than 1) and 0 (the lightest kml).
elevation is a height in meter used in certain kml using lines (0= to the ground). By giving an elevation nodes are visible from further away.

Warnings:

The KML doesn't show ways. It is not intended to help compare or help mapping but just to be "aware" of mappers activity. For legal reasons do not use any data of Google Earth/Google Maps/etc to help you mapping in Open Street Map

Contributions:

"awp.monkey" for a SAX patch (instead of ElementTree? parsing) to allow a smaller memory footprint on big file for OSMAware (see  issue1  on project's website)






