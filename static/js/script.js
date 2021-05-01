function goBack() {
  window.history.back()
}

function ClosePopUpForm() {
  document.getElementById('pop-up-form').style.display = 'none';
  document.getElementsByClassName('page-mask')[0].style.display = 'none';
}

$(document).ready(function(){

  $(window).scroll(function() {
    if ($(this).scrollTop() >= 50) {        // If page is scrolled more than 50px
        $('#return-to-top').fadeIn(200);    // Fade in the arrow
    } else {
        $('#return-to-top').fadeOut(200);   // Else fade out the arrow
    }
  });

  $(".close").click(function() {
    // document.getElementById('DeleteQuizFormDiv').style.display = 'block';
    // document.getElementsByClassName('page-section-covered')[0].style.backgroundColor = '#000000a3';
    var quiz_title = get_quiz_title();
    var message = "Votre progression sera perdue, êtes-vous sûr de vouloir quitter ?";
    var form_action = "/cancelquiz";

    $("#pop-up-form").children().children('h4').text(quiz_title);
    $("#pop-up-form").children().siblings('form').attr('action', form_action);
    $("#pop-up-form").children().siblings('form').children().children('h5').html(message);

    $('#pop-up-form').fadeIn(50);
    $('.page-mask').fadeIn(50);
  })

  function get_quiz_title() {
    return $('h1').text();
  }

  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  $('#quiz_form').submit(function(event) {
    set_checkboxes_values_in_playing();
  });

  function set_checkboxes_values_in_playing() {
    $("input[type=radio]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().parent().siblings('div').children().children().children("h3").text();
        $(this).attr("value", answer_text);

       }
     });
  }

});
