
function _mod_breadcrumbs() {
    // private section - following fields and functions are private and need to be accessed by methods provided in the public section




    /****
     * create single bread crumbs
     *
     * @param nodeJQ node in the jstree (must be a jquery element)
     * @param isLeaf boolean if crumb is the last one in the list
     * @return {*}: breadcrumb
     */
    function createBreadCrumb(nodeJQ, isLeaf) {
        var cssClass = "";
        var icon = "";
        if (isLeaf) {
            cssClass = ' class = "breadCrumbLeaf" ';
        }
        else {
            cssClass = ' class = "breadCrumbInnerNode" ';
            icon = '<img src="' + MYAPP.menuIconPath +'193a-arrow-right.png" />';
        }
        return jQuery('<span ' + cssClass + '>' + nodeJQ.children("a").justtext() + icon + '</span> ');
    }




    // private section END


    // public section
    return {

        /****
         * delete the old bread crumb list
         * build the new bread crumb list
         *
         * @param nodeJQ node in the jstree (must be a jquery element)
         */
        updateBreadCrumbs : function (nodeJQ) {
        var stack = [];
        var i;

        //delete the old bread crumb list
        jQuery("#breadCrumbs").empty();

        // collect new bread crumbs
        stack.push(createBreadCrumb(nodeJQ, true));

        if (nodeJQ) {
            nodeJQ = MYAPP.tree._get_parent(nodeJQ);
            while (nodeJQ && nodeJQ !== -1) {
                stack.push(createBreadCrumb(nodeJQ, false));
                nodeJQ = MYAPP.tree._get_parent(nodeJQ);
            }
        }

        // print bread crumbs
        for (i = stack.length - 1; i >= 0; i--) {
            jQuery("#breadCrumbs").append(stack[i]);
        }
        //console.log(jQuery("#breadCrumbs").text());
    }
    };
    // public section END   (return end)
}
// Search Module End