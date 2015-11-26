$(document).ready(function() {
    var selected_exps = [];

    // Colapse
    $('.show_children').click(function(){
        $(this).parent().next('.children').css('display', 'inline');
        $(this).parent().find('.show_children').css('display', 'none');
        $(this).parent().find('.hide_children').css('display', 'inline');
    });
    $('.hide_children').click(function() {
        $(this).parent().next('.children').css('display', 'none');
        $(this).parent().find('.show_children').css('display', 'inline');
        $(this).parent().find('.hide_children').css('display', 'none');
    });

    // Select experiments
    $('.exp').click(function() {
        var exp_pk = $(this).attr('exp_pk');
        if ($(this).is(':checked')) {
            selected_exps.push(exp_pk);
        } else {
            selected_exps.pop(exp_pk);
        };
        var href = $('#comparison-url').attr('href').split('=')[0];
        $('#comparison-url').attr('href', href+'='+selected_exps);
    });

});
