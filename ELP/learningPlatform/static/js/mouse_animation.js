document.addEventListener('mousemove', function(e) {
    var mouseFollow = document.querySelector('.mouse-follow');
    mouseFollow.style.left = e.pageX + 'px';
    mouseFollow.style.top = e.pageY + 'px';
});
