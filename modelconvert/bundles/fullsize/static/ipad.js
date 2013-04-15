jQuery.jQTouch({
    icon : 'jqtouch.png',
    addGlossToIcon : true,
    statusBar : 'black-translucent',
    startupScreen : '/jqt_startup_big.png',
    preloadImages : [
    ]
});

// increase the default animation speed to exaggerate the effect
jQuery.fx.speeds._default = 1000;

jQuery(document).ready(function () {
    // not used, remove metadata stuff from js file!
    jQuery.get(MYAPP.jsonFilePath, init, "json");

    jQuery( "#help" ).dialog({
        autoOpen: false,
        show: "drop",
        hide: "drop",
        resizable: false
    });
});

function init(jsonData) {
    MYAPP.data = jsonData;
    jQuery("#metaData").height(jQuery("body").height());
    createDataList();

    if (MYAPP.data.length > 0) {
        switchX3DomModel("x3DomLinkID_5");
    }
}


function createDataList() {
    var ele;
    var linkCnt = 0;
    for (var i in MYAPP.data) {
        ele = MYAPP.data[i];
        var element = jQuery('                                                              \
            <li class="arrow artItem">                                                      \
                <a href="#view" class="flip" id="x3DomLinkID_' + linkCnt + '">              \
                   <!--img src="data/' + ele.model + '/icon.png" alt="' + ele.title + '"/-->     \
                   <strong class="title">' + ele.title + '</strong><br/>                    \
                   <span class="description">' + ele.description + '</span>                 \
                </a>                                                                        \
            </li>                                                                           \
        ');

        jQuery('#resultList').append(element);
        ele.jqueryElement = element;

        jQuery("#x3DomLinkID_" + linkCnt).click(function (event) {
            switchX3DomModel(jQuery(this).attr("id"));
        });
        ele.jqueryId = "x3DomLinkID_" + linkCnt;

        linkCnt++;
    }
}

function createMetaElement(lable, data) {
    var element = jQuery('                          \
        <li class="artItem" >                       \
            <a href="#"> ' + lable + ' </a>         \
            <p class="infoText">' + data + '</p>    \
        </li>                                       \
    ');

    element.find(".infoText").hide();

    jQuery(element).click(function (event) {
        var infoText = jQuery(this).find(".infoText");
        if (infoText.is(":visible"))
            infoText.slideUp('fast');
        else
            infoText.slideDown('fast');
    });
    return element;
}


function switchX3DomModel(idStr) {
    if(MYAPP.curID == idStr.replace('x3DomLinkID_', '')){
        return;
    }

    MYAPP.curID = idStr.replace('x3DomLinkID_', '');
    var model = MYAPP.data[MYAPP.curID].model;

    //document.getElementById("x3DomInline").setAttribute('url', "data/" + model + "/model-bg.x3d");

    jQuery("#viewTitle").text(MYAPP.data[MYAPP.curID].title);
    MYAPP.cam = "inline__cam_" + model;

    switchMetaData();
}

function switchMetaData() {
    var meta = MYAPP.data[MYAPP.curID].meta;
    var metaParent = jQuery("#metaData");
    metaParent.empty();

    metaParent.append(createMetaElement("Name", meta.Name));
    metaParent.append(createMetaElement("Description", meta.description));
    metaParent.append(createMetaElement("Site", meta.Site));
}

function showHelp() {
    jQuery( "#help" ).dialog( "open" );
    //jQuery("#help").fadeIn();
}

function fixSpecular() {
    var mts = document.getElementsByTagName("Material");
    for (var i=0; i<mts.length; i++) {
        mts[i].setAttribute("specularColor", "0.5 0.5 0.5");
        mts[i].setAttribute("shininess", "0.2");
    }
}

// called in onload of inline
function setCamera() {
    // workaround for meshlab output with specular 1 1 1
    fixSpecular();
    
    // this one probably won't work, but don't care for now
    document.getElementById( MYAPP.cam ).setAttribute('set_bind','true');
}
