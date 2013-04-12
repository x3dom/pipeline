var MYAPP = {};
MYAPP.mouseX;  	        // experimental
MYAPP.mouseY;
MYAPP.toggleDebug = false;

// temp solution for loading pathes
MYAPP.path              = "static/Data/Models/";
MYAPP.modelName         = "/model-cacheoptsac.x3d";
MYAPP.model = {};
MYAPP.model.birth        = MYAPP.path + "B_56_Birth/B_56_PoissonMeshQuadric.ply_conv" + MYAPP.modelName;
MYAPP.model.cruciform    = MYAPP.path + "1934-III-2-2_CruciformFigurine/1934-III-2-2_CruciformFigurineDec.ply_conv" + MYAPP.modelName;
MYAPP.model.glassFlask   = MYAPP.path + "1963-XI-22-9_GlassFlask/1963-XI-22-9_GlassFlask_PoissonMeshQuadric.ply_conv" + MYAPP.modelName;
MYAPP.model.InfotGod     = MYAPP.path + "ENKOMI_F.E.63_16_IngotGod/ENKOMI_F.E.63_16_IngotGod.ply_conv" + MYAPP.modelName;
MYAPP.model.mirror       = MYAPP.path + "KITION_F.E._T.8-34_IvoryMirrorHandle/KITION_F.E._T.8-34_IvoryMirrorHandle_PoissonMesh_Tex_Quadric.ply_conv" + MYAPP.modelName;
MYAPP.model.limesone     = MYAPP.path + "1997-VII-15-3_LimestoneSphinxAndLionComplexDec/1997-VII-15-3_LimestoneSphinxAndLionComplexDec.ply_conv" + MYAPP.modelName;

MYAPP.pathShader         = "static/shader/";
//MYAPP.pathShader         = "";

MYAPP.cam = "";


var mod_ColorPicker;
var mod_Menu;

jQuery(document).ready(function () {
    mod_ColorPicker = mod_colorPicker();
    mod_ColorPicker.init();

    mod_Menu = mod_menu();
    mod_Menu.init();

	$("#x3dMain").mousemove(function(e){ 	        // experimental
		MYAPP.mouseX = e.pageX; 
		MYAPP.mouseY = e.pageY; 
	});

});

function init(){
    //document.getElementById('x3DomInline2').addEventListener('load',initInline, false );
    //document.getElementById('inline2').addEventListener('error',showError, false );

    //document.getElementById("x3DomInline").setAttribute('url', url);
}

function initInline(){
    //MYAPP.pathShader = getRelativeShaderPath();

    //console.log("initInline()");
    modifyX3DModel();

    createMenu();
}


/***
 * When switching a x3d model the scene must be "convertet" so that the Radiance Scaling Shader works.
 * Therefor it is necessary to rewrite the appearance of the fist shape node
 */
function modifyX3DModel() {
    var app = getFirstAppearance();
    //console.log(($("#x3DomInline").find('Shape'))[1]);  // shape 1 (id 2)
    renewAppRadianceScaling(app);

    console.log(($("#x3DomInline"))[0]);  // shape 1 (id 2)

}



/***
 * replace the entire content of a Appearance node with the stuff that is needed for Radiance Scaling
 * @param app: Appearance to be replaced
 * @param shapes: Shapes that are necessary for the Rendered Texture of the new Radiance Scaling Appearance
 */
function renewAppRadianceScaling(app){
    // put the new Appearance for the first Shape node together
    var rt = jQuery('                                                                                                   \
            <RenderedTexture id="test" DEF="fieldRenderedTex" update="ALWAYS" dimensions="1024 1024 4" repeatS="false" repeatT="false" showNormals="true">    \
            </RenderedTexture>                                                                                          \
    ');
    //    <Viewpoint USE="' + getCamDEF() + '" containerField="viewpoint"></Viewpoint>                            \
    //rt.append(jQuery('<Viewpoint USE="' + getCamDEF() + '" containerField="viewpoint"></Viewpoint>'));

    var rendTex = (rt)[0];
    var vp = document.createElement("Viewpoint");
    //vp.setAttribute("USE", getCamDEF());
    vp.setAttribute("USE", "vp");
    vp.setAttribute("containerField", "viewpoint");
    rendTex.appendChild(vp);


    var cs = jQuery('<ComposedShader DEF="ComposedShader"> </ComposedShader> ');
    cs.append(jQuery('                                                                                                  \
                 <field id="fieldSpecularPower" name="fieldSpecularPower" type="SFFloat" value="1.0"></field>           \
                 <field id="fieldAlpha" name="fieldAlpha" type="SFFloat" value="0"></field>                             \
                 <field id="fieldGamma" name="fieldGamma" type="SFFloat" value="0"></field>                             \
                 <field name="fieldRenderedTex" type="SFInt32" value="0"></field>                                       \
                 <ShaderPart type="VERTEX" url="' + MYAPP.pathShader + 'radianceScalingMainVertexShader.glsl"> </ShaderPart>             \
                 <ShaderPart type="FRAGMENT" url="' + MYAPP.pathShader + 'radianceScalingMainFragmentShader.glsl"> </ShaderPart>         \
    '));

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



function debugMenu(){

    //mod_Menu.addSlider($("#menuList"), "fieldAlpha", "value", "Alpha (direction > 0.5 = neutral)", true);
}


function createMenu(){

    mod_Menu.addButton($("#menuList"), "Back", function () {
        window.location = "index.html";
    });
    mod_Menu.addButton($("#menuList"), "Toggle debug", toggleDebug);
    mod_Menu.addButton($("#menuList"), "switch Model", function () {
        //switchX3DomModel(MYAPP.model.birth);
    });
    mod_Menu.addSlider($("#menuList"), "fieldAlpha", "value", "Alpha (direction -> 0.5 = neutral)", true);
    mod_Menu.addSlider($("#menuList"), "fieldGamma", "value", "Gamma (strength -> 0 = no scaling)", true, 400);

    MYAPP.curLightID = "sun";
    mod_Menu.addButton($("#menuList"), "Light color", function () {
        mod_ColorPicker.open(MYAPP.curLightID, "color");
    });

    mod_Menu.addSlider($("#menuList"), "sunLight", "ambientIntensity", "Ambient Intensity", true);
    mod_Menu.addSlider($("#menuList"), "sunLight", "intensity", "Intensity", true);
    mod_Menu.addSlider($("#menuList"), "fieldSpecularPower", "value", "Specular Power", true, 2500);

}


function isExistId(id){
    if(document.getElementById(id) === null){
        return false;
    }
    return true;
}



function toggleDebug() {
    if(MYAPP.toggleDebug){
        $("#x3dMain").attr('showStat', 'false');        // dose not work for some reason?
        $("#x3dMain").attr('showLog', 'false');        // dose not work for some reason?
        $("#renderedTexture").attr('render', 'false');
    }

    else{
        $("#x3dMain").attr('showStat', 'true');        // dose not work for some reason?
        $("#x3dMain").attr('showLog', 'true');        // dose not work for some reason?
        $("#renderedTexture").attr('render', 'true');
    }

    MYAPP.toggleDebug = !MYAPP.toggleDebug;
}



function getCamDEF(){
    var inline = $("#x3DomInline");
    var vp = inline.find('Viewpoint');
    //console.log((vp)[0].getAttribute("DEF"));
    return (vp)[0].getAttribute("DEF");
}