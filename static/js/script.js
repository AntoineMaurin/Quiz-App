function duplicate() {
    var i = 0;
    var original = document.getElementsByClassName('answers-section')[0];
    var clone = original.cloneNode(true); // "deep" clone

    original.parentNode.appendChild(clone);

    var displayed_rows = getDisplayedRows();
    var last_element = displayed_rows[displayed_rows.length - 1];
    for (elt of last_element.getElementsByTagName("input")) {
      elt.value = '';
    }
    var all_buttons = document.getElementsByClassName('buttons-section');

    for (button of all_buttons) {
      button.style.display = 'none';
    }
    var buttons = document.getElementsByClassName('buttons-section')[0];
    var buttons_clone = buttons.cloneNode(true);
    original.parentNode.appendChild(buttons_clone);
    buttons_clone.style.display = 'flex';

}

function removeRow() {

  var displayed_rows = getDisplayedRows();

  if (displayed_rows.length > 1) {
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
  document.getElementById('QuizNameForm').style.display = 'block';
}

function CloseDeleteQuestionForm() {
  document.getElementById('DeleteQuestionForm').style.display = 'none';
}

function OpenDeleteQuizForm(){
  document.getElementById('DeleteQuizForm').style.display = 'block';
}

function CloseDeleteQuizForm() {
  document.getElementById('DeleteQuizForm').style.display = 'none';
}

$(document).ready(function(){

  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  $('#quiz_form').submit(function(event) {

    $("input[type=checkbox]").each(function() {

      if (this.checked) {

        let answer_text = $(this).parent().siblings('input').val();
        $(this).attr("value", answer_text);

       }
     });

  });

  $("#CreateQuizButton").click(function(){
    $("#QuizNameForm").fadeToggle();
  });

  $(".del-question").click(function() {

    $("#DeleteQuestionForm").css("display", "block");

    // var question_id = $(this).parent().find('name.question_id').val();
    var question_id = $(this).parent().parent().siblings('input[name=question_id]').val();
    var question_number_and_title = $(this).parent().parent().siblings('.question-title')[0].innerHTML;
    var question_index = $(this).parent().parent().siblings('.question-title')[0].id;

    clean_text = $.trim(question_number_and_title);
    question_number = clean_text.split(" ")[0];
    question_title = clean_text.split(/ (.+)/)[1];

    $("#delete_question_title").text("Question " + question_number);
    $("#delete_question_id").val(question_id);
    $("#delete_question_message").text(question_title);
    $("form").attr("action", "/deletequestion/" + question_index);

  });
});
