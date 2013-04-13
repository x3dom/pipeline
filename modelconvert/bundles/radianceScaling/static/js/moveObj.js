// the x3dom runtime object
var runtime = null;

var sunSphere = null;
var sunLight = null;
var drag = false;

var w = 0, h = 0;
var uPlane, vPlane, pPlane;

var isect = null;
var translationOffset = null;

var firstRay = null;
var lastX = 0, lastY = 0;
var buttonState = 0;


// get plane parallel to viewing plane through point 'origin'
function calcViewPlane(origin)
{
    var ray = null;

    // init width and height
    w = runtime.getWidth();
    h = runtime.getHeight();

    ray = runtime.getViewingRay(0, h-1);
    var r = ray.pos.add(ray.dir);   //bottom left of viewarea

    ray = runtime.getViewingRay(w-1, h-1);
    var s = ray.pos.add(ray.dir);   //bottom right of viewarea

    ray = runtime.getViewingRay(0, 0);
    var t = ray.pos.add(ray.dir);   //top left of viewarea

    uPlane = s.subtract(r).normalize();
    vPlane = t.subtract(r).normalize();

    if (arguments.length === 0)
        pPlane = r;
    else
        pPlane = x3dom.fields.SFVec3f.copy(origin);
}

// helper to calc determinant
function det(mat)
{
    return 	mat[0][0]*mat[1][1]*mat[2][2] + mat[0][1]*mat[1][2]*mat[2][0] +
        mat[0][2]*mat[2][1]*mat[1][0] - mat[2][0]*mat[1][1]*mat[0][2] -
        mat[0][0]*mat[2][1]*mat[1][2] - mat[1][0]*mat[0][1]*mat[2][2] ;
}

// translation along plane parallel to viewing plane E:x=p+t*u+s*v
function translateXY(l)
{
    var track = null;
    var z = [], n = [];

    for (var i=0; i<3; i++) {
        z[i] = [];
        n[i] = [];

        z[i][0] = uPlane.at(i);
        n[i][0] = z[i][0];

        z[i][1] = vPlane.at(i);
        n[i][1] = z[i][1]

        z[i][2] = (l.pos.subtract(pPlane)).at(i);
        n[i][2] = -l.dir.at(i);
    }

    // get intersection line-plane with cramer's rule
    var s = det(n);

    if (s !== 0) {
        var t = det(z) / s;
        track = l.pos.addScaled(l.dir, t);
    }

    if (track) {
        if (isect) {
            // calc offset from first click position
            track = track.subtract(isect);
        }
        track = track.add(translationOffset);
    }

    return track;
}

// translation along picking ray to zoom object in/out
function translateZ(l, currY)
{
    var vol = runtime.getSceneBBox();
    var sign = (currY < lastY) ? 1 : -1;
    var fact = sign * (vol.max.subtract(vol.min)).length() / 50;

    translationOffset.setValues(translationOffset.addScaled(l.dir, fact));

    return translationOffset;
}

function over(event)
{
    runtime.getCanvas().style.cursor = "crosshair";
}

function out(event)
{
    if (!drag)
        runtime.getCanvas().style.cursor = "pointer";
}

// on button press
function start(event)
{
    if (!drag)
    {
        lastX = event.layerX;
        lastY = event.layerY;

        drag = true;
        runtime.noNav();    // disable navigation

        // calc view-aligned plane through original pick position
        isect = new x3dom.fields.SFVec3f(event.worldX, event.worldY, event.worldZ);
        calcViewPlane(isect);

        firstRay = runtime.getViewingRay(event.layerX, event.layerY);
        // to distinguish between parallel or orthogonal movement
        buttonState = event.button;

        var mTrans = sunSphere.getAttribute("translation");
        if (mTrans)
            translationOffset = x3dom.fields.SFVec3f.parse(mTrans);
        else
            translationOffset = new x3dom.fields.SFVec3f(0, 0, 0);

        runtime.getCanvas().style.cursor = "crosshair";
    }
}

// on mouse move
function move(event)
{
    if (drag)
    {
        var pos = runtime.mousePosition(event);
        var ray = runtime.getViewingRay(pos[0], pos[1]);

        var track = null;

        if (buttonState == 2)   // right mouse button
            track = translateZ(firstRay, pos[1]);
        else
            track = translateXY(ray);

        if (track){
            sunSphere.setAttribute("translation", track.x + " " + track.y + " " + track.z);
            sunLight.setAttribute("location", track.x + " " + track.y + " " + track.z);
            console.log("sphere: " + sunSphere.getAttribute("translation") + "\n Licht: " + sunLight.getAttribute("translation"));
        }

        lastX = pos[0];
        lastY = pos[1];
    }
}

// on button release
function stop(event)
{
    if (drag)
    {
        lastX = event.layerX;
        lastY = event.layerY;

        isect = null;
        drag = false;
        runtime.examine();    // enable navigation

        runtime.getCanvas().style.cursor = "pointer";
    }
}

// some inits to attach listeners etc.
document.onload = function()
{
    var boxes = document.getElementById("x3dMain");
    runtime = boxes.runtime;
    boxes.addEventListener('mouseup', stop, false);
    boxes.addEventListener('mouseout', stop, false);
    boxes.addEventListener('mousemove', move, true);

    sunLight = document.getElementById("sunLight");

    sunSphere = document.getElementById("sun");
    sunSphere.addEventListener('mousedown', start, false);
    sunSphere.addEventListener('mouseover', over, false);
    sunSphere.addEventListener('mouseout', out, false);
}
