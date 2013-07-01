var MYAPP = {};

/****
 * global configuration
 */
MYAPP.model = "conrod"; // "conrod"         // for the folder ind data containing the model and all its data
MYAPP.modelRootId = "modelRoot";                            // for the inline element
MYAPP.centerOfRotation = "1.2828279 152.4117 27.60026";     // set center of rotation
MYAPP.scaleAnnotMarker = 10;                             // set the size of annotation markers

MYAPP.sortTree = false;                                 // should the tre to be sorted alphabetically??

// target id's to insert the content of different modules
MYAPP.menuContainerID = "menuContainer";


MYAPP.isFlyToOnSelect = false;                         //
MYAPP.isHighlightOn = true;
MYAPP.x3dNodeHighlightColor = "#ffff55";

MYAPP.menuIconPath = "static/img/GlyphishIcons-Free/icons/";


// turn off ALL jQuery effects -> more efficient
//jQuery.fx.off = true;


/****
 * END configuration
 */

// modules to be used (global scope)
var mod_TabManager;
var mod_menu;
var mod_search;
var mod_breadcrumbs;
var mod_coordinateSystem;
var mod_HTMLTreeFromX3dTree;


/***************************************************************************
 * all the initialisation that dose not directly correspond to the model
 * is done here after the resources are loaded
 ***************************************************************************/

//!!!!!!!!!!!!!!!!!! not needed since the model is insert hardcoded !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
/*
jQuery(document).ready(function () {
	document.getElementById(MYAPP.modelRootId).setAttribute("url", '"static/data/' + MYAPP.model + '/model.x3d"');
	document.getElementById("ViewpointMain").setAttribute("centerOfRotation", MYAPP.centerOfRotation);
});
*/

// is executed when the model is compleatly loaded -> onload in index.html
function mainInit(){

    // get module instances

    mod_search              = _mod_search();
    mod_breadcrumbs         = _mod_breadcrumbs();
    mod_HTMLTreeFromX3dTree = _mod_HTMLTreeFromX3dTree();
    mod_TabManager          = _mod_TabManager();
    mod_menu                = _mod_menu();
    mod_coordinateSystem    = _mod_coordinateSystem();

    mod_coordinateSystem.init("CoordinateAxes__CoordinateAxes", "ViewpointMain");



    // set all the functions that need to be executed when an x3d element is clicked
    x3dTree.prepareX3dTree( [ htmlTree.highlightTree ] );

    // create HTML List that is used to create the jsTree
    mod_HTMLTreeFromX3dTree.createHTML_ListFromX3d(jQuery("#" + MYAPP.modelRootId), jQuery("#treeList"));

    //htmlTree.destroyTree();
    htmlTree.initTree();




	// set the top padding of the content container to the height of the header
	jQuery("#contentContainer").css("padding-top", jQuery(".ui-header").height() + "px");


	// module initialisation
	registerEventListenerMenu(mod_menu);
	mod_TabManager.init();

    console.log("vorher")
	jQuery.get("static/data/menu.txt", mod_menu.init, "json");

    console.log("fertig")


    /****************** set up Autocompleat searchfield *******************/
    mod_search.initSearch("tree_" + MYAPP.modelRootId, "searchFieldGraph");

    jQuery("#tree").find("li").each(function () {
        mod_search.pushTag(jQuery(this).attr("id"), htmlTree.getX3dIdFromTreeId(jQuery(this)).toLowerCase());
    });


};







/************************************************************
 * register event listener for menu *************************
 ************************************************************/
function registerEventListenerMenu(mod_menu) {
	/***** Buttons Debug ***********************************/
	mod_menu.pushEventListener("debug_switchPosition", function () {
		//mod_menu.switchPosition();
		mod_menu.setNextPosition();
	});
	mod_menu.pushEventListener("debug_open", function () {
		jQuery("#tree").jstree("open_all");
	});
	mod_menu.pushEventListener("debug_close", function () {
		jQuery("#tree").jstree("close_all");
	});
	mod_menu.pushEventListener("debug_switchTree", function () {
		switchViewTree("tree");
	});
	mod_menu.pushEventListener("debug_switchAccordion", function () {
		switchViewTree("accordion");
	});
	mod_menu.pushEventListener("debug_toggleStats",  function () {
		// not implemented jet
		//var statistics = document.getElementById('x3dElement').runtime.statistics();
		//document.getElementById('x3dElement').runtime.statistics(statistics);
	});



	/***** Buttons views ******************************/
	mod_menu.pushEventListener("view_next", function () {
		document.getElementById('x3dElement').runtime.nextView();
		document.getElementById('CoordinateAxes').runtime.nextView();
	});
	mod_menu.pushEventListener("view_pref", function () {
		document.getElementById('x3dElement').runtime.prevView();
		document.getElementById('CoordinateAxes').runtime.prevView();
	});
	mod_menu.pushEventListener("view_reset_cur", function () {
		document.getElementById('x3dElement').runtime.resetView();
		document.getElementById('CoordinateAxes').runtime.resetView();
	});
	mod_menu.pushEventListener("view_upright", function () {
		document.getElementById('x3dElement').runtime.uprightView();
	});
	mod_menu.pushEventListener("view_top", function () {
		document.getElementById('x3dElement').runtime.showAll('negY');
	});
	mod_menu.pushEventListener("view_bottom", function () {
		document.getElementById('x3dElement').runtime.showAll('posY');
	});
	mod_menu.pushEventListener("view_left", function () {
		document.getElementById('x3dElement').runtime.showAll('posX');
	});
	mod_menu.pushEventListener("view_right", function () {
		document.getElementById('x3dElement').runtime.showAll('negX');
	});
	mod_menu.pushEventListener("view_front", function () {
		document.getElementById('x3dElement').runtime.showAll('negZ');
	});
	mod_menu.pushEventListener("view_back", function () {
		document.getElementById('x3dElement').runtime.showAll('posZ');
	});


	/***** Buttons Visibility**************************/
	mod_menu.pushEventListener("visib_showAll", function () {
		MYAPP.tree.check_node(jQuery("#tree_" + MYAPP.modelRootId));
		MYAPP.tree.check_all();
	});
	mod_menu.pushEventListener("visib_hideAll", function () {
		MYAPP.tree.uncheck_node(jQuery("#tree_" + MYAPP.modelRootId));
	});
	mod_menu.pushEventListener("visib_faces", function () {
		x3dTree.renderVisibility('Point');
	});
	mod_menu.pushEventListener("visib_points", function () {
		x3dTree.renderVisibility('Face');
	});


	/***** Buttons Setting **************************/
	mod_menu.pushEventListener("toggleLockMenu", function (event, ui) {
		//alert(event)
		mod_menu.setMenuKeepOpen(jQuery(this).val());
	});


    mod_menu.pushEventListener("toggleStat", function () {
        var showStat = document.getElementById('x3dElement').runtime.statistics();
        //document.getElementById('x3dElement').runtime.statistics(!showStat);

        $("#x3dom-state-viewer").fadeToggle();
    });
    mod_menu.pushEventListener("toggleLog", function () {
        //document.getElementById('x3dElement').runtime.debug();
        $("#x3dom_logdiv").slideToggle();
    });

    /*
	mod_menu.pushEventListener("showObjOnSelect", function (event, ui) {
		var val = jQuery(this).val();
		if (val === true || val === "true") {
			MYAPP.isFlyToOnSelect = true;
		}
		else {
			MYAPP.isFlyToOnSelect = false;
		}
	});
	*/




	/***** Buttons Navigation Modes ******************* /
	 jQuery("#btn_examineMode").click(function(){
	 document.getElementById('x3dElement').runtime.examine() ;
	 return false;
	 });
	 jQuery("#btn_walkMode").click(function(){
	 document.getElementById('x3dElement').runtime.walk();
	 return false;
	 });
	 jQuery("#btn_lookAtMode").click(function(){
	 document.getElementById('x3dElement').runtime.lookAt();
	 return false;
	 });
	 jQuery("#btn_flyMode").click(function(){
	 document.getElementById('x3dElement').runtime.fly();
	 return false;
	 });
	 jQuery("#btn_gameMode").click(function(){
	 document.getElementById('x3dElement').runtime.game();
	 return false;
	 });

	 /***** Annotation Debug ***************************/



    /**** toggle buttons in header **********************/

    jQuery("#checkboxFlyTo").bind( "change", function(event, ui) {
        var val = $(this).is(':checked');
        if (val === "on" || val === true || val === "true") {
            MYAPP.isFlyToOnSelect = true;
        }
        else {
            MYAPP.isFlyToOnSelect = false;
        }
    });
    jQuery("#checkboxHighlight").bind( "change", function(event, ui) {
        var val = $(this).is(':checked');
        if (val === "on" || val === true || val === "true") {
            MYAPP.isHighlightOn = true;
        }
        else {
            MYAPP.isHighlightOn = false;
        }
    });
}













