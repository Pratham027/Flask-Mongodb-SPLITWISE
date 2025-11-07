// Select the form
const form = document.querySelector("form");

if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault(); // Prevent actual form submission for demo

    const email = document.querySelector("input[name='email']").value.trim();

    if (!email) {
      alert("Please enter your email!");
      return;
    }

    // Basic email validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!emailPattern.test(email)) {
      alert("Please enter a valid email address!");
      return;
    }

    // Show success message
    alert(`Password reset link has been sent to ${email}!`);

    // Optionally, you can submit the form to backend after showing alert
    // form.submit();
  });
}

console.log("✅ forgot_password.js loaded successfully!");
