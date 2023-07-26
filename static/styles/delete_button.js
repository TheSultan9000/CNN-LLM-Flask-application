
// As the buttons are being created through a for loop to extract the information from the Flask framework, a list of all buttons is created
let btns = document.querySelectorAll(".button__delete");

// A listener is then added to each button before executing the deletefunction
btns.forEach(btn => {

   btn.addEventListener('click', async (event)=> {

    event.preventDefault();
    
    await deletefunction(btn.value); 
  
    // Reload the page once the script is executed
    location.reload();
  });
});
  
async function deletefunction(buttonValue) {
  /** 
  * Passes the button id to the flask framework
  * Expects: activation of delete button, string: button id
  * Action: POST button id to the Flask framework
  * Returns: none.
  */

    var formData = new FormData();
    formData.append('button', buttonValue);

    return fetch('/database_management/', {
        method: 'POST',
        body: formData
      })
        .catch(error => console.error(error));
  }