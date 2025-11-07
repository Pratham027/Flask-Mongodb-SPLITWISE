// Check if form exists
const form = document.querySelector("form");

if (form) {
  form.addEventListener("submit", (e) => {
    const username = document.querySelector("input[name='username']").value.trim();
    const email = document.querySelector("input[name='email']").value.trim();
    const password = document.querySelector("input[name='password']").value.trim();
    const confirmPassword = document.querySelector("input[name='confirm_password']").value.trim();

    // Basic validation
    if (!username || !email || !password || !confirmPassword) {
      e.preventDefault();
      alert("Please fill in all fields!");
      return;
    }

    // Check email format
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!emailPattern.test(email)) {
      e.preventDefault();
      alert("Enter a valid email address!");
      return;
    }

    // Check password match
    if (password !== confirmPassword) {
      e.preventDefault();
      alert("Passwords do not match!");
      return;
    }

    // Password length check
    if (password.length < 6) {
      e.preventDefault();
      alert("Password must be at least 6 characters long!");
      return;
    }
  });
}

// Handle social buttons
document.getElementById("google-btn")?.addEventListener("click", function() {
  alert("Google signup clicked! Integrate Google OAuth here.");
});

document.getElementById("apple-btn")?.addEventListener("click", function() {
  alert("Apple signup clicked! Integrate Apple OAuth here.");
});

document.getElementById("facebook-btn")?.addEventListener("click", function() {
  alert("Facebook signup clicked! Integrate Facebook OAuth here.");
});

console.log("✅ signup.js loaded successfully!");
