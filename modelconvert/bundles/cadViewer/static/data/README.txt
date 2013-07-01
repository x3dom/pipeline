
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!! VERY IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!! THIS MODULE IS JUST A COPY OF THE "slimViewerV2" (but a view things are deleted) !!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!! When changing this Template, it makes sense to change the original code and than  !!!!!!!!!!!!!!!!!!
!!!!!!!!!!!! delete the the unneeded modules and rebuild this template. It is not a lot of work ;) !!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

##### create the template ########
 - delete unused modules
 - comment out line 46ff to:
 //!!!!!!!!!!!!!!!!!! not needed since the model is insert hardcoded !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 /*
 jQuery(document).ready(function () {
 	document.getElementById(MYAPP.modelRootId).setAttribute("url", '"static/data/' + MYAPP.model + '/model.x3d"');
 	document.getElementById("ViewpointMain").setAttribute("centerOfRotation", MYAPP.centerOfRotation);
 });
 */
 - edit the inline tag to for the model convert x3d url:
  <Inline id="modelRoot" nameSpaceName="inline" mapDEFToID="true" url="{{ model.inline }}" onload="mainInit();"></Inline>

 - edit the Tabs, change the container with the id tabs to:
      <div id="tabs" data-role="navbar">
          <ul>
              <li><a id="leftPane_tab_blank"      href="#"><img src="static/img/GlyphishIcons-Free/icons/176-ipad2.png" alt="full viewport"></a></li>
              <li><a id="leftPane_tab_sceneGraph" href="#" class="ui-btn-active">Graph</a></li>
          </ul>
      </div>







######## how to use ########
---- allgemein ----
- in der datei main.js ist im Kopf bereich ein block "global configuration". 
  in desem werden die ganz groben konfig einstellungen vorgenommen. 

---- modelle austauschen ----
- einen ordner in static/data/ anlegen und ihn mit dem modellnamen benennen. 
- in dem ordner sollten die dateien model.x3d, metaData.txt und annotation.txt liegen.
  metaData.txt und annotation.txt kann fehlen, das f�hrt jedoch zu einigen fehlern. 
  wenn die datei vorhanden ist muss auf jeden fall das Format richtig sein! 
	-> siehe Modulebeschreibung mod_annotation oder Beispiel Dateien
- in MYAPP.model den ordnernamen eintragen.  
- Dar�ber hinas kann die Skalierung der Annotationsmarker angegeben werden oder das CenterOfRotation

---- baum sortieren ----
- wenn der baum alphabetisch sortiert sein soll dann muss das flag MYAPP.sortTree auf true gesetzt werden  
  in der Datei htmlTree.js

---- fly to ein- / ausschalten ----
- der standardwert steht in MYAPP.isFlyToOnSelect
- zum anpassen der Visualisierung muss im Button selbst checked="checked" gesetzt werden 
  Dieser ist in der Index.html und hat die ID "checkboxFlyTo"

---- highlight farbe ----
- die farbe f�r highlighted objekt teile wird in MYAPP.x3dNodeHighlightColor gesetzt


######## interessante plugins  f�r b�ume###########
- http://www.ztree.me/v3/demo.php#_113


- http://www.designchemical.com/lab/jquery-drill-down-menu-plugin/examples/#
- http://codecanyon.net/item/jquery-drilldown-menu/2852431
- http://drilldown.createit.pl/example/classic-light.html
- http://www.filamentgroup.com/lab/jquery_ipod_style_and_flyout_menus/

######## known issues ######
- der jstree l�scht erst die komplette HTML Liste und erzeugt diese dann neu. 
  Darum kann man keine referenzen an die Knoten in der HTML Liste h�ngen. 
  Man muss also bei jedem click im jstree die zugeh�rigen x3d elemente neu per id suchen. 
  Dies ist ein gro�er Nachteil und sollte bei der auswahl zuk�nfitger baumplugins ber�cksichtigt werden. 

  
  
######## TODO ##############


---- set Render Flags (Subbaum ein- / ausblenden) ----
- akutell wird das rendern von subtrees in den Zeilen 399 und 410 in htmlTree.js gesetzt. Der entsprechnde Code: 
x3dTree.setX3dRenderHide(document.getElementById(id)); 
und
x3dTree.setX3dRenderShow(document.getElementById(id));

Die neue exp. Methode ist in Zeile 401 und 412 auskommentiert. Der Code: 
//document.getElementById(id).setVisibility(true);
und 
//document.getElementById(id).setVisibility(false);
Die Funktion war noch nicht ganz fertig als ich abgereist bin. 

   

---- annotation / meta ----
- das Annotations Modul wurde etwas �berarbeitet. Da das Metadata Modul eine abgespeckte Kopie ist,
  k�nnte es sinnvoll sein dieses entsprechend anzupassen. 
- wenn beide toggle slider (popup annotation und popup metadat) im men� auf on stehen 
  dann verschwinden die metadaten zu schnell wieder


---- usability ----
- wenn man auf einen aktuell gew�hlten knoten im accordeon tree clickt dann passiert nichts
	-> sch�ner w�re wenn sich dann die aktuelle kategorie wieder schlie�t
- wenn man die koordinaten pfeile dreht dreht sich nicht das object


- brotkrum navi verdeckt teilweise eintr�ge, besser w�re sowas 
  -> http://www.comparenetworks.com/developers/jqueryplugins/jbreadcrumb.html

---- menu ----
- menu defaults festlegen -> wenn ein toggel schalter verwendet wird sollte dieser 
  automatisch seinen start wert an die entsprechende variable bei der initialisierung geben. 
  Aktuell muss man in der Men� json datei den eintrag �ndern und im javascript die zugeh�rigen inital werte.
- allgemein ist das men� modul noch sehr experimentell :(. Da gibt es weitaus sch�nere L�sungen...
