jQuery(document).ready(function () {
    $("#dropdown").bind("change", function (event, ui) {
        switchNavigationMode(event.target.value);
        switchTitle(event.target.value);
    });
});

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


// workaround for meshlab output with specular '1 1 1'
function fixSpecular() {
    var mts = document.getElementsByTagName("Material");
    for (var i = 0; i < mts.length; i++) {
        mts[i].setAttribute("specularColor", "0.5 0.5 0.5");
        mts[i].setAttribute("shininess", "0.2");
    }
}
