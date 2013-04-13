var MYAPP = {};
MYAPP.mouseX;  	        // experimental
MYAPP.mouseY;
MYAPP.toggleDebug = false;

MYAPP.path        = {};
MYAPP.path.shader = "static/shader/";



var mod_ColorPicker;
var mod_Menu;
var mod_MoveObj;

jQuery(document).ready(function () {
    mod_ColorPicker = mod_colorPicker();
    mod_ColorPicker.init();

    mod_Menu = mod_menu();
    mod_Menu.init();
});


function initInline(){
    //MYAPP.path.shader = getRelativeShaderPath();

    modifyX3DModel();
    createMenu();
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
            <Viewpoint USE="vp" containerField="viewpoint"></Viewpoint>                                                 \
        </RenderedTexture>                                                                                              \
    ');

    var cs = jQuery('<ComposedShader DEF="ComposedShader"> </ComposedShader> ');
    cs.append(jQuery('                                                                                                  \
         <field id="fieldSpecularPower" name="fieldSpecularPower" type="SFFloat" value="1.0"></field>                   \
         <field id="fieldAlpha" name="fieldAlpha" type="SFFloat" value="0"></field>                                     \
         <field id="fieldGamma" name="fieldGamma" type="SFFloat" value="0"></field>                                     \
         <field name="fieldRenderedTex" type="SFInt32" value="0"></field>                                               \
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
