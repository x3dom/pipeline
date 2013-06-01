var MYAPP = {};
MYAPP.toggleDebug = false;
MYAPP.runtime     = null;
MYAPP.path        = {};
MYAPP.path.shader = "static/shader/";


var mod_ColorPicker;
var mod_Menu;
var mod_MoveObj;

MYAPP.lastW = 1024;
MYAPP.lastH = 1024;
MYAPP.inlineLoaded = false;


jQuery(document).ready(function () {
    mod_ColorPicker = mod_colorPicker();
    mod_ColorPicker.init();

    mod_Menu = mod_menu();
    mod_Menu.init();


});

function initInline() {
    //MYAPP.path.shader = getRelativeShaderPath();
    MYAPP.runtime = document.getElementById("x3dMain").runtime;

    MYAPP.runtime.exitFrame = function()
    {
        if (!MYAPP.inlineLoaded)
        {
            setUpLightAndCam();
            modifyX3DModel();
            createMenu();

            MYAPP.inlineLoaded = true;
        }

        var w = +MYAPP.runtime.getWidth();
        var h = +MYAPP.runtime.getHeight();

        if (w != MYAPP.lastW || h != MYAPP.lastH)
        {
            var rt = document.getElementById('test');
            rt.setAttribute('dimensions',  w + ' ' + h + ' 4');

            MYAPP.lastW = w;
            MYAPP.lastH = h;
        }
    };
}

function setUpLightAndCam() {
   // set inline Cam
   var inlineVP = document.getElementById("inline__" + getCamDEF());
   var oldVP = document.getElementById("vp");

   oldVP.setAttribute("position", inlineVP.getAttribute("position"));
   oldVP.setAttribute("centerOfRotation", inlineVP.getAttribute("centerOfRotation"));
   oldVP.setAttribute("fieldOfView", inlineVP.getAttribute("fieldOfView"));
   oldVP.setAttribute("orientation", inlineVP.getAttribute("orientation"));

   // position Light
   var bBox = MYAPP.runtime.getSceneBBox();
   var center = (bBox.min.add(bBox.max)).multiply(0.5);
   var bBoxSize = bBox.max.subtract(bBox.min);
   var m = MYAPP.runtime.viewMatrix();
   var up = m.e1();
   var forw = m.e2().multiply(-1.0);
   var cross = up.cross(forw).multiply(-1.0);
   var lightOffset = up.add(cross).normalize().multComponents(bBoxSize);
   var newLightPos = center.add(lightOffset);

   var bBoxMaxLength = (bBoxSize.x < bBoxSize.y ? bBoxSize.y : bBoxSize.x);
   bBoxMaxLength = (bBoxMaxLength < bBoxSize.z ? bBoxSize.z : bBoxMaxLength);
   var newSunSize = bBoxMaxLength * 0.05;

   document.getElementById("sunLight").setAttribute("location", newLightPos.x + " " + newLightPos.y + " " + newLightPos.z);
   document.getElementById("sun").setAttribute("translation", newLightPos.x + " " + newLightPos.y + " " + newLightPos.z);
   document.getElementById("sun").setAttribute("scale", newSunSize + " " + newSunSize + " " + newSunSize);
}


/***
 * When switching a x3d model the scene must be "convertet" so that the Radiance Scaling Shader works.
 * Therefor it is necessary to rewrite the appearance of the fist shape node
 */
function modifyX3DModel() {
    var app = getFirstAppearance();
    renewAppRadianceScaling(app);

    //console.log(($("#x3DomInline").find('Shape'))[1]);  // shape 1 (id 2)
    //console.log(($("#x3DomInline"))[0]);  // shape 1 (id 2)
}



/***
 * replace the entire content of a Appearance node with the stuff that is needed for Radiance Scaling
 * @param app: Appearance to be replaced
 * @param shapes: Shapes that are necessary for the Rendered Texture of the new Radiance Scaling Appearance
 */
function renewAppRadianceScaling(app){
    var rt = jQuery('                                                                                                   \
        <RenderedTexture id="test" DEF="fieldRenderedTex" update="ALWAYS" dimensions="1024 1024 4" repeatS="false" repeatT="false" showNormals="true">    \
            <Viewpoint USE="scene__vp" containerField="viewpoint"></Viewpoint>                                          \
            <Transform USE="scene__sunGeo" containerField="excludeNodes"></Transform>                                   \
        </RenderedTexture>                                                                                              \
    ');

    var cs = jQuery('<ComposedShader DEF="ComposedShader"> </ComposedShader> ');
    cs.append(jQuery('                                                                                                  \
         <field id="fieldSpecularPower" name="fieldSpecularPower" type="SFFloat" value="1.0"></field>                   \
         <field id="fieldAlpha" name="fieldAlpha" type="SFFloat" value="0"></field>                                     \
         <field id="fieldGamma" name="fieldGamma" type="SFFloat" value="0"></field>                                     \
         <field name="tex" type="SFInt32" value="0"></field>                                               \
                                                                                                                        \
         <ShaderPart type="VERTEX" url="' + MYAPP.path.shader + 'radianceScalingMainVertexShader.glsl"> </ShaderPart>   \
         <ShaderPart type="FRAGMENT" url="' + MYAPP.path.shader +'radianceScalingMainFragmentShader.glsl"> </ShaderPart>\
    '));

    //<ShaderPart type="VERTEX" url="' + MYAPP.path.shader + 'vs.glsl"> </ShaderPart>   \
    //     <ShaderPart type="FRAGMENT" url="' + MYAPP.path.shader +'vs.glsl"> </ShaderPart>\
    //console.log((rt)[0] );
    //console.log((cs)[0]);

    app.empty();
    app.append(rt);
    app.append(cs);
}


function getFirstAppearance() {
    var inline = $("#x3DomInline");
    var shapes = inline.find('Shape');
    return shapes.first().find("Appearance");
}


function getRelativeShaderPath(){
    var url = $("#x3DomInline").attr("url");
    var urlDepth = url.match(/\//g).length;
    var shaderPath = "";
    for(var i=0; i<urlDepth-1; i++){
        shaderPath += "../";
    }
    shaderPath += "shader/";
    //console.log("url: " + url);
    //console.log("url: " + urlDepth);
    //console.log("url: " + shaderPath);
    return shaderPath;
}


function createMenu(){
/*
    mod_Menu.addButton($("#menuList"), "Toggle debug", toggleDebug);
    mod_Menu.addButton($("#menuList"), "Back", function () {
        window.location = "index.html";
    });
    mod_Menu.addButton($("#menuList"), "switch Model", function () {
        //switchX3DomModel(MYAPP.model.birth);
    });
  */
    mod_Menu.addSlider($("#menuList"), "fieldGamma", "value", "Gamma (strength -> 0 = no scaling)", true, 400);
    mod_Menu.addSlider($("#menuList"), "fieldAlpha", "value", "Alpha (direction -> 0.5 = neutral)", true);

    mod_Menu.addButton($("#menuList"), "Light color", function () {
        mod_ColorPicker.open("sun", "color");       // if "sun" is used as first argument,
                    // the light source needs to be named with "sunLight" and
                    // the material of the Sphere to visualize it must contain a Material nemed "sunMat"
    });

    mod_Menu.addSlider($("#menuList"), "sunLight", "ambientIntensity", "Ambient Intensity", true);
    mod_Menu.addSlider($("#menuList"), "sunLight", "intensity", "Intensity", true);
    mod_Menu.addSlider($("#menuList"), "fieldSpecularPower", "value", "Specular Power", true, 2500);
}


function getCamDEF(){
    var inline = $("#x3DomInline");
    var vp = inline.find('Viewpoint');
    //console.log((vp)[0].getAttribute("DEF"));
    return (vp)[0].getAttribute("DEF");
}
