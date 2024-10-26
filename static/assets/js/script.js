    // Mobile Menu Toggle Logic
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuToggle && mobileMenu) {
        const toggleMenu = () => {
            mobileMenu.classList.toggle('hidden');
        };

        menuToggle.addEventListener('click', toggleMenu);
    }

