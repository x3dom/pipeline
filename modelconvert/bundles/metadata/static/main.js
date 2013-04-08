var MYAPP = {}; // always put global Variables into some object like this or use better technics. This avoids errors.

function createMetaDataList(xmlData) {
	var element;
	var title;
	var content;
	
	//console.log(xmlData.toString());
	//console.log($(xmlData).text());

	$(xmlData).find("entry").each(function () {
		title = $(this).find("title").text();
		content = $(this).find("content").text();
		
		element = createMetaDataItem(title, content);
		jQuery('#metaDataList').append(element);
	});

	// the list has to be initialised, because we changed the DOM after jQuery did so
	jQuery('div[data-role=collapsible]').collapsible();
}

function createMetaDataItem(title, content) {
	var group;
	var header;
	var p;

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
		"data-theme" : "b",
		"class" : "metaDateEntry"
	});

	// create header
	header = jQuery('<h3/>').text(title);
	group.append(header);

	p = jQuery('<p >' + content + '</p>');
	group.append(p);

	return group;
}


function popup(){
	jQuery(".popUp").fadeIn();
}









// just for your infromation :)
function testConversion(){
	var myObj = {
		test: "bla"
	};
	var jqObj = jsObjToJqObj(myObj);
	var jsObj = jqObjToJsObj(jqObj);
	
	console.log(myObj.test);				// original JS Object
	console.log(jqObj.test);				// convertet JQuery Object -> fail (wrong access)
	console.log(jsObj.test);				// backword convertet JS Object
}
function jqObjToJsObj(jqObj){
	return jqObj[0];
}
function jsObjToJqObj(jqObj){
	return $(jqObj);
}

