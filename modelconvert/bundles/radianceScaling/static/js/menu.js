function mod_menu() {
    var publicMod = {};

    /********* private section *************/

    function refreshSlider(event, ui) {
        var sliderVal = $(this).prev().find(".sliderVal");
        var slider = $(this).parent();
        var value = ui.value;

        if (slider.attr("data-isFloat") === "true") {
            value = value / 100;
        }

        sliderVal.text("( " + value + " )");
        slider.data("target").setAttribute(slider.data("attribute"), value);
        //$(slider.data("target")).val(value);
        //slider.data("target").attr("ambientIntensity", value);
		//alert(slider.data("target").getAttribute("id"));
    }

    /********* public section *************/
        // register menu Events
    publicMod.init = function () {
        $("#menu").draggable();
        $("#menuList").hide();
        $("#menu").addClass("menuOpened");

        // menu opener Button
        $("#menuOpener").button({
            text:true,
            icons:{
                secondary:'ui-icon-circle-triangle-s'
            }
        });
        $("#menuOpener").click(function () {
            $("#menuList").slideToggle();
            $("#menu").toggleClass("menuOpened");
            if ($("#menu").hasClass("menuOpened")) {
                $(this).button("option", "icons", {secondary:"ui-icon-circle-triangle-s"});
            }
            else {
                $(this).button("option", "icons", {secondary:"ui-icon-circle-triangle-n"});
            }

        });
    }

    publicMod.addButton = function (parent, text, callback) {
        var div = $('<div class="buttonContainer"></div>');
        var a = $('<a href="#">' + text + '</a>');

        a.button({
            text:true,
            icons:{
                secondary:' ui-icon-carat-1-e'
            }
        })

        a.click(callback);

        div.append(a);
        parent.append(div);
    }


    publicMod.addSlider = function (parent, target, attribute, text, isFloat, max) {
        var div = $('<div class="sliderContainer"></div>');
        var label = $('<div class="sliderLabel">' + text + ' <span class="sliderVal"> </span></div>');
        var slider = $('<div class="slider"></div>');


        var val = ($("#" + target))[0].getAttribute(attribute);
        //console.log(val);
        max = max || 100;

        div.attr("data-isFloat", isFloat.toString());
        div.data("target", document.getElementById(target));
        div.data("attribute", attribute);


        label.find(".sliderVal").text("( " + val + " )");
        if (isFloat) {
            val = parseInt(val * 100);
        }

        slider.slider({
            orientation: "horizontal",
            range: "min",
            max: max,
            value: val,
            slide: refreshSlider,
            change: refreshSlider
        });

        div.append(label);
        div.append(slider);
        parent.append(div);
    }

    return publicMod;
}
