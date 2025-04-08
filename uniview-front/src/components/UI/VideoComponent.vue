<template>
    <div class="video_box">


        <video ref="videoElement" class="video-player" muted>
            <source class="video" :src="videoPath" type="video/webm" />
        </video>

        <div class="controls">
            <!-- <button @click="sendControlAction('play')">Play</button>
            <button @click="sendControlAction('pause')">Pause</button> -->
            <div class="play-div">



                <button @click="togglePlayPause">
                    {{ isPlaying ? 'Pause' : 'Play' }}
                </button>
                <button @click="sendControlAction('stop')">Stop</button>
            </div>
            <div class="range-div">
                <input type="range" min="0" :max="duration" v-model="currentTime" @input="onSeekInput"
                    @change="onSeekChange" />
            </div>
        </div>


    </div>



</template>


<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const roomId = route.params.id;
const videoPath = ref('');
const videoElement = ref(null);
const isPlaying = ref(true); // отслеживает, играет ли видео

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



onMounted(() => {
    setupWebSocketVideo()
    setupWebsocketController()
    watch(currentTime, () => {
        if (videoElement.value) {
            videoElement.value.currentTime = currentTime.value;
        }
    });
});

function setupWebSocketVideo() {
    ws_video = new WebSocket(`ws://localhost:8000/ws/video/${roomId}`) // URL подставь свой

  ws_video.onmessage = (event) => {
    const message = event.data;
    
    console.log(message);
    let path = "http://localhost:8000/video/" + message;
    console.log(path);
    videoPath.value = path;

    if (videoElement.value) { // Проверка, что videoElement существует
      videoElement.value.load(); // Перезагружаем видео, чтобы обновить источник
      videoElement.value.play(); // Автоматическое воспроизведение видео
      duration.value = videoElement.value.duration;
    }

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
    if (videoElement.value) {
        currentTime.value = videoElement.value.currentTime;
    }
}

function onSeekChange() {
    sendControlAction('seek');
}

</script>


<style scoped>
.video {
    width: 100%;
    height: 100%;
    background-color: black;
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
    width: 90%;
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