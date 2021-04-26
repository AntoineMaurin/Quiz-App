function OpenDeleteQuizForm(){
  document.getElementById('DeleteQuizFormDiv').style.display = 'block';
  // document.getElementsByClassName('page-section-covered')[0].style.backgroundColor = '#000000a3';
}

function CloseDeleteQuizForm() {
  document.getElementById('DeleteQuizFormDiv').style.display = 'none';
}

$(document).ready(function() {

  const csrf = $("input[name=csrfmiddlewaretoken]").val();

  var question_number = 1;
  $("#quiz-creation-question-number").children("h5").text("Question " + question_number);

  $(".remove-alert").click(function() {
    $(".remove-alert").parent().parent().hide();
  });

  $("#toggle-questions-list").click(function() {
    $('#QuestionForm').hide();
    $('#QuestionsList').show();
  });

  $("#toggle-quiz-summary").click(function() {
    $('#QuestionsList').hide();
    $('#QuestionForm').show();
  });

  function set_checked_answer() {
    $("input[type=radio]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().parent().siblings().children('input').val();
        $(this).attr("value", answer_text);

       }
     });
  }

  function clear_fields() {

    $("input:not([type=hidden]").each(function() {
      $(this).val('');
    });

    $("input[type=radio]").each(function() {
      if (this.checked) {
        $(this).prop("checked", false);
       }
     });
  }

  function increment_question_number() {
    var question_text = "Question "
    question_number ++;
    $("#quiz-creation-question-number").children("h5").text(question_text + question_number);
  }

  function add_question(question_data) {
    var card = $('#question_creation_card').clone();
    var card_container = $("#question_creation_card").parent("div");

    card.children().children("p").text(question_data["question"]);
    card.removeAttr("id");

    var answers = card.children().siblings().children().children("div");

    answers.each(function (index) {
      if (question_data["answers"][index] == question_data["right-answer"]) {
        $(this).addClass("font-weight-bold");
      }
      $(this).text(question_data["answers"][index]);
    });

    card_container.append(card);
    card.css('display', 'flex');
  }

  $("#add-question-button").click(function () {

    set_checked_answer();

    var form_data = $('#quiz_question_form').serializeArray();
    var answers = [];
    for (answer of $('input[name=answer]')) {
      answers.push(answer.value);
    }

    $.ajax({
      type: "GET",
      url: "/ajaxcheckquestionfields",
      data: {
        // 'csrfmiddlewaretoken' : csrf,
        'form_data': JSON.stringify(form_data),
        'answers': JSON.stringify(answers)},
      dataType: "json",
      success: function(result) {

        // $("input[name=csrfmiddlewaretoken]").val(csrf);

        if ('error' in result) {
            $("#message-questions-text").text(result["error"]);
            $("#message-questions-list").css('display', 'flex');
        }
        else {
            clear_fields();
            increment_question_number();
            $("#question_creation_card").hide();
            $("#message-questions-list").hide();
            add_question(result);
        }
      },
      error: function(rs, e) {
         console.log(e);
       }});
  });

  // On click -> check -> then submit, or show message

  $('#submit-quiz-button').click( function() {

    $.ajax({
      type: "GET",
      url: "/ajaxcheckquiz",
      success: function(result) {

        if ('error' in result) {
          $("#message-quiz-text").text(result["error"]);
          $("#message-quiz-list").css('display', 'flex');
        }
        else {
          $('#quiz-creation-form').submit();
        }

      },
      error: function(rs, e) {
         console.log(e);
       }});

  });

});
