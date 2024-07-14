document.addEventListener('DOMContentLoaded', function() {
    const emojis = ['🎉', '👏', '🥳', '🎊', '🌟', '🏆'];
    const container = document.querySelector('.container');

    emojis.forEach(emoji => {
        const span = document.createElement('span');
        span.className = 'emoji';
        span.innerHTML = emoji;
        container.appendChild(span);
    });

    const animateEmojis = () => {
        document.querySelectorAll('.emoji').forEach((emoji, index) => {
            setTimeout(() => {
                emoji.style.transform = `scale(1) translateY(${Math.random() * 100 - 50}px) translateX(${Math.random() * 100 - 50}px)`;
                emoji.style.opacity = 1;
            }, index * 300);
        });
    };

    animateEmojis();
});
