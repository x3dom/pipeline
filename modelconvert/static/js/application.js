$(document).ready(function(){
    $('#meta-upload').hide();
    $('#input_group_url').hide();


    $('#radio-fullsize, #radio-meta').click(function() {
        $('#meta-upload').slideDown();
    });
    $('#radio-basic').click(function() {
        $('#meta-upload').slideUp();
    });

    $('#toggle_input_file').click(function(e) {
        $('#input_group_file').hide();
        $('#input_group_url').show();
        e.preventDefault();
    })

    $('#toggle_input_url').click(function(e) {
        $('#input_group_file').show();
        $('#input_group_url').hide();
        e.preventDefault();
    })



    // generic toggler
    $('a.toggler').each(function() {
        // hide all elements with ids given in hrefs
        $($(this).attr('href')).hide();
    })
    $('a.toggler').each(function() {
        $(this).click(function(e) {
            e.preventDefault();
            var elem = $($(this).attr('href'));
            var link = $(this);
            elem.slideToggle('fast', function() {

            if ($(this).is(':visible')) {
                link.text(link.attr('data-toggle-on'))
            } else {
                link.text(link.attr('data-toggle-off'))
            }

            });
        });
    });

});




