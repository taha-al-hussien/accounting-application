html = document.querySelector(':root');
html.classList.add('theme-transition');
theme = localStorage.getItem('ammar-theme')
html.setAttribute('data-bs-theme', theme ? theme : 'dark');
addEventListener('keydown', (e) => {
  if (e.key == 'n') {
    html.setAttribute('data-bs-theme', 'dark')
    localStorage.setItem('ammar-theme', 'dark')
  } else if (e.key == 'd') {
    html.setAttribute('data-bs-theme', 'light')
    localStorage.setItem('ammar-theme', 'light')
  } else if (e.key == 'r') {
  } 
})