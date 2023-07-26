// This script has been created to avoid saving the uplaod images before displaying
const uploadInput = document.getElementById('input__upload');
const uploadedImage = document.getElementById('uploaded__image');

uploadInput.addEventListener('change', function() {
  /**
   * Displays image uploaded by the user
   * Expects: Listener function activation on input__upload form
   * Modifies: None
   * Returns: The image in style: block;
   */
  const file = this.files[0];
  
  // Once the image has been loaded, the uploadedImage variable is updated with the image URL and the dsiplay it set to block;
  const reader = new FileReader();
  reader.onload = function(e) {
    uploadedImage.src = e.target.result;
    uploadedImage.style.display = 'block';
  }
  
  reader.readAsDataURL(file);
});