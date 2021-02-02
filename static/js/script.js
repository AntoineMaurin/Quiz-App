function duplicate(maximum_rows) {

  var displayed_rows = getDisplayedRows();

  if (displayed_rows.length < maximum_rows) {
    var i = 0;
    var original = document.getElementsByClassName('answers-section')[0];
    var clone = original.cloneNode(true); // "deep" clone

    original.parentNode.appendChild(clone);

    var displayed_rows = getDisplayedRows();
    var last_element = displayed_rows[displayed_rows.length - 1];
    for (elt of last_element.getElementsByTagName("input")) {
      elt.value = '';
      elt.checked = false;
    }
  }
}

function removeRow(minimum_rows) {

  var displayed_rows = getDisplayedRows();

  if (displayed_rows.length > minimum_rows) {
    var last_element = displayed_rows[displayed_rows.length - 1];
    for (elt of last_element.getElementsByTagName("input")) {
      elt.required = false;
      elt.value = '';
      elt.name = '';
    }
    last_element.style.display = 'none';
  }
}

function getDisplayedRows() {
  var all_answer_rows = document.getElementsByClassName('answers-section');

  var displayed_rows = [];

  for (row of all_answer_rows) {
    if (row.style.display !== 'none')

      displayed_rows.push(row);
  }
  return displayed_rows;
}

function showQuizNameForm() {
  document.getElementById('QuizNameFormDiv').style.display = 'block';
}

function CloseDeleteQuestionForm() {
  document.getElementById('DeleteQuestionFormDiv').style.display = 'none';
}

function CloseEditQuestionForm() {
  document.getElementById('EditQuestionFormDiv').style.display = 'none';
}

function OpenDeleteQuizForm(){
  document.getElementById('DeleteQuizFormDiv').style.display = 'block';
}

function CloseDeleteQuizForm() {
  document.getElementById('DeleteQuizFormDiv').style.display = 'none';
}

function getNumberAndTitle(number_and_title) {
  clean_text = $.trim(number_and_title);
  var question_number = clean_text.split(" ")[0];
  var question_title = clean_text.split(/ (.+)/)[1];
  return [question_number, question_title];
}

$(document).ready(function(){

  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  $('#quiz_question_form').submit(function(event) {
    set_checkboxes_values_in_edition();
  });
  $('#DeleteQuestionForm').submit(function(event) {
    set_checkboxes_values_in_edition();
  });
  $('#EditQuestionForm').submit(function checkfieldsfunction(event) {

    event.preventDefault();

    var answers_titles = [];
    var answers_types = [];

    $("input[name=answer]").each(function() {
      answers_titles.push($(this).val());
    })

    $('input[name=is_ans_right]:checked').each(function() {
      answers_types.push("true");
    });

    $.ajax({
      type: "GET",
      url: "/ajaxcheckfields",
      data: {'answers_titles': answers_titles,
             'answers_types': answers_types},
      dataType: "json",
      success: function(result) {

        if (result["error"] == "answers not filled"){
          $("#msg_uncompleted_answers").css('display', 'block');
        }
        else if (result["error"] == "no right answer") {
          $("#msg_no_right_answer").css('display', 'block');
        }
        else {
          set_checkboxes_values_in_edition();
          $('#EditQuestionForm').submit();
          $("#EditQuestionForm").off('submit', checkfieldsfunction);
          CloseEditQuestionForm();
        }
      },
      error: function(rs, e) {
         console.log(e);
       }});

  });
  $('#quiz_question_form').submit(function(event) {
    set_checkboxes_values_in_creation();
  });
  $('#quiz_form').submit(function(event) {
    set_checkboxes_values_in_playing();
  });


  function set_checkboxes_values_in_edition() {
    $("input[type=checkbox]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().siblings('input').val();
        $(this).attr("value", answer_text);

       }
     });
  }

  function set_checkboxes_values_in_creation() {
    $("input[type=checkbox]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().parent().siblings().children('input').val();
        $(this).attr("value", answer_text);

       }
     });
  }

  function set_checkboxes_values_in_playing() {
    $("input[type=checkbox]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().siblings('h3').text();
        $(this).attr("value", answer_text);

       }
     });
  }

  $("#CreateQuizButton").click(function(){
    $("#QuizNameFormDiv").fadeToggle();
  });

  $(".del-question").click(function() {

    $("#DeleteQuestionFormDiv").css("display", "block");

    var question_id = $(this).parent().parent().siblings('input[name=question_id]').val();
    var question_number_and_title = $(this).parent().parent().siblings('.question-title')[0].innerHTML;
    var question_index = $(this).parent().parent().siblings('.question-title')[0].id;

    var question_number = getNumberAndTitle(question_number_and_title)[0];
    var question_title = getNumberAndTitle(question_number_and_title)[1];

    $("#delete_question_title").text("Question " + question_number);
    $("#delete_question_id").val(question_id);
    $("#delete_question_message").text(question_title);
    $("#DeleteQuestionFormDiv").children('form').attr("action", "/deletequestion/" + question_index);

  });

  $(".edit-question").click(function() {

    $("#EditQuestionFormDiv").css("display", "block");

    var question_index = $(this).parent().parent().siblings('.question-title')[0].id;

    var question_number_and_title = $(this).parent().parent().siblings('.question-title')[0].innerHTML;

    var question_number = getNumberAndTitle(question_number_and_title)[0];
    var question_title = getNumberAndTitle(question_number_and_title)[1];

    $("#EditQuestionFormDiv").children('form').attr("action", "/editquestion/" + question_index);
    $('#question_number').text("Question " + question_number);
    $("#question_to_edit").val(question_title);

    $.ajax({
      type: "GET",
      url: "/ajaxgetanswers",
      data: {'question_index': question_index},
      dataType: "json",
      success: function(result) {

        var number_of_rows = $('.answers-section').length;

        var i;
        for (i = 0; i < number_of_rows; i++) {
          removeRow(1);
        }

        for (res of result) {
          duplicate(7);
        }
        removeRow(1);

        var j = 0;
        $("input[name=answer]").each(function() {
          $( this ).val(result[j][0]);
          j++;
        });

        var k = 0;
        $("input[name=is_ans_right]").each(function() {
          if (result[k][1] != false) {
            $(this).prop("checked", true);
          }
          k++;
        });

      },
      error: function(rs, e) {
         console.log(e);
       }});
  });

});
