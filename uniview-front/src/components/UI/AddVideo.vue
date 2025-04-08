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
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import UploadVideo from './UploadVideo.vue';
  import { useRoute } from 'vue-router';
  
  
  const route = useRoute();
  const roomId = route.params.id;
  const showUrlInput = ref(false);
  const showFileInput = ref(false);
  const videoUrl = ref('');
  const videoSocket = ref(null);
  
  
  const toggleInput = (type) => {
    if (type === 'url') {
      showUrlInput.value = !showUrlInput.value;
      showFileInput.value = false;
    } else {
      showFileInput.value = !showFileInput.value;
      showUrlInput.value = false;
    }
  };

  onMounted(() => {
  videoSocket.value = new WebSocket(`ws://localhost:8000/ws/video/${roomId}`);
});
  
  const handleFileUpload = async (FileOrEvent) => {

    const file = FileOrEvent?.target?.files?.[0] || FileOrEvent;

    if (!(file instanceof File)) {
      console.warn("Не является объектом типа File", FileOrEvent);
      return;
    }

    const chunkSize = 1024 * 1024;

    for (let i = 0; i < file.size; i += chunkSize) {
      const chunk = file.slice(i, i + chunkSize);
      const buffer = await chunk.arrayBuffer();
      videoSocket.value.send(buffer);
    }

    // Отправляем маркер окончания
    videoSocket.value.send(new TextEncoder().encode("__END_OF_STREAM__"));
  };
  </script>
  
  <style scoped>
  .add-video-container {
    display: flex;
    position: relative;
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
    top: 10px;
    left: 40%;
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
  