// This script was created to allow communication between the upload HTML and Flask function /protected/
document.getElementById('form__submit').addEventListener('submit', async function(event) {
  // This is used to prevent defult form behaviour to ensure the function is excecuted below
    event.preventDefault();
  
    // await ensures the Flask function is complete before progessing
    await sumbitImage();
  
    // Reload the page once the script is executed
    location.reload();
  });
  
  function sumbitImage() {
    /**
   * Extracts the uploaded image, Tag input, description input, and button value from HTML and passes the infromation to the Flask framework
   * Expects: HTML button value, image path, string: tags, string: description
   * Action: The data is passed into a Flask framework to run a CNN and LLM
   * Returns: None. The image is saved and the image path, tags, and description are uploaded to a database.
   */
    var fileInput = document.getElementById('input__upload');
    var file = fileInput.files[0];
    var buttonValue = document.getElementById('button__submit').value;
    var tag_upload = document.getElementById('input__tag').value
    var description_upload = document.getElementById('input__description').value

    var formData = new FormData();
    formData.append('image', file);
    formData.append('button', buttonValue);
    formData.append('tag_upload', tag_upload);
    formData.append('description_upload', description_upload);

    return fetch('/protected/', {
        method: 'POST',
        body: formData
      })
        .catch(error => console.error(error));
  }