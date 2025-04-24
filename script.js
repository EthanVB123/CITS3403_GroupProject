// LOGIN FORM VALIDATION
document.getElementById("loginForm").addEventListener("submit", function (event) {
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
    errorMsg.style.display = "none";
    alert("Login successful!");
  }
});

// REGISTER FORM VALIDATION
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

  // Username validation
  var hLetter = /[a-zA-Z]/.test(username);
  var includeNumber = /\d/.test(username);
  var includeSpecialc = /[!@#$%^&*(),.?":{}|<>]/.test(username);

  // Password validation
  var pLetter = /[a-zA-Z]/.test(password);
  var pincludeNumber = /\d/.test(password);
  var pincludeSpecialc = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  // Step 1: email validation
  if (!emailCheck) {
    errorMsg.style.display = "block";
    errorMsg.textContent = "Please enter a valid email address!";
  } else if (existingEmail) {
    errorMsg.style.display = "block";
    errorMsg.textContent = "This email is already registered/taken! Please enter a new one!";
  }

  // Step 2: username validation
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

  // Step 3: password validation
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

  // ✅ Final success
  else {
    errorMsg.style.display = "none";
    alert("Registration successful!");

    // Save new user
    users.push({ email: email.toLowerCase(), username: username.toLowerCase(), password });
    localStorage.setItem("registeredUsers", JSON.stringify(users));
  }
});

