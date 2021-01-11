// function duplicate() {
//     var i = 0;
//     var original = document.getElementsByClassName('question-section')[0];
//     var clone = original.cloneNode(true); // "deep" clone
//     clone.id = "duplicetor" + ++i; // there can only be one element with an ID
//     original.parentNode.appendChild(clone);
//
//     var buttons = document.getElementsByClassName('buttons-section')[0];
//     buttons.style.display = 'none';
//     original.parentNode.appendChild(buttons);
//     buttons.style.display = 'flex';
//
// }

// function showQuizNameForm() {
//   document.getElementById('QuizNameForm').style.display = 'block';
// }

function CloseDeleteQuestionForm() {
  document.getElementById('DeleteQuestionForm').style.display = 'none';
}


$(document).ready(function(){

  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  $("#CreateQuizButton").click(function(){
    $("#QuizNameForm").fadeToggle();
  });

  $(".del-question").click(function() {

    $("#DeleteQuestionForm").css("display", "block");

    // var question_id = $(this).parent().find('name.question_id').val();
    var question_id = $(this).parent().parent().siblings('input[name=question_id]').val();
    var question_number_and_title = $(this).parent().parent().siblings('.question-title')[0].innerHTML;

    clean_text = $.trim(question_number_and_title);
    question_number = clean_text.split(" ")[0];
    question_title = clean_text.split(/ (.+)/)[1];

    // console.log(question_number_and_title);
    // console.log(question_number);
    // console.log(question_title);

    $("#delete_question_title").text("Question " + question_number);
    $("#delete_question_id").val(question_id);
    $("#delete_question_message").text(question_title);

  });
});
