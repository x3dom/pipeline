var MYAPP = {}; // always put global Variables into some object like this or use better technics. This avoids errors.

MYAPP.xmlPattern = null;
MYAPP.xml = null;
MYAPP.pattern = {};

/***
 * callback for the pattern xml file.
 * @param pattern
 */

function readPattern(xmlData){
    MYAPP.xmlPattern = xmlData;
    processPattern(xmlData);
    //printPattern();

    if(MYAPP.xml !== null){
        createMetaDataList();
    }
}

function printPattern(){
    for(var i = 0; i < MYAPP.pattern.length; i++){
        console.log(MYAPP.pattern[i].title + " : " + MYAPP.pattern[i].path + " : " + MYAPP.pattern[i].position);
    }
    var json_text = JSON.stringify(MYAPP.pattern, null, 4);
    console.log(json_text);
}

function processPattern(xmlNode){
    var children = $(xmlNode).children();
    if(children.length > 0 ){
        $(xmlNode).children().each(function () {
            //console.log(this.tagName);
            processPattern($(this));
        });
    }
    else{
        processLeaf($(xmlNode));
    }
}

function processLeaf(node){
    var print = node.attr("print");
    if(!print || print == undefined || print.toLowerCase() != "true"){
        return;
    }

    var printSection = node.attr("printSection");
    if(!printSection){
        printSection = "Default";
    }

    var printTitle = node.attr("printTitle");
    if(printTitle == undefined){
        printTitle = node.prop("tagName");
    }
    //console.log(title);

    var parents = node.getParentPathIndices();
    //console.log(parents);

    console.log(node.getParentPath());

    var entry = {title: printTitle, path: parents};

    if(!MYAPP.pattern[printSection]){
        //var section = {section: printSection, items: new Array()};
        MYAPP.pattern[printSection] = new Array();
    }
    MYAPP.pattern[printSection].push(entry);
    //console.log(printSection + " - " + MYAPP.pattern[printSection])

}

/***
 * add a function to jquery that return the path from the parent to the node itself
 * this path just contains the indices of the elements in the tree (not the names)
 * source: http://stackoverflow.com/questions/2068272/getting-a-jquery-selector-for-an-element
 * @return {*}
 */
jQuery.fn.getParentPathIndices = function () {
    if (this.length != 1) throw 'Requires one element.';

    var path = "", node = this, index;
    while (node.length) {
        var realNode = node[0];
        if (!realNode.localName) break;     // avoid that the first element (document) dose stupid stuff

        var parent = node.parent();

        var siblings = parent.children();
        index = siblings.index(realNode);

        path = (path !== "" ? index + ' ' : index) + path;
        node = parent;
    }

    return path;
};


/***
 * add a function to jquery that return the path from the parent to the node itself
 * source: http://stackoverflow.com/questions/2068272/getting-a-jquery-selector-for-an-element
 * @return {*}
 */
jQuery.fn.getParentPath = function () {
    if (this.length != 1) throw 'Requires one element.';

    var path, node = this;
    while (node.length) {
        var realNode = node[0], name = realNode.localName;
        if (!name) break;
        //name = name.toLowerCase();

        var parent = node.parent();

        var siblings = parent.children(name);
        if (siblings.length > 1) {
            name += ':::eq(' + siblings.index(realNode) + ')';
        }

        path = name + (path ? ' ' + path : '');
        node = parent;
    }

    return path;
};

/***
 * callback for the xml meta data file
 * @param xml
 */
function readXML(xml){
    MYAPP.xml = xml;
    if(MYAPP.xmlPattern !== null){
        createMetaDataList();
    }
}


/****
 * this is like a mein function
 * it creates the meta data list at the left side of the document
 */
function createMetaDataList() {
	var element;
	var title;
	var content;
    var contentCnt = 0;
    var patternSection;
    var section;

	//console.log(MYAPP.xml.toString());
	//console.log($(MYAPP.xml).text());

    for(var secKey in MYAPP.pattern){
        patternSection = MYAPP.pattern[secKey];
        section = createCollapsibleItem(secKey, "b");
        contentCnt = 0
        //console.log(secKey)

        for(var i = 0; i < patternSection.length; i++){
            title = patternSection[i].title.replace(/_/g," ");
            content = getContent(patternSection[i].path);
            if(content){
                element = createCollapsibleItem(title, "a");
                element.append( jQuery('<p >' + content + '</p>') );
                section.append(element);
                contentCnt++;
            }
        }
        if(contentCnt > 0){
            jQuery('#metaDataList').append(section);
        }
    }

	// the list has to be initialised, because we changed the DOM after jQuery did so
	jQuery('div[data-role=collapsible]').collapsible();
}

/***
 * catch the content for one entry in the meta data list from the xml file.
 * content is the value of the corresponding tag or the value of attributes in this tag
 * @param path: path to the tag encoded as a string of numbers. each number represents
 *              the index of on element in one hirachie level
 * @return {*}: returns a string with the content
 */
function getContent(path){
    var pathArr = path.split(' ');
    //console.log(pathArr);
    var node = getNode($(MYAPP.xml), pathArr, 0);

    if(!node || node == null) {
        console.error("Node from pattern does not match with any node from the xml file! No Content can be loaded.");
        return "";
    }

    var content = node.text();
    // if the tag dose not contain content look in attributes
    if((!content || content === undefined || content == "") && node.attr("Mandatory")){
        content = "<strong>&lt;Mandatory&gt;:<br/></strong>" + node.attr("Mandatory");
    }
    if((!content || content === undefined || content == "") && node.attr("Recommended")){
        content = "<strong>&lt;Recommended&gt;:</strong><br/>" + node.attr("Recommended");
    }
    //console.log("cont: " + content);

    return content;
}

/***
 * catch the node that corresponds with the path.
 * works with an array of indices. each index is representing on node in one hirachical level
 * @param node: node to start with
 * @param path: array with all the indices
 * @param i: current hirachical level
 * @return {*}: node that has been found in the xml structure
 */
function getNode(node, path, i){
    if(!i || i < 0){
        i = 0;
    }

    var index = parseFloat(path[i]);
    //console.log("i: " + i + " index " + index);
    var newNode = node.children().eq(index);
    //console.log("node: " + (node)[0].tagName + " --- new node: " + (newNode)[0].tagName);

    if(i < path.length - 1){
        return getNode(newNode, path, i + 1);
    }
    return newNode;
}

/***
 * create on entry item (= one "button" with content) in the metadata list.
 * @param title: the header for the button to open the content part
 * @param theme: letters between a and e change the appearance of the list
 * @return {*}: entry object that can be appended in the Meta data list
 */
function createCollapsibleItem(title, theme) {
	var group;
	var header;
    var theme = theme;

    if(!theme){
        theme = "b";
    }
	/*
	 <div data-role="collapsible" data-collapsed="false" data-mini="true" class="menuGroupHide">
	 <h3>I'm a header</h3>
	 <p>I'm the collapsible content. By default I'm closed, but you can click the header to open me.</p>
	 </div>
	 */

	// create div for group
	group = jQuery('<div/>').attr({
		"data-role" : "collapsible",
		"data-collapsed" : "true",
		"data-mini" : "true",
		"data-iconpos" : "right",
		"data-theme" : theme,
		"class" : "metaDateEntry"
	});

	// create header
	header = jQuery('<h3/>').text(title);
	group.append(header);

	return group;
}

// workaround for meshlab output with specular '1 1 1'
function fixSpecular() {
    var mts = document.getElementsByTagName("Material");
    for (var i=0; i<mts.length; i++) {
        mts[i].setAttribute("specularColor", "0.5 0.5 0.5");
        mts[i].setAttribute("shininess", "0.2");
    }
}

function popup(){
	jQuery(".popUp").fadeIn();
}
