var MYAPP = {};

/****
 * global configuration
 */
MYAPP.model = "conrod"; //"engine3" "conrod" "test"         // for the folder ind data containing the model and all its data
MYAPP.modelRootId = "modelRoot";                            // for the inline element

MYAPP.sortTree = false;                                 // should the tre to be sorted alphabetically??

// target id's to insert the content of different modules
MYAPP.menuContainerID = "menuContainer";


MYAPP.isFlyToOnSelect = false;
MYAPP.x3dNodeHighlightColor = "#ffff55";

MYAPP.menuIconPath = "static/img/GlyphishIcons-Free/icons/";

/****
 * END configuration
 */

// modules to be used
var mod_TabManager;
var mod_menu;


/***************************************************************************
 * all the initialisation that dose not directly correspond to the model
 * is done here after the resources are loaded
 ***************************************************************************/
jQuery(document).ready(function () {

});



// is executed when the model is compleatly loaded -> onload in index.html
function mainInit(){
    mod_sceneGraph.initSceneGraph();

    //jQuery.mobile.changePage( "#objBrowser", { transition: "slideup"} );
    //jQuery.mobile.changePage( "#objBrowser" );

    // set the top padding of the content container to the height of the header
    jQuery("#contentContainer").css("padding-top", jQuery(".ui-header").height() + "px");

    // module registration
    mod_menu = modules("menu");
    mod_TabManager = modules("tabManager");

    // module initialisation
    jQuery.get("static/data/menu.txt", mod_menu.init, "json");
    registerEventListenerMenu(mod_menu);
    mod_TabManager.init();
};

/****
 * get module instances
 * tree and sceneGraph are processed separately
 *
 * @param type string that specifies what kind of module is loaded
 * @return {*} a pointer to the module
 */
function modules(type) {
	if (type && type === "search") {
		return _mod_search();
	}
	if (type && type === "tabManager") {
		return _mod_TabManager();
	}
	if (type && type === "menu") {
		return _mod_menu();
	}
	return null;
}


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
		mod_sceneGraph.renderVisibility('Point');
	});
	mod_menu.pushEventListener("visib_points", function () {
		mod_sceneGraph.renderVisibility('Face');
	});



	/***** Buttons Setting **************************/
	mod_menu.pushEventListener("toggleLockMenu", function (event, ui) {
		//alert(event)
		mod_menu.setMenuKeepOpen(jQuery(this).val());
	});
	mod_menu.pushEventListener("showObjOnSelect", function (event, ui) {
		var val = jQuery(this).val();
		if (val === true || val === "true") {
			MYAPP.isFlyToOnSelect = true;
		}
		else {
			MYAPP.isFlyToOnSelect = false;
		}
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


	/***** Buttons Navigation Modes *******************/
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

}


/*****************************************
 * JQuery plugin
 *
 * makes it possible to just select the text of an element but
 * no child elements content
 *
 * http://viralpatel.net/blogs/2011/02/jquery-get-text-element-without-child-element.html
 **************************************/
jQuery.fn.justtext = function () {
	return $(this).clone()
		.children()
		.remove()
		.end()
		.text();
};

/*
 * it provides functions that are described in the book "JavaScript the Good Parts"
 * This functions and techniques are very helpful to write good and clean code!!!
 *
 * Module that hides all its variables in closures (private variables)
 */
var jsGoodParts = (function () {
	"use strict";
	return {
		init : function () {
			Function.prototype.method = function (name, func) {
				if (!this.prototype[name]) {
					this.prototype[name] = func;
					return this;
				}
			};
			Number.method("integer", function () {
				return Math[this < 0 ? 'ceil' : 'floor'](this);
			});
			String.method("trim", function () {
				return this.replace(/^\s+|\s+$/g, '');
			});
		},

		/*
		 * checks if the argument is an Object
		 * Objects can be real Objects or Arrays
		 */
		isObject : function (obj) {
			if (obj && typeof obj === 'object') {
				return true;
			}
			return false;
		},
		/*
		 * checks if the argument is an Object
		 * This function excludes Arrays!
		 */
		isRealObject : function (obj) {
			if (obj && typeof obj === 'object' && !this.isArray(obj)) {
				return true;
			}
			return false;
		},
		/*
		 * checks if the argument is an Array
		 * This function excludes Objects!
		 */
		isArray : function (obj) {
			if (obj && typeof obj === 'object' && typeof obj.length === 'number' && !(obj.propertyIsEnumerable('length'))) {
				return true;
			}
			return false;
		}
	};
}());
