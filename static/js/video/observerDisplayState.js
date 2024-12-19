function checkVisibility() {
    const animation = document.getElementById('animation');
    const videoContainer = document.getElementById('videoPlayerContainer');
    const iframeContainer = document.getElementById('iframePlayerContainer');

    if (videoContainer.style.display !== 'none' || iframeContainer.style.display !== 'none') {
        animation.style.display = 'none';
    } else {
        animation.style.display = 'block';
    }
}

const observer = new MutationObserver(checkVisibility);

observer.observe(document.getElementById('videoPlayerContainer'), { attributes: true });
observer.observe(document.getElementById('iframePlayerContainer'), { attributes: true });

checkVisibility();