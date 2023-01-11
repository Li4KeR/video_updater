function send_form(form_id) {
    var form = $('#'+form_id);
    var msg = form.serialize();

    var nuke = '#nuke_'+form_id
//    var msg = form.serialize();

    $('#nuke_'+form_id).addClass('display-none');
    $('#block_for_load_'+form_id).removeClass('display-none')

//    $('#nuke_'+form_id).click(function(){
//      $(this).addClass('display-none');
//      $('#block_for_load_'+form_id).removeClass('display-none')
//    });

//    alert(form_id)
    $.ajax({
        type: 'POST',
        url: '/',
        data: msg,
        success: function(data) {
            $('#nuke_'+form_id).removeClass('display-none');
            $('#block_for_load_'+form_id).addClass('display-none');
            $('#nuke_'+form_id).load('/ '+nuke);
//            $('#nuke_'+form_id.load('index.html '+ '"' + nuke + '"');
//            alert('index.html '+ '"' + nuke + '"')
        },
        error: function(){
            alert('Ошибка!');
        }
    });
//    location.reload();
}

