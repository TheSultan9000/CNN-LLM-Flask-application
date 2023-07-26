// This script was created to allow communication between the upload HTML and Flask function /upload/
document.getElementById('form__upload').addEventListener('submit', async function(event) {
  // This is used to prevent defult form behaviour to ensure the function is excecuted below
  event.preventDefault();

  // While the Flask function is running this ensures that the submit form cannot be submitted and a visual loading icon ("lds-roller" element) is displayed
  var ldsRollerElement = document.querySelector('.lds-roller');
  ldsRollerElement.style.display = 'block';
  form__submit.style.display = 'none';

  // await ensures the Flask function is complete before progessing
  await uploadImage();

  // Hide the "lds-roller" element
  ldsRollerElement.style.display = 'none';
  form__submit.style.display = 'block';
});

function uploadImage() {
  /**
   * Extracts the uploaded image and button value from HTML and passes the infromation to the Flask framework
   * Expects: HTML button value, image path
   * Action: The data is passed into a Flask framework to run a CNN and LLM
   * Returns: list of strings: Tags, string: discription
   */
  var fileInput = document.getElementById('input__upload');
  var file = fileInput.files[0];
  var buttonValue = document.getElementById('button__upload').value;

  var formData = new FormData();
  formData.append('image', file);
  formData.append('button', buttonValue);

  //Communicates with the /upload/ Flask function
  return fetch('/upload/', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      var image = document.getElementById('uploaded__image');
      var result__tag = document.getElementById('result__tag');
      var result__description = document.getElementById('result__description');

      // This ensures the image is still visible ater the HTML file is rendered in Flask
      image.src = URL.createObjectURL(file);

      // The results are updated and passed back into the HTML
      result__tag.textContent = 'CNN suggested tags: ' + data.result__tag.join(', ');
      result__description.textContent = 'LLM suggested description: ' + data.result__description;
    })
    .catch(error => console.error(error));
}