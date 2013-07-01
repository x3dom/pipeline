

function _mod_HTMLTreeFromX3dTree() {
    "use strict";
    // private section - following fields and functions are private and need to be accessed by methods provided in the public section


    /****
     * create the HTML List from the x3d model -> this list is used to create the jsTree
     * the List is created recursively starting at the first x3dNodeJQ node.
     *
     * @param x3dNodeJQ x3d node that supplies the id to create the new element in the tree (submitted as a jQuery element)
     * @param parentJQ element in the tree that becomes the parent of the new node (submitted as a jQuery element)
     */
    function initHTML_List(x3dNodeJQ, parentJQ) {
        // console.log(x3dNodeJQ.children().length + " - " + x3dNodeJQ.attr("id"))
        var isLeaf;
        if (x3dNodeJQ.children().size() > 0) { // inner node
            if (x3dTree.isx3dNodeGoodForTree(x3dNodeJQ[0])) {
                isLeaf = x3dTree.isX3dNodeLeaf(x3dNodeJQ[0]);

                parentJQ = addNodeToTree(parentJQ, x3dNodeJQ, isLeaf);
            }
            x3dNodeJQ.children().each(function () {             // recursive colling of the function to add the nodes to the tree
                initHTML_List(jQuery(this), parentJQ);		// kid and new node (as new parentJQ)
            });
        }
    }

    /****
     * add a node to the tree
     *
     * @param parentJQ element in the tree that becomes the parent of the new node (submitted as a jQuery element)
     * @param x3dNodeJQ x3d node that supplies the id to create the new element in the tree (submitted as a jQuery element)
     * @param isLeaf boolean -> to set the icons correct and if false create a child list to add more children
     * @return {*} new node or the list for more children
     */
    //  todo: WARNING: the reference to the x3d node is saved multiple times. this is redundant, but I dont know at the moment how it will be used !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    function addNodeToTree(parentJQ, x3dNodeJQ, isLeaf) {
        //console.log(x3dNodeJQ.attr("id"))
        // check if the id of the x3d node is usable as a title for the tree node
        var key = x3dNodeJQ.attr("id");
        if (key === "") {
            alert("Wrong Format -> no ID set for Element " + x3dNodeJQ);
        }
        var title = key;
        // check if the node is an textnode, if yes take the text as the node name
        if (x3dNodeJQ.prop("nodeName") === "#text") {
            title = x3dNodeJQ.prop("nodeValue") + " ** ID: " + title;
        }
        title = title.replace("inline__", "");


        /* add node as HTML */
        var node = document.createElement("li");
        node.setAttribute("id", "tree_" + key);
        node.x3dNode = x3dNodeJQ[0];
        //node.setAttribute("class", "checked");

        var a = document.createElement("a");
        a.setAttribute("href", "#");

        a.x3dNode = x3dNodeJQ[0];
        a.addEventListener('click', highlightX3DNode, false);

        a.appendChild(document.createTextNode(title));

        node.appendChild(a);

        parentJQ.append(node);


        if (isLeaf) {               // if leaf set icon
            node.setAttribute("rel", "shapeLeaf");
        }
        else {                      // else create a new list for more children
            var ul = document.createElement("ul");
            node.appendChild(ul);
            parentJQ = jQuery(ul);
        }


        return parentJQ;
    }



    function highlightX3DNode(){
        x3dTree.highlightX3dNode(this.x3dNode);

        jQuery(".activeNode").removeClass("activeNode");
        jQuery(this).addClass("activeNode");
    }

    function renderX3dNode(){
        //x3dTree.setX3dRender(render , this.x3dNode);

        var li = jQuery(this).closest("li");
        var liParents = li.parents(".checked");
        //console.log(liParents[liParents.length-1])

        var hasUncheckedParent = li.parents(".unchecked");

        if(!hasUncheckedParent){
            //console.log("show")
            x3dTree.setX3dRenderShow(this.x3dNode)
        }
        else{
            //console.log("hide")
            x3dTree.setX3dRenderHide(this.x3dNode);
        }
    }
    // private section END





    // public section
    // all methods that give access to the private fields and allow to process the menu
    return {
        createHTML_ListFromX3d : function(x3dNodeJQ, parentJQ) {
            initHTML_List(x3dNodeJQ, parentJQ);
        }
    };
    // public section END   (return end)
}
// Search Module End










