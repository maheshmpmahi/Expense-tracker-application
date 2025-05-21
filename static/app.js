document.addEventListener('DOMContentLoaded', function () {
  const sign_in_btn = document.querySelector("#sign-in-btn");
  const sign_up_btn = document.querySelector("#sign-up-btn");
  const container = document.querySelector(".container");

  const users = {}; // Simulated in-memory user database

  // Panel switching
  sign_up_btn?.addEventListener("click", () => container.classList.add("sign-up-mode"));
  sign_in_btn?.addEventListener("click", () => container.classList.remove("sign-up-mode"));

  // Login form logic
  const loginForm = document.getElementById('loginForm');
  loginForm?.addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
      alert('Please fill in both fields.');
      return;
    }

    if (users[username] && users[username] === password) {
      window.location.href = 'login.html'; // Redirect to dashboard
    } else {
      alert('Invalid username or password!');
    }
  });

  // Sign-up form logic
  const signupForm = document.getElementById('signupForm');
  loginForm?.addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${username}&password=${password}`
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Redirect to dashboard if successful
        } else {
            alert('Sign up successful! Please log in.');
        }
    });
});
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    if (users[username]) {
      alert('Username already exists!');
      return;
    }

    users[username] = password; // Store new user
    alert('Sign up successful! Please log in.');
    container.classList.remove("sign-up-mode"); // Switch to sign-in form
  });
