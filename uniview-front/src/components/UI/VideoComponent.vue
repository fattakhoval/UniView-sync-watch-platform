<template>
    <div class="video-player">
        <video ref="videoPlayer" controls class="video"></video>
    </div>
</template>


<script setup>

import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const roomId = route.params.id;

const videoPlayer = ref(null);
const videoSocket = ref(null);

const END_MARKER = new TextEncoder().encode("__END_OF_STREAM__");

const mediaSource = new MediaSource();

let sourceBuffer = null;
const chunkQueue = [];

onMounted(() => {
  videoSocket.value = new WebSocket(`ws://localhost:8000/ws/video/${roomId}`);
  videoSocket.value.binaryType = 'arraybuffer';


  videoPlayer.value.src = URL.createObjectURL(mediaSource);
});

mediaSource.addEventListener('sourceopen', () => {

    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8, opus"');

    sourceBuffer.addEventListener("updateend", () => {
        if (chunkQueue.length > 0 && !sourceBuffer.updating) {
        sourceBuffer.appendBuffer(chunkQueue.shift());
        }
    });

    sourceBuffer.addEventListener("error", (event) => {
        console.error("SourceBuffer error:", event);
    });

    videoSocket.value.onmessage = (event) => {
        const chunk = new Uint8Array(event.data);
        console.log(chunk)


        // Если буфер не занят — сразу добавляем, иначе в очередь
        if (mediaSource.readyState === "open" && sourceBuffer && !sourceBuffer.updating) {
            try {
                sourceBuffer.appendBuffer(chunk);
            } catch (err) {
                console.error('Error:', err);
                chunkQueue.push(chunk);
            }
        } else {
            chunkQueue.push(chunk);
        }
    };
});


onBeforeUnmount(() => {
    // Закрытие соединений при выходе из компонента
    videoSocket.value?.close();
    // controlSocket.value?.close();
});


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