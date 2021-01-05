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

function showQuizNameForm() {
  document.getElementById('QuizNameForm').style.display = 'block';
}
