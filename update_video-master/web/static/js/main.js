//        $(document).ready(function () {
//            $(".video_form" ).submit(function( event ) {
//              age = form.querySelector('[name="check_box"]');
//              alert(age);
////              sendAjaxForm("video_form", "msg");
////              event.preventDefault();
//            });
//        });
//const formElement = document.getElementById('send_data'); // извлекаем элемент формы
//formElement.addEventListener('submit', (e) => {
//  e.preventDefault();
//  const formData = new FormData(formElement); // создаём объект FormData, передаём в него элемент формы
//  // теперь можно извлечь данные
//  const name = formData.get('name'); // 'John'
//  const surname = formData.get('surname'); // 'Smith'
//});

$("form").submit(function(){
    // var $form = document.querySelector("form");
    var $form = $(this);
    var $data = $form.serialize()
    alert($data)

    $.ajax({
      url: '/',
      method: 'POST',
      data: $data
    }).then(function (result) {
      console.log('result', $form.serialize())
    }).catch(function (err) {
      console.log('err')
    })

    // $.post(
    //     $form.attr("/"), // ссылка куда отправляем данные
    //     $form.method('POST'),
    //     $form.serialize()     // данные формы
    // );

    // отключаем действие по умолчанию
    return false;
});

$(document).ready(function() {
    $.ajax({
      type: GET,
      dataType: 'json',
      url: '/',
      success: function(data) { // и как правильно получить здесь?
          $("#userName").text(data.name);
          $("#userAge").text(data.age);
      }
    })
    return false;
});

        /* отправка формы через ajax */
//        function sendAjaxForm(form_ajax, msg) {
//            var form = $("#" + form_ajax);
//            $.ajax({
//                type: form.attr('method'),
//                url: form.attr('action'),
//                data: form.serialize(),
//                success: function (response) {
//                    var json = jQuery.parseJSON(response);
//                    $('#' + msg).html(json.msg);
//                    if (json.success == 'true') {
//                        form.trigger('reset');
//                    }
//                    else
//                    {
//                        alert("Что-то пошло не так!");
//                        console.log("Ошибка");
//                    }
//                },
//                error: function (error) {
//                    console.log(error);
//                }
//            });
//        }