<template>
<video ref="videoElement" controls class="video-player" muted>
  <source class="video" :src="videoPath" type="video/webm" />
</video>

<div>
  <button @click="sendControlAction('play')">Play</button>
  <button @click="sendControlAction('pause')">Pause</button>
  <button @click="sendControlAction('stop')">Stop</button>
</div>

<div>
  <input
    type="range"
    min="0"
    :max="duration"
    v-model="currentTime"
    @input="onSeekInput"
    @change="onSeekChange"
  />
</div>



</template>


<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const roomId = route.params.id;
const videoPath = ref('');
const videoElement = ref(null);
let ws_video;
let ws_control;


const currentTime = ref(0);
const duration = ref(0)


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

function setupWebsocketController(){
  ws_control = new WebSocket(`ws://localhost:8000/ws/control/${roomId}`)

  ws_control.onmessage = (event) => {
    const message = JSON.parse(event.data);
    const action = message.action

    console.log(action);
    if (videoElement.value) { // Проверка, что videoElement существует
      if (action === "pause") {
        videoElement.value.pause();
      }

      if (action === "play") {
        videoElement.value.play();
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
.video-player {
    width: 75%;
    height: 100%;
}
</style>