// Efeitos de Hover interativos para os cards e glows
document.addEventListener('DOMContentLoaded', () => {
    // Segue o mouse suavemente com os glows do background
    const glow1 = document.querySelector('.glow-1');
    const glow2 = document.querySelector('.glow-2');

    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        // Movimento Parallax invertido bem sutil
        glow1.style.transform = `translate(${x * -50}px, ${y * -50}px)`;
        glow2.style.transform = `translate(${x * 50}px, ${y * 50}px)`;
    });

    // Smooth scroll para links da ancora
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
