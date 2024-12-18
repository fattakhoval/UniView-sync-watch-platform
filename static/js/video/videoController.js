import { actionRoomSocket } from '../chat/action.js';

const video = document.getElementById('videoPlayer');
const playButton = document.getElementById('playButton');
const seekBar = document.getElementById('seekBar');
const muteButton = document.getElementById('muteButton');
const fullScreenButton = document.getElementById('fullScreenButton');

// Воспроизведение и пауза видео
playButton.addEventListener('click', function() {
    if (video.paused) {
        video.play();
        playButton.textContent = 'Pause';
        actionRoomSocket.send(JSON.stringify({ 'action': 'play' }));

    } else {
        video.pause();
        playButton.textContent = 'Play';

        actionRoomSocket.send(JSON.stringify({ 'action': 'pause' }));
    }
});

// Обновление ползунка времени
video.addEventListener('timeupdate', function() {
    const value = (video.currentTime / video.duration) * 100;
    seekBar.value = value;
});

// Перемотка видео
seekBar.addEventListener('input', function() {
    const seekTime = (seekBar.value / 100) * video.duration;
    video.currentTime = seekTime;
});

// Включение/выключение звука
muteButton.addEventListener('click', function() {
    video.muted = !video.muted;
    muteButton.textContent = video.muted ? 'Unmute' : 'Mute';
});

// Полноэкранный режим
fullScreenButton.addEventListener('click', function() {
    if (video.requestFullscreen) {
        video.requestFullscreen();
    } else if (video.mozRequestFullScreen) { // Firefox
        video.mozRequestFullScreen();
    } else if (video.webkitRequestFullscreen) { // Chrome, Safari и Opera
        video.webkitRequestFullscreen();
    } else if (video.msRequestFullscreen) { // IE/Edge
        video.msRequestFullscreen();
    }
});