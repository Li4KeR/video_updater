function send_form(form_id) {
    var form = $('#'+form_id);
    var msg = form.serialize();

//    var msg = form.serialize();

    $('#nuke_'+form_id).click(function(){
      $(this).addClass('display-none');
      $('#block_for_load_'+form_id).removeClass('display-none')
    });

//    alert(form_id)
    $.ajax({
        type: 'POST',
        url: '/',
        data: msg,
        success: function(data) {
            $('#nuke_'+form_id).removeClass('display-none');
            $('#block_for_load_'+form_id).addClass('display-none')
//            alert(data)
        },
        error:  function(){
            alert('Ошибка!');
        }
    });

}

