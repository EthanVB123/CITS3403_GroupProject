// talks to flask server to handle login and registration
document.addEventListener('DOMContentLoaded', ()=> {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    const errorEl = document.getElementById('errorMsg');
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const resp = await fetch(loginForm.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new URLSearchParams(new FormData(loginForm))
      });
      if (resp.ok) {
        // if logged in, go to homepage
        window.location = '/';
      } else {
        // if login failed, show error
        const data = await resp.json();
        errorEl.textContent = data.error || 'Unknown error';
        errorEl.style.display = 'block';
      }
    });
  }

  const registerForm = document.getElementById('Registerdata');
  if (registerForm) {
    const errorEl = document.getElementById('errorRgst');
    registerForm.addEventListener('submit', async e => {
      e.preventDefault();
      const resp = await fetch(registerForm.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new URLSearchParams(new FormData(registerForm))
      });
      if (resp.ok) {
        // if registration succeeded, go to login page
        window.location = '/login';
      } else {
        // if registration failed, show error
        const data = await resp.json();
        errorEl.textContent = data.error || 'Registration failed';
        errorEl.style.display = 'block';
      }
    });
  }
});

