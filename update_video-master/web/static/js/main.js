function send_form(form_id) {
    var form = $('#'+form_id);
    var msg = form.serialize();

//    var msg = form.serialize();


    alert(msg)
    $.ajax({
        type: 'POST',
        url: '/',
        data: msg,
        success: function(data) {
            alert(data)
        },
        error:  function(){
            alert('Ошибка!');
        }
    });

}

//$("form").submit(function(){
//    // var $form = document.querySelector("form");
//    var $form = $(this);
//    var $data = $form.serialize()
//    alert($data)
//
//    $.ajax({
//      url: '/',
//      method: 'POST',
//      data: $data
//    }).then(function (result) {
//      console.log('result', $form.serialize())
//    }).catch(function (err) {
//      console.log('err')
//    })
//
//    // $.post(
//    //     $form.attr("/"), // ссылка куда отправляем данные
//    //     $form.method('POST'),
//    //     $form.serialize()     // данные формы
//    // );
//
//    // отключаем действие по умолчанию
//    return false;
//});
//
//$(document).ready(function() {
//    $.ajax({
//      type: GET,
//      dataType: 'json',
//      url: '/',
//      success: function(data) { // и как правильно получить здесь?
//          $("#userName").text(data.name);
//          $("#userAge").text(data.age);
//      }
//    })
//    return false;
//});
