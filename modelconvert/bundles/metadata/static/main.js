var MYAPP = {}; // always put global Variables into some object like this or use better technics. This avoids errors.

MYAPP.pattern = null;
MYAPP.xml = null;

/***
 * callback for the pattern json file.
 * @param pattern
 */
function readPattern(pattern){
    MYAPP.pattern = pattern;
    if(MYAPP.xml !== null){
        createMetaDataList();
    }
}
/***
 * callback for the xml meta data file
 * @param xml
 */
function readXML(xml){
    MYAPP.xml = xml;
    if(MYAPP.pattern !== null){
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


function popup(){
	jQuery(".popUp").fadeIn();
}
