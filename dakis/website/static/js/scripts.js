$(document).ready(function() {

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
    var selected_exps = [];
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

    // Bold best results
    var tables = $("tbody");
    for (var t=0; t < tables.size(); t++) {
        var cell_values = {};
        var row_selector = $(tables[t]).find("tr[class^='cls']");
        var cols = [".cmp-4", ".cmp-5", ".cmp-6"];
        console.log(t);

        try {
            for (var i=0; i < row_selector.size(); i++) {
                var cls = row_selector[i].classList[0];
                for (j=0; j < cols.length; j++) {
                    var val = parseFloat($(row_selector[i]).find(cols[j]).html().replace('&gt;', ''));
                    var key = cls + cols[j];
                    if (key in cell_values) {
                        cell_values[key].push(val);
                    } else {
                        cell_values[key] = [val];
                    };
                };
            };
        } catch(err) {
            break;
        };

        for (var i=0; i < row_selector.size(); i++) {
            var cls = row_selector[i].classList[0];
            for (j=0; j < cols.length; j++) {
                var cell = $(row_selector[i]).find(cols[j]);
                var val = parseFloat(cell.html().replace('&gt;', ''));
                var key = cls + cols[j];
                if (val === Math.min.apply(Math, cell_values[key])) {
                    $(cell).css("font-weight","bold");
                };
            };
        };
    };

});
