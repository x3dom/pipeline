
// workaround for meshlab output with specular '1 1 1'
function fixSpecular() {
    var mts = document.getElementsByTagName("Material");
    for (var i=0; i<mts.length; i++) {
        mts[i].setAttribute("specularColor", "0.5 0.5 0.5");
        mts[i].setAttribute("shininess", "0.2");
    }
}