$j(document).ready(function(){
    $j('#meta-upload').hide();


    $j('#radio-fullsize, #radio-meta').click(function() {
        $j('#meta-upload').slideDown();
    });
    $j('#radio-basic').click(function() {
        $j('#meta-upload').slideUp();
    });
});




