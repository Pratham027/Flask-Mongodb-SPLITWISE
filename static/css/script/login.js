// Check if form exists
const form = document.querySelector("form");

if (form) {
  form.addEventListener("submit", (e) => {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
      e.preventDefault();
      alert("Enter both username and password!");
    }
  });
}

// Handle social buttons
document.getElementById("google-btn")?.addEventListener("click", function() {
  alert("Google login clicked! Integrate Google OAuth here.");
});

document.getElementById("apple-btn")?.addEventListener("click", function() {
  alert("Apple login clicked! Integrate Apple OAuth here.");
});

document.getElementById("facebook-btn")?.addEventListener("click", function() {
  alert("Facebook login clicked! Integrate Facebook OAuth here.");
});

console.log("✅ login.js loaded successfully!");
