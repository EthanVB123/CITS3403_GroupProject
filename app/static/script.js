document.addEventListener("DOMContentLoaded", (event) => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm != null) {
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault();

      var username = document.forms["loginForm"]["username"].value.trim();
      var password = document.getElementById("password").value.trim();
      var errorMsg = document.getElementById("errorMsg");

      var hasLetter = /[a-zA-Z]/.test(username);
      var hasNumber = /\d/.test(username);
      var hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(username);

      var pswdLetter = /[a-zA-Z]/.test(password);
      var pswdNumber = /\d/.test(password);
      var pswdSpecialCharacter = /[!@#$%^&*(),.?":{}|<>]/.test(password);

      if (
        password.length < 8 ||
        !pswdLetter ||
        !pswdNumber ||
        !pswdSpecialCharacter
      ) {
        errorMsg.style.display = "block";
        errorMsg.textContent =
          "Password must be at least 8 characters and include a letter, number, and special character.";
      } else if (
        username.length < 8 ||
        !hasLetter ||
        !hasNumber ||
        !hasSpecialChar
      ) {
        errorMsg.style.display = "block";
        errorMsg.textContent =
          "Username must be at least 8 characters and include a letter, number, and special character.";
      } else {
        let users = JSON.parse(localStorage.getItem("registeredUsers")) || [];
        let correctUser = users.find(user =>
          user.username.toLowerCase() === username.toLowerCase() &&
          user.password === password
        );

        if (correctUser) {
          errorMsg.style.display = "none";
          localStorage.setItem("currentUser", JSON.stringify(correctUser));
          window.location.href = "homepage.html"; 
        } else {
          errorMsg.style.display = "block";
          errorMsg.textContent = "We don’t seem to have your login account. Please try again.";
        }
      }
    }); 
  }

  // REGISTER FORM VALIDATION
  const registrationForm = document.getElementById("Registerdata");
  if (registrationForm != null) {
    document.getElementById("Registerdata").addEventListener("submit", function (event) {
      event.preventDefault();

      const email = document.getElementById("email").value.trim();
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();
      const errorMsg = document.getElementById("errorRgst");

      // Simulated registered users (you can replace with localStorage retrieval)
      let users = JSON.parse(localStorage.getItem("registeredUsers")) || [];
      let takenEmails = users.map(user => user.email.toLowerCase());

      var emailCheck = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      var existingEmail = users.some(user => user.email.toLowerCase() === email.toLowerCase());
      var existingUsername = users.some(user => user.username.toLowerCase() === username.toLowerCase());

      // what needs to be included in our username to be valid-establish it as variables to be used in condition statements 
      var hLetter = /[a-zA-Z]/.test(username);
      var includeNumber = /\d/.test(username);
      var includeSpecialc = /[!@#$%^&*(),.?":{}|<>]/.test(username);

      // what needs to be included in our password to be valid-establish it as variables to be used in condition statements 
      var pLetter = /[a-zA-Z]/.test(password);
      var pincludeNumber = /\d/.test(password);
      var pincludeSpecialc = /[!@#$%^&*(),.?":{}|<>]/.test(password);

      // check if email is there
      if (!emailCheck) {
        errorMsg.style.display = "block";
        errorMsg.textContent = "Please enter a valid email address!";
      } else if (existingEmail) {
        errorMsg.style.display = "block";
        errorMsg.textContent = "This email is already registered/taken! Please enter a new one!";
      }

      //check if our username meets the requirements 
      else if (
        username.length < 8 ||
        !hLetter ||
        !includeNumber ||
        !includeSpecialc ||
        existingUsername
      ) {
        errorMsg.style.display = "block";
        errorMsg.textContent =
          "Username cannot be created — must be at least 8 characters and include a letter, a number, and a special character (and must be unique).";
      }

      // check if password meets the requirements 
      else if (
        password.length < 8 ||
        !pLetter ||
        !pincludeNumber ||
        !pincludeSpecialc
      ) {
        errorMsg.style.display = "block";
        errorMsg.textContent =
          "Password cannot be created — must be at least 8 characters and include a letter, number, and special character.";
      }

      //  if everything is good display a message that shows registeration has been processed
      else {
        errorMsg.style.display = "none";
        alert("Registration successful!");

        // Save our new user
        users.push({ email: email.toLowerCase(), username: username.toLowerCase(), password });
        localStorage.setItem("registeredUsers", JSON.stringify(users));
        window.location.href = "login.html"; //send them to the login page if succesfully completes registeration
        
      }

    });
  }
});
