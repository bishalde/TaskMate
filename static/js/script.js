// script.js

document.addEventListener('DOMContentLoaded', function() {
    const crescentImage = document.querySelector('.optionsicon img[src$="/images/crescent.png"]');
    const body = document.getElementById('main-body');
    const header = document.querySelector('header');

    // Check if the user has a stored preference for the theme
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        body.classList.add(storedTheme);
        // Add dark-mode class to header if the theme is dark
        if (storedTheme == 'dark-mode') {
            header.classList.add('header-dark');
        }
    }

    crescentImage.addEventListener('click', function() {
        // Toggle dark-mode class on body
        body.classList.toggle('dark-mode');
        // Toggle header-dark class on header
        header.classList.toggle('header-dark', body.classList.contains('dark-mode'));
        // Update the stored preference for the theme
        const currentTheme = body.classList.contains('dark-mode') ? 'dark-mode' : '';
        localStorage.setItem('theme', currentTheme);
    });
});
