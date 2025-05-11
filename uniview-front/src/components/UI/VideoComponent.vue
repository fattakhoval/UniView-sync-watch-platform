<template>

    <div class="video_box">

        <video ref="videoElement" id="video" class="video-player" muted></video>

        <div class="controls">
            <!-- <button @click="sendControlAction('play')">Play</button>
            <button @click="sendControlAction('pause')">Pause</button> -->
            <div class="play-div">

                <select id="quality"></select>

                <button @click="togglePlayPause" class="control-btn">
                    <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white"
                        viewBox="0 0 16 16">
                        <path d="M4.5 3.5v9l7-4.5-7-4.5z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white"
                        viewBox="0 0 16 16">
                        <path d="M5.5 3.5v9h-1v-9h1zm6 0v9h-1v-9h1z" />
                    </svg>
                    <!-- {{ isPlaying ? 'Pause' : 'Play' }} -->
                </button>
                <button @click="sendControlAction('stop')">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M12 21C10.8907 21 9.85133 20.7913 8.882 20.374C7.91267 19.9567 7.06533 19.3853 6.34 18.66C5.61467 17.9347 5.04333 17.0873 4.626 16.118C4.20867 15.1487 4 14.1093 4 13H5C5 14.95 5.67933 16.6043 7.038 17.963C8.39667 19.3217 10.0507 20.0007 12 20C13.9493 19.9993 15.6037 19.3203 16.963 17.963C18.3223 16.6057 19.0013 14.9513 19 13C18.9987 11.0487 18.3197 9.39468 16.963 8.03801C15.6063 6.68135 13.952 6.00201 12 6.00001H11.62L13.246 7.62701L12.538 8.34701L9.692 5.48001L12.577 2.61401L13.285 3.33401L11.619 5.00001H12C13.1093 5.00001 14.1487 5.20868 15.118 5.62601C16.0873 6.04335 16.9347 6.61468 17.66 7.34001C18.3853 8.06535 18.9567 8.91268 19.374 9.88201C19.7913 10.8513 20 11.8907 20 13C20 14.1093 19.7913 15.1487 19.374 16.118C18.9567 17.0873 18.3853 17.935 17.66 18.661C16.9347 19.387 16.0873 19.958 15.118 20.374C14.1487 20.79 13.1093 20.9987 12 21Z"
                            fill="white" />
                    </svg>
                </button>
            </div>
            <div class="range-div">
                <input type="range" min="0" :max="duration" v-model="currentTime" @input="onSeekInput"
                    @change="onSeekChange" class="custom-slider" :style="{
                        background: `linear-gradient(to right, #6a11cb ${(currentTime / duration) * 100}%, #333 ${(currentTime / duration) * 100}%)`
                    }" />
            </div>
            <button @click="toggleMute" class="control-btn">
                <svg v-if="isMuted" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M3.15808 13.93C2.80815 13.347 2.62329 12.6799 2.62329 12C2.62329 11.3201 2.80815 10.653 3.15808 10.07C3.26562 9.89052 3.40952 9.73552 3.58053 9.61496C3.75155 9.49441 3.94589 9.41097 4.15108 9.37L5.84408 9.031C5.94504 9.01101 6.03611 8.957 6.10208 8.878L8.17008 6.395C9.35208 4.975 9.94408 4.266 10.4711 4.457C10.9981 4.648 11.0001 5.572 11.0001 7.42V16.582C11.0001 18.429 11.0001 19.352 10.4721 19.544C9.94508 19.734 9.35308 19.025 8.17108 17.606L6.10008 15.122C6.03436 15.0432 5.94368 14.9892 5.84308 14.969L4.15008 14.63C3.94489 14.589 3.75055 14.5056 3.57953 14.385C3.40852 14.2645 3.26562 14.1095 3.15808 13.93Z"
                        stroke="#B3B3B3" />
                    <path d="M15 15L21 9M21 15L15 9" stroke="#B3B3B3" stroke-linecap="round" />
                </svg>
                <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M11.553 3.064C11.686 3.12273 11.799 3.21883 11.8784 3.34062C11.9577 3.46241 12 3.60464 12 3.75V20.25C12.0001 20.3954 11.9579 20.5377 11.8786 20.6596C11.7993 20.7814 11.6863 20.8776 11.5533 20.9364C11.4204 20.9952 11.2732 21.0141 11.1296 20.9908C10.9861 20.9674 10.8525 20.9029 10.745 20.805L5.46 16H2.75C2.28587 16 1.84075 15.8156 1.51256 15.4874C1.18437 15.1592 1 14.7141 1 14.25V9.75C1 8.784 1.784 8 2.75 8H5.46L10.745 3.195C10.8526 3.0974 10.9863 3.03316 11.1297 3.01008C11.2731 2.987 11.4202 3.00608 11.553 3.065V3.064ZM10.5 5.445L6.255 9.305C6.11681 9.4306 5.93674 9.50014 5.75 9.5H2.75C2.6837 9.5 2.62011 9.52634 2.57322 9.57322C2.52634 9.62011 2.5 9.6837 2.5 9.75V14.25C2.5 14.388 2.612 14.5 2.75 14.5H5.75C5.937 14.5 6.117 14.569 6.255 14.695L10.5 18.555V5.445ZM18.718 4.222C18.8586 4.08155 19.0492 4.00266 19.248 4.00266C19.4468 4.00266 19.6374 4.08155 19.778 4.222C24.074 8.518 24.074 15.482 19.778 19.778C19.6358 19.9105 19.4478 19.9826 19.2535 19.9792C19.0592 19.9757 18.8738 19.897 18.7364 19.7596C18.599 19.6222 18.5203 19.4368 18.5168 19.2425C18.5134 19.0482 18.5855 18.8602 18.718 18.718C19.6003 17.8358 20.3002 16.7885 20.7777 15.6358C21.2552 14.4831 21.501 13.2477 21.501 12C21.501 10.7523 21.2552 9.51687 20.7777 8.36419C20.3002 7.21151 19.6003 6.16418 18.718 5.282C18.5776 5.14138 18.4987 4.95075 18.4987 4.752C18.4987 4.55325 18.5776 4.36263 18.718 4.222Z"
                        fill="#B3B3B3" />
                    <path
                        d="M16.2429 7.757C16.1732 7.68733 16.0905 7.63207 15.9995 7.59437C15.9085 7.55666 15.8109 7.53726 15.7124 7.53726C15.6139 7.53726 15.5163 7.55666 15.4253 7.59437C15.3343 7.63207 15.2516 7.68733 15.1819 7.757C15.1122 7.82666 15.057 7.90937 15.0193 8.00039C14.9816 8.09142 14.9622 8.18898 14.9622 8.2875C14.9622 8.38602 14.9816 8.48358 15.0193 8.5746C15.057 8.66563 15.1122 8.74833 15.1819 8.818C15.5998 9.23586 15.9312 9.73194 16.1574 10.2779C16.3835 10.8239 16.4999 11.409 16.4999 12C16.4999 12.591 16.3835 13.1761 16.1574 13.7221C15.9312 14.2681 15.5998 14.7641 15.1819 15.182C15.0494 15.3242 14.9773 15.5122 14.9807 15.7065C14.9842 15.9008 15.0629 16.0862 15.2003 16.2236C15.3377 16.361 15.5231 16.4397 15.7174 16.4432C15.9117 16.4466 16.0997 16.3745 16.2419 16.242C17.367 15.1168 17.9991 13.5907 17.9991 11.9995C17.9991 10.4083 17.368 8.88221 16.2429 7.757Z"
                        fill="#B3B3B3" />
                </svg>
            </button>

            <div class="time-display">
                {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
            </div>

        </div>
        

    </div>
    
    

</template>


<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import Hls from 'hls.js';

const route = useRoute();
const roomId = route.params.id;
const videoPath = ref('');
const videoElement = ref(null);
const isPlaying = ref(false); // отслеживает, играет ли видео
const isSeeking = ref(false); // флаг ручной перемотки
const iframeHtml = ref('');

let ws_video;
let ws_control;


const currentTime = ref(0);
const duration = ref(0);
const isMuted = ref(true);

function toggleMute() {
    if (videoElement.value) {
        isMuted.value = !isMuted.value;
        videoElement.value.muted = isMuted.value;
    }
}

function togglePlayPause() {
    if (isPlaying.value) {
        sendControlAction('pause');
        isPlaying.value = false;
    } else {
        sendControlAction('play');
        isPlaying.value = true;
    }
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}


onMounted(() => {
    setupWebSocketVideo()
    setupWebsocketController()
});


function resetVideoElement() {
    if (videoElement.value) {
        videoElement.value.pause();
        videoElement.value.removeAttribute('src');
        videoElement.value.load();
        videoElement.value.ontimeupdate = null;
        videoElement.value.onloadedmetadata = null;
    }
}

function initVideoElement(videoPathUrl) {

    nextTick(() => {
        if (!videoElement.value) {
            console.warn("videoElement еще не готов");
            return;
        }

        resetVideoElement();

        videoElement.value.onloadedmetadata = () => {
            duration.value = videoElement.value.duration;
            videoElement.value.play();
            isPlaying.value = true;
        };

        videoElement.value.ontimeupdate = () => {
            if (!videoElement.value.seeking && !isSeeking.value) {
                currentTime.value = videoElement.value.currentTime;
            }
        };

        videoElement.value.src = videoPathUrl;
        videoElement.value.load();
    });
}

async function setupWebSocketVideo() {
    ws_video = new WebSocket(`ws://localhost:8000/ws/video/${roomId}`)

    ws_video.onmessage = async (event) => {
        const message = event.data;
        console.log(message);

        if (typeof message === 'string' && message.startsWith('LINK:')) {
            const masterUrl = message.slice(5);

            const playlistData = await getPlaylistData(masterUrl);

            initVideoElementLink(playlistData);

            return;
        }

        const path = "http://localhost:8000/video/" + message;
        console.log(path);
        initVideoElement(path);

    }
};


async function getPlaylistData(masterUrl) {
    const response = await fetch('http://127.0.0.1:8000/video/playlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: masterUrl }),
    });
    const data = await response.text();
    return URL.createObjectURL(new Blob([data], { type: 'application/vnd.apple.mpegurl' }));
}

function initVideoElementLink(playlistUrl) {
    const video = document.getElementById('video');
    const qualitySelect = document.getElementById('quality');

    if (Hls.isSupported()) {
        const hls = new Hls();

    // Загружаем мастер-плейлист с изменённым URL
    hls.loadSource(playlistUrl);
    hls.attachMedia(video);

    hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
      // Заполняем список доступных качеств
      qualitySelect.innerHTML = ''; // очищаем старые значения
      data.levels.forEach((level, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.text = `${level.height}p (${Math.round(level.bitrate / 1000)} kbps)`;
        qualitySelect.appendChild(option);
      });

      
      videoElement.value.onloadedmetadata = () => {
            duration.value = videoElement.value.duration;
        };

      videoElement.value.ontimeupdate = () => {
            if (!videoElement.value.seeking && !isSeeking.value) {
                currentTime.value = videoElement.value.currentTime;
            }
        };

      // Устанавливаем обработчик изменения качества
      qualitySelect.addEventListener('change', function () {
        const selectedLevel = parseInt(this.value);
        hls.currentLevel = selectedLevel;
      });

      // Автовыбор качества (по умолчанию)
      hls.currentLevel = -1; // Автоматический выбор первого уровня
    });

    hls.on(Hls.Events.ERROR, function (event, data) {
      if (data.fatal) {
        switch (data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            console.error("Network error: ", data);
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            console.error("Media error: ", data);
            break;
          case Hls.ErrorTypes.OTHER_ERROR:
            console.error("Other error: ", data);
            break;
          default:
            console.error("Fatal error: ", data);
            break;
        }
      }
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    // Для браузеров, поддерживающих natively .m3u8 (например, Safari)
    video.src = playlistUrl;
    video.addEventListener('loadedmetadata', () => video.play());
  }
}

function setupWebsocketController() {
    ws_control = new WebSocket(`ws://localhost:8000/ws/control/${roomId}`)

    ws_control.onmessage = (event) => {
        const message = JSON.parse(event.data);
        const action = message.action

        console.log(action);
        if (videoElement.value) { // Проверка, что videoElement существует
            if (action === "pause") {
                videoElement.value.pause();
                isPlaying.value = false;

            }

            if (action === "play") {
                videoElement.value.play();
                isPlaying.value = true;
            }

            if (action === "stop") {
                videoElement.value.pause();
                videoElement.value.currentTime = 0;
            }

            if (action === "seek" && message.value !== undefined) {
                videoElement.value.currentTime = message.value;
            }
        }
    }
}

function sendControlAction(action) {
    if (ws_control && ws_control.readyState === WebSocket.OPEN) {
        if (action === 'seek') {
            // Отправляем действие "seek" с value
            ws_control.send(JSON.stringify({ action, value: currentTime.value }));
        } else {
            // Отправляем другие действия (play, pause, stop) без value
            ws_control.send(JSON.stringify({ action }));
        }
    }
}


function onSeekInput() {
    // if (videoElement.value) {
    //     currentTime.value = videoElement.value.currentTime;
    // }

    isSeeking.value = true;
}

function onSeekChange() {
    // sendControlAction('seek');

    if (videoElement.value) {
        videoElement.value.currentTime = currentTime.value;
        sendControlAction('seek');
    }
    isSeeking.value = false;
}

</script>


<style scoped>
.video_iframe {
    width: 75%;
    height: 90%;
}

.video {
    width: 100%;
    height: 100%;
    background-color: black;
}

.time-display {
    color: #ccc;
    font-size: 14px;
    padding: 0 12px;
    min-width: 100px;
}


.video_box {
    width: 75%;
    height: 90%;
    background-color: #1f1f1f;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
}

.video-player {
    width: 100%;

}

.control-btn {
    background: #2d2d2d;
    border: none;
    border-radius: 50%;
    padding: 10px;
    margin-right: 10px;
    cursor: pointer;
    transition: background 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.control-btn:hover {
    background: #444;
}

.control-btn svg {
    width: 20px;
    height: 20px;
    fill: #fff;
}

.custom-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 6px;
    outline: none;
    cursor: pointer;
    background: #333;
    /* fallback */
    transition: background 0.3s ease;
}

.custom-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 0px;
    height: 0px;
    background: transparent;
    border: none;
    box-shadow: none;
}

.custom-slider::-moz-range-thumb {
    width: 0px;
    height: 0px;
    background: transparent;
    border: none;
    box-shadow: none;
}


.range-div {
    width: 100%;
    padding: 0 12px;
}


/* Кнопки управления */
.controls {
    margin-top: 12px;
    display: flex;
    gap: 16px;
    position: absolute;
    bottom: 0;
    width: 100%;
    justify-content: start;
    align-items: center;

}

.play-div {
    display: flex;
}

.controls button {
    background-color: #1f1f1f;
    color: #fff;
    border: none;
    padding: 12px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s ease;
}

.controls button:hover {
    background-color: #2d2d2d;
}

.range-div,
.range-div input {
    width: 100%;
}

/* Ползунок */
.slider-container {
    margin-top: 16px;
    width: 100%;
    /* max-width: 960px; */
}

.slider {
    width: 100%;
    height: 6px;
    appearance: none;
    background: #444;
    border-radius: 4px;
    outline: none;
    cursor: pointer;
}

.slider::-webkit-slider-thumb {
    appearance: none;
    width: 14px;
    height: 14px;
    background: #9db358;
    border-radius: 50%;
    cursor: pointer;
}

.slider::-moz-range-thumb {
    width: 14px;
    height: 14px;
    background: #9db358;
    border: none;
    border-radius: 50%;
    cursor: pointer;
}
</style>