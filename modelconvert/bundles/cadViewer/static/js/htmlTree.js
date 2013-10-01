/*global MYAPP, jQuery */  /* for jsLint */


var htmlTree = function () {


	/************************** private section ********************************/
	/****
	 * init part for jquery mobile -> mainly style / css stuff and event stuff
	 */
	function jstreeJqmInit() {
		"use strict";

		jQuery("#treeList").addClass("ui-listview ui-listview-inset ui-corner-all");
		jQuery("#treeList li:first").addClass("first");
		jQuery("#tree li").each(function () {
			jQuery(this).addClass("ui-btn ui-btn-icon-right ui-li-has-arrow ui-li ui-li-has-count ui-corner-all ui-li ui-btn-up-c");
			jQuery(this).find("a").addClass("ui-corner-all");

			// hover for li elements
			jQuery(this).hover(
				function () {   // mouse in
					jQuery(this).removeClass("ui-btn-up-c ui-btn-down-c").addClass("ui-btn-hover-c");
				},
				function () {   // mouse out
					jQuery(this).removeClass("ui-btn-hover-c ui-btn-down-c").addClass("ui-btn-up-c");
				}
			);
			// hover for links
			jQuery(this).find("a").hover(
				function () {   // mouse in
					jQuery(this).addClass("ui-focus");
				},
				function () {   // mouse out
					jQuery(this).removeClass("ui-focus");
				}
			);


			if (!jQuery(this).hasClass("jstree-leaf")) {
				var childCnt = jQuery(this).children("ul").children("li").size();
				var counter = document.createElement("span");
				counter.setAttribute("class", "ui-li-count ui-btn-up-c ui-btn-corner-all ");
				counter.appendChild(document.createTextNode(childCnt));
				jQuery(this).children("a").append(counter);
			}
		});

	}







	/*******************************************************************
	 ******* tree modes (accordion behavior) ****************************
	 ********************************************************************/
	/****
	 * set up the modes for the tree
	 * 1. mode: normal explorer tree view
	 * 2. mode: accordion navigation
	 */
	function initTreeModes() {
		"use strict";
		MYAPP.treeMode = {};
		MYAPP.treeMode.accordion = {};		// "accordion"
		MYAPP.treeMode.tree = {};		    // "tree"

		// set tree view mode to the value of the toggle slider
		MYAPP.currentTreeMode = jQuery("#switchViewTreeSlider").val();

		/******* manipulate tree behavier and apperance (MODES) ****************
		 * there are 3 restrictions for the whanted behavieor
		 *
		 * when node x is clicked:
		 * 1.) node is opend (== childs visible) and all childs have to be closed (== childs childs are hidden)
		 * 2.) all siblings need to be opend
		 * 3.) all direct parents need to be opend but cant have any other brunches opend
		 *
		 ****************************************************************/

		MYAPP.treeMode.accordion.onSelect = function (node) {
			// 1. and 2. restirction
			MYAPP.tree.open_node(node);
			if (!MYAPP.tree.is_leaf(node)) {
				switchTreeModeChildren(node, effects.show);
				switchTreeModeSiblings(node, effects.hide);
			}
			// 3.) restirction
			switchTreeModeParents(node);
		};
		MYAPP.treeMode.tree.onSelect = function (node) {
			MYAPP.tree.toggle_node(node);
		};
		htmlTree.switchTreeMode(MYAPP.currentTreeMode);
        console.log("test")
	}

	/****
	 * shows child nodes and closes them === hides the children (of current node current)
	 *
	 * @param node jsTree node
	 * @param effect function that is stored in effects
	 */
	function switchTreeModeChildren(node, effect) {
		"use strict";
		if (node && effect) {
			var children = MYAPP.tree._get_children(node);
			jQuery(children).each(function () {
				effect(jQuery(this));
				MYAPP.tree.close_node(jQuery(this));
			});
		}
	}

	/****
	 * hides and shows sibbling nodes (of current node current)
	 *
	 * @param node jsTree node
	 * @param effect function that is stored in effects
	 */
	function switchTreeModeSiblings(node, effect) {
		"use strict";

		if (node && effect) {
			var prev = MYAPP.tree._get_prev(node, true);
			while (prev) {
				effect(prev);
				prev = MYAPP.tree._get_prev(prev, true);
			}
			var next = MYAPP.tree._get_next(node, true);
			while (next) {
				effect(next);
				next = MYAPP.tree._get_next(next, true);
			}
		}
	}

	/*****
	 * shows all parents and hides their siblings
	 * @param node jsTree node
	 */
	function switchTreeModeParents(node) {
		"use strict";

		if (node) {
			var parent = MYAPP.tree._get_parent(node);
			while (parent && parent !== -1) {
				effects.show(parent);
				switchTreeModeSiblings(parent, effects.hide);
				parent = MYAPP.tree._get_parent(parent);
			}
		}
	}

	// holds different effects to show and hide elements such as li items
    // - currently they dont have any effect. To speed up things, all effects are turned off
    //   in main.js with the line: jQuery.fx.off = true;
	var effects = {
		hide : function (node) {
			"use strict";
			//node.stop().slideUp();
			node.stop().hide();
		},
		show : function (node) {
			"use strict";
			//node.stop().slideDown();
			node.stop().show();
		},
		toggle : function (node) {
			"use strict";
			if (node.is(':hidden')) {
				effects.show(node);
			}
			else {
				effects.hide(node);		// warum geht hier this nicht??????????????????
			}
		}
	};

    /****
     * convert an jstree id to the corresponding id in the x3d tree
     */
    function getX3dIdFromTreeId (nodeJQ) {
        return nodeJQ.attr("id").replace("tree_", "");
    }
	/*******************************************************************
	 ******* END tree modes (accordion behavior) ***********************
	 *******************************************************************/







	/************************** END private section ********************************/




	/********* public section ********/
	/****
	 * init the tree
	 * create the html list, init jsTree and set up events and settings
	 */
    this.initTree = function () {
		var tree = jQuery("#tree");

		//var plugins = [ "cookies" ];  // good if the state of the tree (opened and closed leafs should be saved)
		var plugins = [ "themes", "html_data", "checkbox", "ui", "types" ];
		if (MYAPP.sortTree) {
			plugins.push("sort");
		}

		// init the jsTree
		tree.jstree({
			"core" : {
                "initially_open" : [ "root" ],
                "animation" : 0
            },
			"themes" : {
				"theme" : "default", // !!! todo: i modefied this because i was not able to set up a new theme :(
				"dots" : true,
				"icons" : true
			},
			"types" : {
				"valid_children" : [ "shapeLeaf" ],
				"types" : {
					"shapeLeaf" : {
						"icon" : {
							//"image" : "/img/menu/icons.gif",
							"position" : "-74px -36px"
						},
						"valid_children" : [ "none" ]
					},
					"default" : {
						"icon" : {
							//"image" : "/img/menu/icons.gif",
							"position" : "-56px -36px"
						},
						"valid_children" : [ "default" ]
					}
				}
			},
			"plugins" : plugins
		});


		MYAPP.tree = jQuery.jstree._reference("#tree");

		initTreeModes();

		// add events

		/*
		 // click and double click dont provide the fields data.rslt.obj, data.inst. thatfore it is more difficult to get the clicked node
		 tree.bind("click.jstree", function (event, data) {
             //console.log("Bind Result: " + event.type);
             var node = jQuery(event.target).closest("li");
		 });
		 */

		tree.bind("dblclick.jstree", function (event) {
			//console.log("Bind Result: " + event.type);
			var nodeJQ = jQuery(event.target).closest("li");

            // toggles the check status of jstree nodes (checkboxes == eye)
            if (MYAPP.tree.is_checked(nodeJQ)) {
                MYAPP.tree.uncheck_node(nodeJQ);
            }
            else {
                MYAPP.tree.check_node(nodeJQ);
            }
		});

		/*
		 * is called every time one clicks on a list entry
		 * it has to process the selection function and execute the deselect function
		 *
		 * for some reason the deselect event is called, but dosnt show the whanted effect.
		 * it would be perfect if the behavieor would be like:
		 * - click on a link -> entry is selected
		 *                   -> AND last selected entry is deselected
		 *                   -> AND deselected event for it is executed
		 * I "fake" the behavier by using the selected event as usally
		 * and also remember the last selection. this enables me to call the deactivate function
		 * which is equal to the deselect event callback (as it should be).
		 */
		tree.bind("select_node.jstree", function (event, data) {
			//console.log("Bind Result: SELECTED ");
			var node = data.rslt.obj;
			//var tree = data.inst;
			//console.log(tree.get_text(data.rslt.obj) + " - " + data.rslt.obj.attr("id")); // ID - Text

			// make shure that the last node is deselected
			MYAPP.tree.deselect_node(MYAPP.lastNodeSelection); // fire deselect event
			deactivate(MYAPP.lastNodeSelection);
			MYAPP.lastNodeSelection = node;

			jQuery(node).addClass("activeNode");

			MYAPP.treeMode[MYAPP.currentTreeMode].onSelect(node);

			//highlight x3d element
			var id = getX3dIdFromTreeId(node);
			//alert(id);
            if(MYAPP.isHighlightOn){
                document.getElementById(id).highlight(true, MYAPP.x3dNodeHighlightColor);
            }
			if (MYAPP.isFlyToOnSelect) {
				document.getElementById('x3dElement').runtime.showObject(document.getElementById(id));
			}

            mod_breadcrumbs.updateBreadCrumbs(data.rslt.obj);
		});

		tree.bind("deselect_node.jstree", function (event, data) {
			//console.log("Bind Result: DE - SELECTED ");
			var node = data.rslt.obj;
			//var tree = data.inst;
			deactivate(node);
		});
		function deactivate(node) {
			if (node) {
				// de-highlight x3d element
				document.getElementById(getX3dIdFromTreeId(node)).highlight(false, MYAPP.x3dNodeHighlightColor);
				jQuery(node).removeClass("activeNode");
			}
		}


		tree.bind("check_node.jstree", function (event, data) {
			//console.log("Bind Result: " + event.type + " - checked: " + data.inst.is_checked(data.rslt.obj));

            // show a node in the x3d scene graph by setting its render flag to true
            var id = getX3dIdFromTreeId(data.rslt.obj);
            x3dTree.setX3dRenderShow(document.getElementById(id));
		});

		tree.bind("uncheck_node.jstree", function (event, data) {
			//console.log("Bind Result: " + event.type + " - unchecked: " + data.inst.is_checked(data.rslt.obj));

            //hide a node in the x3d scene graph by setting its render flag to false
            var id = getX3dIdFromTreeId(data.rslt.obj);
            //x3dTree.setX3dRender(false, id);
            x3dTree.setX3dRenderHide(document.getElementById(id));
		});

		jQuery("#switchViewTreeSlider").bind("change", function () {
			htmlTree.switchTreeMode(jQuery(this).val());
		});


		tree.bind("loaded.jstree", function () {
			jQuery('#tree ul:first').attr("id", "treeList");
			MYAPP.tree.check_all();
			jstreeJqmInit();
		});

	};

	/****
	 * switch the tree view between accordion and tree
	 * @param mode string that holds the mode -> at the moment "tree" or "accordion"
	 */
    this.switchTreeMode = function (mode) {
		"use strict";

		if (mode === "accordion") {
			MYAPP.currentTreeMode = "accordion";
			jQuery("#tree").removeClass("treeContainer").addClass("accordionView");
			MYAPP.treeMode.accordion.onSelect(MYAPP.lastNodeSelection);
		}
		else if (mode === "tree") {
			MYAPP.currentTreeMode = "tree";
			jQuery("#tree").removeClass("accordionView").addClass("treeContainer");
			// make shure that all nodes are visible (accordionView hides some)
			jQuery("#tree").find("li").show();
		}
	};




	/****
	 * select a node in the tree when clicking an x3d node in the scene graph.
	 * the selected jstree node will be highlighted
	 * @param event click event from x3DOM
	 */
    this.highlightTree = function (event) {
		"use strict";
		var id = event.hitObject._x3domNode._xmlNode.getAttribute("id");
		var node = document.getElementById("tree_" + id);
		//console.log("highlightTree  " + id)
		MYAPP.tree.select_node(node);
	};

	/****
	 * destroy the jstree
	 */
    this.destroyTree = function () {
		jQuery("#treeList").empty();

		try {
			jQuery.jstree._reference("#tree").destroy();
			$("#tree").jstree('destroy');
			//$("#tree").jstree("destroy");
			//$("#treeList").remove();
			console.log("tree is destroyed.")
		}
		catch (e) {
			console.log("tree could not be destroyed. It might not be created jet.")
		}
    };


    /****
     * convert an jstree id to the corresponding id in the x3d tree
     */
    this.getX3dIdFromTreeId = function (nodeJQ) {
        return nodeJQ.attr("id").replace("tree_", "");
    }


    return this;
}();