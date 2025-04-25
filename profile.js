// profile-script.js

// Example JS variables (replace with real values or localStorage)
const User = {
    username: "ShibuTheSolver",
    puzzlesSolved: 42,
    friendRanking: 3
  };
  
  // Display values on profile.html
  window.addEventListener("DOMContentLoaded", function () {
    document.getElementById("usernameDisplay").textContent = User.username;
    document.getElementById("solvedCount").textContent = User.puzzlesSolved;
    document.getElementById("ranking").textContent = `#${User.friendRanking}`;
  });