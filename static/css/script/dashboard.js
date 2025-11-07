// 1️⃣ Handle editing expenses
document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.group-card');
        const title = prompt("Edit title", card.querySelector('.group-info h4').innerText);
        const amount = prompt("Edit amount", card.querySelector('.amount-info p').innerText.replace('₹',''));
        const split_with = prompt("Edit split_with (comma-separated)", card.querySelector('.group-info p').innerText);

        if(title && amount !== null) {
            // Create a form to submit POST request for updating expense
            const expenseId = card.getAttribute('data-id');
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/update/${expenseId}`;

            const titleInput = document.createElement('input');
            titleInput.name = 'title';
            titleInput.value = title;
            form.appendChild(titleInput);

            const amountInput = document.createElement('input');
            amountInput.name = 'amount';
            amountInput.value = amount;
            form.appendChild(amountInput);

            const splitInput = document.createElement('input');
            splitInput.name = 'split_with';
            splitInput.value = split_with;
            form.appendChild(splitInput);

            document.body.appendChild(form);
            form.submit();
        }
    });
});

// 2️⃣ Handle logout button separately
const logoutBtn = document.getElementById("logout-btn");

if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    const confirmLogout = confirm("Are you sure you want to logout?");
    if (confirmLogout) {
      window.location.href = "/logout";
    }
  });
}

console.log("✅ dashboard.js loaded successfully!");
