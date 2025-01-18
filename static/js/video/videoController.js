import { actionRoomSocket } from '../chat/action.js';

const video = document.getElementById('videoPlayer');
const playButton = document.getElementById('playButton');
const seekBar = document.getElementById('seekBar');
const muteButton = document.getElementById('muteButton');
const fullScreenButton = document.getElementById('fullScreenButton');
const buttonIcon = document.getElementById('buttonIcon');
const playIcon = '<i class="fas fa-play"></i>';
const pauseIcon = '<i class="fas fa-pause"></i>';
const muteIcon = '<i class="fa-solid fa-volume-high" style="color: #ffffff;"></i>';
const unmuteIcon = '<i class="fa-solid fa-volume-xmark" style="color: #ffffff;"></i>';



let copyText = document.querySelector('#copy-text')
document.querySelector('#copy-btn').addEventListener('click', () => {
    navigator.clipboard.writeText(copyText.value)
      .then(() => {
        alert('Ссылка для приглашения скопирована')
        console.log('Скопировано')
      })
      .catch(error => {
        console.error(`Текст не скопирован ${error}`)
      })
    });

// Воспроизведение и пауза видео
playButton.addEventListener('click', function() {
    if (video.paused) {
        video.play();
        playButton.innerHTML = pauseIcon;
        actionRoomSocket.send(JSON.stringify({ 'action': 'play' }));

    } else {
        video.pause();
        playButton.innerHTML = playIcon;

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
    actionRoomSocket.send(JSON.stringify({ 'action': 'scroll', 'seek_time': seekTime }));
});

// Включение/выключение звука
muteButton.addEventListener('click', function() {
    video.muted = !video.muted;
    muteButton.innerHTML = video.muted ? unmuteIcon : muteIcon;
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