function send_form(form_id) {
    var form = $('#'+form_id);
    var msg = form.serialize();
    var nuke = '#nuke_'+form_id;

    $('#block_button_player_'+form_id).toggleClass('display-none block-button');
    $('#nuke_'+form_id).addClass('display-none');
    $('#block_for_load_'+form_id).removeClass('display-none')

    $.ajax({
        type: 'POST',
        url: '/',
        data: msg,
        success: function(data) {
            $('#nuke_'+form_id).removeClass('display-none');
            $('#block_for_load_'+form_id).addClass('display-none');
            $('#block_button_player_'+form_id).toggleClass('block-button display-none');
            $('#div_'+form_id).load('/ '+nuke);
            $('#block_feedback_status_'+form_id).text('Все ок');
            alert('vse ok')
        },
        error: function(){
            alert(form_id);
        }
    });
//    location.reload();
}


function send_play(nuke_id) {
    var form = $('#'+form_id);
    var msg = form.serialize();
    var nuke = '#nuke_'+form_id;

    $.ajax({
        type: 'POST',
        url: '/about/'+nuke_id,
        data: msg,
        success: function(data) {
            alert('good'+nuke_id)
        },
        error: function(){
            alert('not good'+nuke_id);
        }
    });
//    location.reload();
}

