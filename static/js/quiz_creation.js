function OpenDeleteQuizForm(){
  document.getElementById('DeleteQuizFormDiv').style.display = 'block';
  // document.getElementsByClassName('page-section-covered')[0].style.backgroundColor = '#000000a3';
}

function CloseDeleteQuizForm() {
  document.getElementById('DeleteQuizFormDiv').style.display = 'none';
}


$(document).ready(function() {

  const csrf = $("input[name=csrfmiddlewaretoken]").val();

  set_question_number();

  setup_card_model();

  $(".remove-alert").click(function() {
    hide_alerts();
  });

  $('#cancel-edit-button').click(function () {
    switch_off_edition();
    clear_fields();
  })

  $("#switch-to-quiz-summary").click(function() {
    switch_to_quiz_summary();
  })

  $("#switch-to-question-form").click(function() {
    switch_off_edition();
    switch_to_question_form();
  });

  function setup_card_model() {
    window.card_model = $('#question-card').clone();
    window.card_container = $('#question-card').parent("div");

    hide_delete_icons_on_model_card();
  }


  function set_question_number() {
    var question_number = 1;

    if ($(".question-card-row").length == 1) {
      question_number = 1;
    }
    else {
      question_number = $(".question-card-row").length;
    }
    $("#question-form-number").children("h5").text("Question " + question_number);
  }

  function hide_delete_icons_on_model_card() {
    icon_1 = $('#question-card').children().children('.delete-question');
    icon_2 = $('#question-card').children().siblings("div .secondary-bg").children().children('.delete-question');

    icon_1.attr("style", "display: none !important");
    icon_2.attr("style", "display: none !important");
  }

  function hide_alerts() {
    $(".remove-alert").each(function() {
      $(this).parent().parent().hide();
    })
  }

  function switch_to_question_form() {
    $('#QuizSummary').hide();
    $('#QuestionForm').show();
    hide_alerts();
    clear_fields();
    set_question_number();
  }

  function switch_to_quiz_summary() {
    $('#QuestionForm').hide();
    $('#QuizSummary').show();
    hide_alerts();
  }

  function switch_off_edition() {
    $('#cancel-edit-button').hide();
    $("#edit-question-button").hide();
    $("#add-question-button").show();
    hide_alerts();
    remove_question_to_edit();
  }

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

  function remove_question_to_edit() {
    $.ajax({
      type: "GET",
      url: "/ajaxremovequestiontoedit",
    });
  }

  function create_question_card() {
    new_card = card_model.clone();
    new_card.removeAttr("id");
    return new_card;
  }

  function fill_quetion_card(card, question_data) {
    card.children().children("p").text(question_data["question"]);

    var answers_slots = card.children().siblings().children().children("div");

    answers_slots.each(function (index) {
      if (question_data["answers"][index] == question_data["right_answer"]) {
        $(this).addClass("font-weight-bold");
      }
      else {
        $(this).removeClass("font-weight-bold");
      }
      $(this).text(question_data["answers"][index]);
    });
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

  function show_message(message_text) {

    if ($("#QuizSummary").is(":visible")) {
      var message_to_show = $('#message-quiz-summary');
    }
    else {
      var message_to_show = $('#message-question-form');
    }
    var message_container = message_to_show.children().siblings(".col-9").children("h5");
    message_container.text(message_text);
    message_to_show.css('display', 'flex');
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
        'right_answer' : right_answer},
      dataType: "json",
      success: function(question_data) {

        if ('error' in question_data) {
          show_message(question_data["error"]);
        }
        else {
          clear_fields();
          $("#question-card").hide();
          $("#message-question-form").hide();
          var new_question_card = create_question_card();
          fill_quetion_card(new_question_card, question_data);
          card_container.append(new_question_card);
          set_question_number();
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
          show_message(result["error"]);
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
        // decrement_question_number();
        clear_fields();
        switch_off_edition();

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
    var right_answer = answers_container.siblings(".font-weight-bold").text();

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

        $('#QuizSummary').hide();

        var question_title_input = $('#question-form-number').siblings("div").children('input');
        var answers_inputs = ($('input[name=answer]'));

        question_title_input.val(title);

        answers_inputs.each(function (index) {
          $(this).val(answers[index]);
          if (answers[index] == right_answer) {

            $(this).parent().parent().siblings().children('input').val();

            $(this).parent().siblings().children().children("input").prop("checked", true);
          }
        });

        // Opening edition mode
        $('#add-question-button').hide();
        $('#cancel-edit-button').show();
        $('#edit-question-button').css('display', 'flex');
        $('#QuestionForm').show();

      },
      error: function(rs, e) {
         console.log(e);
       }});

  });

  $('#edit-question-button').click( function() {

    set_checked_answer();
    // Get the edited question form
    form_fields = get_question_form_fields();
    var question_title = JSON.stringify(form_fields[0]);
    var right_answer = JSON.stringify(form_fields[1]);
    var answers = JSON.stringify(form_fields[2]);

    if (right_answer == null) {
      right_answer = '""';
    }

    $.ajax({
      type: "GET",
      url: "/ajaxeditquestion",
      data: {'question_title': question_title,
             'right_answer': right_answer,
             'answers': answers},
      dataType: "json",
      success: function(result) {

        // Displays message if the data was not correct
        // If it's ok, the question has been updated in the backend
        // Then we display the modifications to the interface

        if ('error' in result) {
          show_message(result["error"]);
        }
        else {
          var question_title_to_edit = result['ancient_question'];
          var card_to_edit = 0;
          $('.question-card-row').each(function() {
            if ($(this).children().children("p").text() == question_title_to_edit) {
              card_to_edit = $(this);
            }
          })

          fill_quetion_card(card_to_edit, result);

          clear_fields();
          switch_off_edition();
          switch_to_quiz_summary();
        }

      },
      error: function(rs, e) {
         console.log(e);
       }});
  });

});
