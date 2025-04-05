<template>
    <div class="add-video-container">
      <button @click="toggleInput('url')" class="add-button">Добавить ссылку</button>
      <button @click="toggleInput('file')" class="add-button">Загрузить видео</button>
  
      <transition name="fade">
        <div v-if="showUrlInput" class="input-wrapper">
          <input 
            v-model="videoUrl" 
            type="text" 
            placeholder="Введите ссылку на видео" 
            class="input-field"
          />
        </div>
      </transition>
  
      <transition name="fade">
        <div v-if="showFileInput" class="input-wrapper">
            <UploadVideo @change="handleFileUpload" />
          <!-- <input 
            type="file" 
            
            class="input-field"
          /> -->
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
import UploadVideo from './UploadVideo.vue';
  
  const showUrlInput = ref(false);
  const showFileInput = ref(false);
  const videoUrl = ref('');
  
  const toggleInput = (type) => {
    if (type === 'url') {
      showUrlInput.value = !showUrlInput.value;
      showFileInput.value = false;
    } else {
      showFileInput.value = !showFileInput.value;
      showUrlInput.value = false;
    }
  };
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Файл загружен:', file.name);
    }
  };
  </script>
  
  <style scoped>
  .add-video-container {
    display: flex;
    gap: 10px;
    padding: 10px 20px;
  }
  
  .add-button {
    background: rgba(49, 40, 66, 0.7);
    color: #fff;
    border: 1px solid rgba(105, 96, 131, 0.769);
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
  }
  
  .add-button:hover {
    background-color: rgba(63, 46, 96, 0.853);
  }
  
  /* Контейнер для инпутов — поверх всех слоев */
  .input-wrapper {
    position: absolute;
    top: 220px;
    left: 13%;
    transform: translateX(-50%);
    z-index: 1000;
  }
  
  .input-field {
    width: 300px;
    padding: 8px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 5px;
    background: rgba(49, 40, 66, 0.9);
    color: #fff;
    outline: none;
    font-size: 14px;
  }
  
  /* Анимация появления */
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease-in-out;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  </style>
  