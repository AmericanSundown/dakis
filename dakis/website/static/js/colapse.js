$(document).ready(function() {
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
});
