var MYAPP = {};
MYAPP.data = {};
MYAPP.curID = -1;
MYAPP.jsonFilePath = "metadata.txt";
MYAPP.cam = "";
MYAPP.metaStatus = 2;

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
        switchX3DomModel("x3DomLinkID_5");  // hier muss normalerweise das erste modell hin!!!!!!!!!!!!!!!!!! also id0
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


function setCamera(){
    //alert(MYAPP.cam);
    document.getElementById( MYAPP.cam ).setAttribute('set_bind','true');
}

