function mod_colorPicker() {
    var publicMod = {};

    /********* private section *************/

    /****
     * refreshes interaction between the sliders
     */
    function refreshColorPickerAllSlider() {
        var all = $("#all").slider("value");
        $("#red").slider("value", all);
        $("#green").slider("value", all);
        $("#blue").slider("value", all);
    }
    /****
     * refreshes the color picker swatch and the target when a slider is moved
     */
    function refreshColorPicker() {
        var red = $("#red").slider("value");
        var green = $("#green").slider("value");
        var blue = $("#blue").slider("value");
        var color = x3domColorFromRGB(red, green, blue);
        var hex = hexFromRGB(red, green, blue);

        $("#colorPickerSwatch").css("background-color", "#" + hex);
		$("#colorPicker").data("targetMat").setAttribute("diffuseColor", color);
		$("#colorPicker").data("targetLight").setAttribute($("#colorPicker").data("attribute"), color);
    }
    /****
     * sets the 3 sliders of the color picker by spliting the sting of color into its components
     * @param colorStr is a string like this -> "0.2 0.5 0.2" the components need to be between 0 and 1
     */
    function setColorPickerSlider(colorStr) {
        var cols = colorStr.split(" ");
        var r = parseInt(parseFloat(cols[0]) * 255);
        var g = parseInt(parseFloat(cols[1]) * 255);
        var b = parseInt(parseFloat(cols[2]) * 255);
        var all = parseInt((r + g + b) / 3);

        $("#all").slider("value", all);
        $("#red").slider("value", r);
        $("#green").slider("value", g);
        $("#blue").slider("value", b);
    }


    /********* color transformations *************/
    function hexFromRGB(r, g, b) {
        var hex = [
            r.toString(16),
            g.toString(16),
            b.toString(16)
        ];
        $.each(hex, function (nr, val) {
            if (val.length === 1) {
                hex[ nr ] = "0" + val;
            }
        });
        return hex.join("").toUpperCase();
    }
    function hexFromX3domColor(color) {
        var cols = color.split(" ");
        var r = parseInt(parseFloat(cols[0]) * 255);
        var g = parseInt(parseFloat(cols[1]) * 255);
        var b = parseInt(parseFloat(cols[2]) * 255);
        //console.log(color + " - "+ r + " - " +g +  " - "+b)
        return hexFromRGB(r, g, b);
    }
    function x3domColorFromRGB(r, g, b) {
        return r / 255 + ' ' + g / 255 + ' ' + b / 255;
    }



    /********* public section *************/
        // register menu Events
    publicMod.init = function (){
        // init slider
        $("#red, #green, #blue").slider({
            orientation:"horizontal",
            range:"min",
            max:255,
            value:127,
            slide: refreshColorPicker,
            change: refreshColorPicker
        });
        $("#all").slider({
            orientation:"horizontal",
            range:"min",
            max:255,
            value:127,
            slide: refreshColorPickerAllSlider,
            change: refreshColorPickerAllSlider
        });

        $("#colorPicker").draggable();

        // buttons
        $("#colorPickerOK").button({
            text:true,
            icons:{
                secondary:'ui-icon-circle-check'
            }
        });
        $("#colorPickerOK").click(function () {
            var red = $("#red").slider("value");
            var green = $("#green").slider("value");
            var blue = $("#blue").slider("value");
            var color = x3domColorFromRGB(red, green, blue);
			
            //console.log(color)
            $("#colorPicker").fadeOut();
        });
        $("#colorPickerCancel").button({
            text:true,
            icons:{
                secondary:'ui-icon-circle-close'
            }
        });
        $("#colorPickerCancel").click(function () {
            // reset the color of the target
			$("#colorPicker").data("targetMat").setAttribute("diffuseColor", $("#colorPicker").data("oldColor"));
			$("#colorPicker").data("targetLight").setAttribute($("#colorPicker").data("attribute"), $("#colorPicker").data("oldColor"));
            $("#colorPicker").fadeOut();
        });

        $("#colorPicker").hide();
    }

    publicMod.open = function (targetId, attribute){
        $("#colorPicker").data("targetLight", document.getElementById(targetId + "Light"));
        $("#colorPicker").data("targetMat", document.getElementById(targetId + "Mat"));
        $("#colorPicker").data("attribute", attribute);
        var oldColor = $("#colorPicker").data("targetMat").getAttribute("diffuseColor");
        var hex = hexFromX3domColor(oldColor);

        setColorPickerSlider(oldColor);

        $("#colorPicker").data("oldColor", oldColor);
        $("#colorPickerSwatch").css("background-color", "#" + hex);
        $("#colorPicker").fadeIn();
    }

    return publicMod;
}
