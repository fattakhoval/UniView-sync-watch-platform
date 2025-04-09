<template>
    <div class="video_iframe" v-if="iframeHtml" v-html="iframeHtml"></div>

    <div v-else class="video_box">

        <video ref="videoElement" class="video-player" muted>
            <source class="video" :src="videoPath" type="video/webm" />
        </video>

        <div class="controls">
            <!-- <button @click="sendControlAction('play')">Play</button>
            <button @click="sendControlAction('pause')">Pause</button> -->
            <div class="play-div">



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
            <div class="time-display">
                {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
            </div>

        </div>


    </div>

</template>


<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const roomId = route.params.id;
const videoPath = ref('');
const videoElement = ref(null);
const isPlaying = ref(true); // отслеживает, играет ли видео
const isSeeking = ref(false); // флаг ручной перемотки
const iframeHtml = ref('');

let ws_video;
let ws_control;


const currentTime = ref(0);
const duration = ref(0);

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

function setupWebSocketVideo() {
    ws_video = new WebSocket(`ws://localhost:8000/ws/video/${roomId}`) // URL подставь свой

    ws_video.onmessage = (event) => {
        const message = event.data;
        console.log(message);

        if (typeof message === 'string' && message.startsWith('IFRAME:')) {
          const url = message.slice(7);
          iframeHtml.value = `<iframe src="${url}" width="100%" height="100%" frameborder="0" allowfullscreen></iframe>`;
          resetVideoElement();
          return;
        }

        iframeHtml.value = '';

        const path = "http://localhost:8000/video/" + message;
        console.log(path);
        initVideoElement(path);

    }
};

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