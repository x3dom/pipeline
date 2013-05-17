var MYAPP = {};

/****
 * global configuration
 */

// target id's to insert the content of different modules
MYAPP.menuContainerID = "menuContainer";
MYAPP.modelInput = "";

MYAPP.isFlyToOnSelect = false;

MYAPP.menuIconPath = "static/img/GlyphishIcons-Free/icons/";
MYAPP.renderOptionLast = "Face";

MYAPP.infoPopupOpen = null;

// modules to be used
var mod_menu;

/***************************************************************************
 * all the initialisation that dose not directly correspond to the model
 * is done here after the resources are loaded
 ***************************************************************************/
jQuery(document).ready(function () {
    $("#dropdown").bind("change", function (event, ui) {
        switchNavigationMode(event.target.value);
        switchTitle(event.target.value);
    });
    $("#btnInfo").bind("click", function (event, ui) {
        popUpShowObjInfo();
    });
    $("#btnFullscreen").bind("click", function (event, ui) {
        //$(document).fullScreen(true);
        $(document).toggleFullScreen();
    });


});


// is executed when the model is compleatly loaded -> onload in index.html
function mainInit(){
	//jQuery.mobile.changePage( "#objBrowser", { transition: "slideup"} );
	//jQuery.mobile.changePage( "#objBrowser" );

	// set the top padding of the content container to the height of the header
	jQuery("#contentContainer").css("padding-top", jQuery(".ui-header").height() + "px");

	// module registration &  initialisation
	mod_menu = modules("menu");
	registerEventListenerMenu(mod_menu);

	jQuery.get("static/data/menu.txt", mod_menu.init, "json");

};

/****
 * get module instances
 *
 * @param type string that specifies what kind of module is loaded
 * @return {*} a pointer to the module
 */
function modules(type) {
	if (type && type === "menu") {
		return _mod_menu();
	}
    if (type && type === "search") {
        return _mod_search();
    }
	return null;
}



function popUpShowObjInfo() {
    var content = [];
    content.push({
        "type" : "html",
        "html" : '<h1>Model: ' + MYAPP.modelInput + '</h1>'
    });
    /*
    <div class='group'>
        <h1>Model: {{ model.input }}</h1>
        <p>Output created with the <a href="http://github.com/x3dom/pipeline">Modelconvert</a> pipeline using <a href="http://instantreality.org">InstantReality</a> and <a href="http://meshlab.sourceforge.net/">MeshLab</a>.</p>
        <p>See <a href="list.html">all converted models</a>.</p>
    </div>

*/



    //jQuery().popUp("close");

    if(MYAPP.infoPopupOpen == null){
        var onClose = function(){
            MYAPP.infoPopupOpen = null;
        }
        MYAPP.infoPopupOpen = jQuery().popUp("new", { "content" : content, "onCloseEventListener": onClose});
    }
    else{
        jQuery().popUp("close", MYAPP.infoPopupOpen);
        MYAPP.infoPopupOpen = null;
    }

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
	});
	mod_menu.pushEventListener("view_pref", function () {
		document.getElementById('x3dElement').runtime.prevView();
	});
	mod_menu.pushEventListener("view_reset_cur", function () {
		document.getElementById('x3dElement').runtime.resetView();
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
        document.getElementById('scene').render = true;
    });
    mod_menu.pushEventListener("visib_hideAll", function () {
        document.getElementById('scene').render = false;
    });
    mod_menu.pushEventListener("visib_faces", function () {
        renderVisibility("Face");
    });
    mod_menu.pushEventListener("visib_points", function () {
        renderVisibility("Point");

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
}


/***************************
 * X3DOM Functions
 *********************************/
// render Points or Faces
function renderVisibility(option) {
    if (option === "Point" && MYAPP.renderOptionLast !== "Point") {
        document.getElementById('x3dElement').runtime.togglePoints();
        MYAPP.renderOptionLast = "Point";
    }
    else if (option === "Face" && MYAPP.renderOptionLast !== "Face") {
        document.getElementById('x3dElement').runtime.togglePoints();
        MYAPP.renderOptionLast = "Face";
    }
}


function switchNavigationMode(mode) {
    if (mode !== undefined) {
        var e = document.getElementById("x3dElement");
        if (mode === "examine" ) {
            e.runtime.examine();
        }
        else if (mode === "lookat" ) {
            e.runtime.lookAt();
        }
        else if (mode === "walk" ) {
            e.runtime.walk();
        }
        else if (mode === "fly" ) {
            e.runtime.fly();
        }
        else if (mode === "helicopter" ) {
            e.runtime.helicopter();
        }
        else if (mode === "none" ) {
            e.runtime.noNav();
        }
    }
}
function switchTitle(mode) {
    if (mode !== undefined) {
        var title = $("#headerTitle");
        if (mode === "examine" ) {
            title.text("Examine");
        }
        else if (mode === "lookat" ) {
            title.text("Look At");
        }
        else if (mode === "walk" ) {
            title.text("Walk Through");
        }
        else if (mode === "fly" ) {
            title.text("Fly");
        }
        else if (mode === "helicopter" ) {
            title.text("Helicopter");
        }
        else if (mode === "none" ) {
            title.text("None");
        }
    }
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
