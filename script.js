document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();
  
    var username = document.forms["loginForm"]["username"].value;
    var errorMsg = document.getElementById("errorMsg");
  
    var hasLetter = /[a-zA-Z]/.test(username);
    var hasNumber = /\d/.test(username);
    var hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(username);
  
    if (
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
      // window.location.href = "game.html"; // Redirect after login (optional)
    }
  });
  