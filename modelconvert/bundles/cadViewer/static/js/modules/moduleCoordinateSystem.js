/**
 * Created with JetBrains WebStorm.
 * User: Nils
 * Date: 22.06.13
 * Time: 16:15
 * To change this template use File | Settings | File Templates.
 */


/*********************************************************************
 **** Add a littel Coordinate System to tht Scene ********************
 **** and make it rotate when rotating the main model ****************
 **** note: the Coordinate System needs to be added manually *********
 ********************************************************************/



// todo: Rotation is routed from the main model to the coordinates, but not visa versa !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

function _mod_coordinateSystem() {

    /************************** private section ********************************/

    /***
     * delegate the rotation of the object to the coordinate arrows
     * @param evt the event that calls the function (connected to the viewpoint "ViewpointMain")
     */
    var viewFunc = function (evt) {
        var pos = evt.position;
        var rot = evt.orientation;
        var mat = evt.matrix;

        //document.getElementById('coordinateAxesViewpoint').setAttribute( 'position', pos.x+' '+pos.y+' '+pos.z);
        document.getElementById(evt.target.coordinateSystId).setAttribute('position', 0 + ' ' + 0 + ' ' + 0);
        document.getElementById(evt.target.coordinateSystId).setAttribute('rotation', rot[0].x + ' ' + rot[0].y + ' ' + rot[0].z + ' ' + rot[1]);

        //x3dom.debug.logInfo('position: ' + pos.x+' '+pos.y+' '+pos.z +'\n' + 'orientation: ' + rot[0].x+' '+rot[0].y+' '+rot[0].z+' '+rot[1]);
    };
    /************************** END private section ********************************/




    /********* public section ********/
    // all methods that give access to the private fields and allow to process the menu
    return {
        init : function (coordinateSystId, mainX3dContainerId) {
            // delegate rotation of the viewpoint to the coordinate axis
            var x3dContainer = document.getElementById(mainX3dContainerId);
            x3dContainer.addEventListener('viewpointChanged', viewFunc, false);
            x3dContainer.coordinateSystId = coordinateSystId;

        }
    };
// public section END   (return end)
}
// Search Module End