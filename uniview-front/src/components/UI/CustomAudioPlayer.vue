<template>
    <div class="voice-message">
      <button @click="togglePlayback">
        <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24" height="24">
          <path d="M8 5v14l11-7z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24" height="24">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
        </svg>
      </button>
  
      <input
        type="range"
        min="0"
        :max="duration"
        step="0.1"
        v-model="currentTime"
        @input="seekAudio"
        class="progress"
      />
  
      <span class="time">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
  
      <audio ref="audioRef" :src="src" @loadedmetadata="loaded" @timeupdate="updateTime" @ended="isPlaying = false" />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const props = defineProps({
    src: {
      type: String,
      required: true,
    },
  })
  
  const audioRef = ref(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  
  function togglePlayback() {
    if (!audioRef.value) return
    if (isPlaying.value) {
      audioRef.value.pause()
    } else {
      audioRef.value.play()
    }
    isPlaying.value = !isPlaying.value
  }
  
  function loaded() {
    duration.value = audioRef.value.duration
  }
  
  function updateTime() {
    currentTime.value = audioRef.value.currentTime
  }
  
  function seekAudio() {
    audioRef.value.currentTime = currentTime.value
  }
  
  function formatTime(sec) {
    const minutes = Math.floor(sec / 60)
    const seconds = Math.floor(sec % 60).toString().padStart(2, '0')
    return `${minutes}:${seconds}`
  }
  </script>
  
  <style scoped>
  .voice-message {
    display: flex;
    align-items: center;
    gap: 5px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2px 4px;
    border-radius: 5px;
  }
  
  .voice-message button {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
  }
  
  .progress {
    flex-grow: 1;
    width: 80%;
    height: 4px;
    appearance: none;
    background: #aaa;
    border-radius: 4px;
    outline: none;
  }
  
  .progress::-webkit-slider-thumb {
    appearance: none;
    width: 10px;
    height: 10px;
    background: white;
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .progress::-moz-range-thumb {
    width: 10px;
    height: 10px;
    background: white;
    border-radius: 50%;
    cursor: pointer;
  }
  
  .time {
    font-size: 10px;
    color: #ccc;
    white-space: nowrap;
    font-family: monospace;
  }
  </style>
  