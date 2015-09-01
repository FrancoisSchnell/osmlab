Few tools (and personal experimentation) around the Open Street Map project ("OSM Aware" is the first service and tool available).

**Warning: KMLs are not updated anymore for now. Also old repository address fxfoo.com is cyber squatted. Please remove links if you have some.**


### OSM Aware ###

**Why:**

I'm missing in OpenStreetMap a current "awareness" of other mappers activity around me (to spot active mappers, adapt/motivate myself in consequence, have local statistics,  eventually spot "vandalism")

**What:**

OSMaware is a Python command-line tool (and automatically updated links and KMLs on this website) which takes an OSM .osc file (a change set in OSM map over time) and produces a KML file of the activity (to be viewed in Google Earth, World Wind, Google Maps, Open Layers, Virtual Earth...). Updated network links are also available (see below).

KMLs are available in mainly three versions:

  * V0 shows only one placemark per user with summary informations and are mainly intended for big files like world day or hour changes.
  * V1 is the most detailed version with one placemark per node but produces big KMLs.
  * V2 shows all the nodes but in the form of polygons instead of placemarks and is "lighter" than V1.

**Screenshots:**


![![](http://farm3.static.flickr.com/2291/2486256508_c2ca194763_m.jpg)](http://farm3.static.flickr.com/2291/2486256508_8de573fbfa_o.png)
![![](http://farm3.static.flickr.com/2253/2460169592_b9532d4cc8_m.jpg)](http://farm3.static.flickr.com/2253/2460169592_c771287306_o.png)
![![](http://farm4.static.flickr.com/3288/2493493984_77cd3ba75b_m.jpg)](http://farm4.static.flickr.com/3288/2493493984_bced32f17b_o.png)

![![](http://farm4.static.flickr.com/3082/2475990682_6f3398ff9e_m.jpg)](http://farm4.static.flickr.com/3082/2475990682_76b44d53b2_o.png)
![![](http://farm3.static.flickr.com/2162/2475990354_73d978eeb9_m.jpg)](http://farm3.static.flickr.com/2162/2475990354_5b55583b8a_o.png)
![![](http://farm4.static.flickr.com/3074/2509007109_de174267ca_m.jpg)](http://farm4.static.flickr.com/3074/2509007109_944c106af0_o.png)


**Examples:**

**"Live" Network links (for Google Earth)**

  * World, the last minute (V1): world-minute-v1-networkLink.kml
  * World, the last day (V0): World-day-v0-networkLink.kml
  * World, the last hour (V0): world-hour-v0-networkLink.kml
  * World, the last hour (V2): world-hour-v2-networkLink.kml
  * World, the last week (V0, !few Mo!): world-week-latest-v0.kml
  * France, the last day (V0): france-day-v0-networkLink.kml
  * France, the last day (V2): france-day-v2-networkLink.kml

**Usage:**

> | python osmaware.py -i inputfile [-k kmlversion] [-e elevation] [- o outputfile] |
|:--------------------------------------------------------------------------------|

  * **inputfile** is the .osc file or archive (gz or bz2) or an http link to a distant file or archive. If you want to directly use archives and/or distant files on Windows you'll have to put [7zip](http://downloads.sourceforge.net/sevenzip/7za457.zip) and/or [wget](http://users.ugent.be/~bpuype/cgi-bin/fetch.pl?dl=wget/wget.exe) in your folder or path first. Some osc files can be found [here](http://wiki.openstreetmap.org/index.php/Planet.osm).
  * **outputfile** is an optional name for the output kml (without the .kml extension). By default the kml name as the same name as the .osc file
  * **kmlversion** is a number which characterized the type of kml produced. 1 (a placemark per node, BIG, default), 2 ("lines",lighter than 1) and 0 (the lightest kml).
  * **elevation** is a height in meter used in certain kml using lines (0= to the ground). By giving an elevation nodes are visible from further away.

**Warnings:**

**The KML doesn't show ways. It is not intended to help compare or help mapping but just to be "aware" of mappers activity. For legal reasons do not use any data of Google Earth/Google Maps/etc to help you mapping in Open Street Map**

This version V1 of the KML produced is **BIG** on world daily or hourly changes and produces a KML file roughly  twice as big as the initial .osc file. On my machines (core2 duo 2Go Vista box and MacBook) a 5 Mo KML is still fine, 10 Mo KML begins to struggle. The second kml version (v2) is lighter (lines instead of placemarks) but the summarized version (v 0) is probably the best for big files or weakest PCs.

The tool should work on Windows, OSX and Linux.

  * kml version 0:
    * a statistic description listing users and the number of nodes created, modified or deleted (click on the KML name in Google Earth, not available on the network link version)
    * one folder and placemark per user placed at the last mapping node
    * each placemark shows a summary (user's profile link, OSM map link, numbers of nodes...)
    * placemark are red if the user deleted at least one node, blue if the user mofied at least one node but didn't delete any and yellow if he created nodes without modifying of  deleting others.

  * kml version 1:
    * a statistic description listing users and the number of nodes created, modified or deleted (click on the KML name in Google Earth, not available on the network link version)
    * the nodes are gathered in 3 folders ("created", "modified", "deleted") for quick type viewing
    * each node (placemark) shows its ID, type ("created"=yellow, "modfied"=blue, "deleted"=red)  timestamp, user's ID, a link to the user's page in OSM and a link to the map location in OSM mapnik


  * kml version 2:
    * a statistic description listing users and the number of nodes created, modified or deleted (click on the KML name in Google Earth, not available on the network link version)
    * the nodes are in a folder per user
    * each user's folders contains "paths" of type created, modified or deleted (they are not ways, just consecutive nodes from the same user to spot activity). "Paths" are broken  in smaller part if consecutive nodes are too far apart from each other

If your PC is powerful enough (or you use small files) you can also view the two versions at the same time in Google Earth to combine informations.

If you want to customize/optimize the KMLs and have some notions of Python you should be able to create new ones by modifying/extending  the code available in the repository. There are handy variables available like the transparency, colors, line thickness, icons, etc.

**Contributions:**

  * "awp.monkey" for a SAX patch (instead of ElementTree parsing) to allow a smaller memory footprint on big file for OSMAware (see [issue1](https://code.google.com/p/osmlab/issues/detail?id=1) on project's website)


