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

  var card_model = $('#question-card').clone();

  var card_container = $('#question-card').parent("div");

  hide_delete_icons_on_model_card();

  function hide_delete_icons_on_model_card() {
    icon_1 = $('#question-card').children().children('.delete-question');
    icon_2 = $('#question-card').children().siblings("div .secondary-bg").children().children('.delete-question');

    icon_1.attr("style", "display: none !important");
    icon_2.attr("style", "display: none !important");
  }

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

  function decrement_question_number() {
    var question_text = "Question "
    question_number --;
    $("#quiz-creation-question-number").children("h5").text(question_text + question_number);
  }

  function create_question_card(question_data) {

    new_card = card_model.clone();

    new_card.removeAttr("id");

    new_card.children().children("p").text(question_data["question"]);

    var answers_slots = new_card.children().siblings().children().children("div");

    answers_slots.each(function (index) {
      if (question_data["answers"][index] == question_data["right-answer"]) {
        $(this).addClass("font-weight-bold");
      }
      $(this).text(question_data["answers"][index]);
    });

    return new_card;

  }

  function get_question_form_fields() {
    var question_title = $('#quiz-question-form').children().children().siblings().children("input").val().replace(/"/g, '&quot;');
    var right_answer = $("input:checked").val();

    var answers = [];
    for (answer of $('input[name=answer]')) {
      answers.push(answer.value);
    }
    return [question_title, right_answer, answers];
  }

  $("#add-question-button").click(function () {

    set_checked_answer();

    form_fields = get_question_form_fields();
    var question_title = JSON.stringify(form_fields[0]);
    var right_answer = JSON.stringify(form_fields[1]);
    var answers = JSON.stringify(form_fields[2]);

    if (right_answer == null) {
      right_answer = '""';
    }

    $.ajax({
      type: "GET",
      url: "/ajaxcheckquestionfields",
      data: {
        // 'csrfmiddlewaretoken' : csrf,
        'question_title': question_title,
        'answers': JSON.stringify(answers),
        'right-answer' : right_answer},
      dataType: "json",
      success: function(question_data) {

        if ('error' in question_data) {
          $("#message-questions-text").text(question_data["error"]);
          $("#message-questions-list").css('display', 'flex');
        }
        else {
          clear_fields();
          $("#question-card").hide();
          $("#message-questions-list").hide();
          var new_question_card = create_question_card(question_data);
          card_container.append(new_question_card);
          increment_question_number();
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

  $(document).on('click', '.delete-question', function(event) {

    event.stopPropagation();

    if ($(this).hasClass("d-none")) {
      var question_title = $(this).parent().parent().siblings('div').children('p').text();
      var parent_card = $(this).parent().parent().parent();
    }
    else {
      var question_title = $(this).siblings('p').text();
      var parent_card = $(this).parent().parent();
    }

    $.ajax({
      type: "GET",
      url: "/ajaxdeletequestion",
      data: {'question_title': question_title},
      dataType: "json",
      success: function() {

        parent_card.remove();
        decrement_question_number();

        if ($(".question-card-row").length == 1) {
          $('#question-card').show();
        }
      },
      error: function(rs, e) {
         console.log(e);
       }});

  });

  $(document).on('click', '.question-card-row', function() {

    // Get the question to be edited

    if ($(this).attr('id') == "question-card") {
      return;
    }
    var title = $(this).children().children('p').text();
    var answers_container = $(this).children().siblings('div').children().children("div");

    var answers = [];
    answers_container.each(function() {
      answers.push($(this).text());
    })

    $.ajax({
      type: "GET",
      url: "/ajaxgetquestiontoedit",
      data: {'question_title': title},
      dataType: "json",
      success: function() {

        // Prepare the form to edit the question
        $('#QuestionsList').hide();

        var question_title_input = $('#quiz-creation-question-number').siblings("div").children('input');
        var answers_inputs = ($('input[name=answer]'));

        question_title_input.val(title);

        answers_inputs.each(function (index) {
          $(this).val(answers[index]);
        });

        $('#add-question-button').hide();
        $('#edit-question-button').css('display', 'flex');
        $('#QuestionForm').show();

      },
      error: function(rs, e) {
         console.log(e);
       }});

  });

  $('#edit-question-button').click( function() {

    // Get the edited question form
    form_fields = get_question_form_fields();
    var question_title = JSON.stringify(form_fields[0]);
    var right_answer = JSON.stringify(form_fields[1]);
    var answers = JSON.stringify(form_fields[2]);

    if (right_answer == null) {
      right_answer = '""';
    }

    console.log(question_title, right_answer, answers);

    $.ajax({
      type: "GET",
      url: "/ajaxeditquestion",
      data: {'question_title': question_title,
             'right_answer': right_answer,
             'answers': answers},
      dataType: "json",
      success: function() {

        // Displays message if the data was not correct
        // If not, the question has been changed in the backend, and here we're
        // gonna show again the QuestionList view

      },
      error: function(rs, e) {
         console.log(e);
       }});
  });

});
