$j(document).ready(function(){
    $j('#meta-upload').hide();
    $j('#input_group_url').hide();


    $j('#radio-fullsize, #radio-meta').click(function() {
        $j('#meta-upload').slideDown();
    });
    $j('#radio-basic').click(function() {
        $j('#meta-upload').slideUp();
    });

    $j('#toggle_input_file').click(function(e) {
        $j('#input_group_file').hide();
        $j('#input_group_url').show();
        e.preventDefault();
    })

    $j('#toggle_input_url').click(function(e) {
        $j('#input_group_file').show();
        $j('#input_group_url').hide();
        e.preventDefault();
    })

});




