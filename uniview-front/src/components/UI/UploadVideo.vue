<template>
  <div
    v-if="!videoFile" 
    class="upload-container"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <label for="video-upload" class="upload-box">
      <div v-if="!videoFile" class="upload-content">
        <svg
          class="upload-icon"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M12 16q.425 0 .713-.288T13 15v-4.175l.9.9q.275.275.7.275t.7-.275q.275-.275.275-.7t-.275-.7l-2.6-2.6q-.15-.15-.325-.213T12 7.25q-.2 0-.375.063T11.3 7.525L8.7 10.125q-.275.275-.275.688 0 .412.275.687.275.275.7.275t.7-.275l.9-.9V15q0 .425.288.713T12 16ZM6 21q-.825 0-1.413-.588T4 19v-7q0-.825.588-1.413T6 10h1V8q0-2.075 1.463-3.537T12 3q2.075 0 3.538 1.463T17 8v2h1q.825 0 1.413.588T20 12v7q0 .825-.588 1.413T18 21H6Z"
          />
        </svg>
        <p v-if="!isDragging">
          Перетащите видео сюда или <span>выберите файл</span>
        </p>
        <p v-else class="dragging-text">Отпустите для загрузки</p>
      </div>
    </label>
    <input
      id="video-upload"
      type="file"
      accept="video/*"
      hidden
      @change="handleFileSelect"
      ref="fileInput"
    />
  </div>

  <!-- Отображение выбранного файла -->
  <div v-if="videoFile" class="file-info">
    <p>Файл: {{ videoFile.name }}</p>
    <button @click="removeFile">Удалить</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const videoFile = ref(null); 
const isDragging = ref(false);
const fileInput = ref(null);

const emit = defineEmits(['change']);

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    console.log('handleFileSelect:', file.name);
    videoFile.value = file;
    emit('change', file);
  }

  // Важно: сброс значения input, чтобы можно было выбрать тот же файл повторно
  event.target.value = null;
};

const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('video/')) {
    console.log('handleDrop:', file.name);
    videoFile.value = file;
    emit('change', file);
  }
};

const removeFile = () => {
  videoFile.value = null;
  emit('change', null);

  // Также сбрасываем input, чтобы снова можно было выбрать тот же файл
  if (fileInput.value) {
    fileInput.value.value = null;
  }
};
</script>

<style scoped>
.upload-container {
  width: 100%;
  max-width: 400px;
  margin: auto;
}

.upload-box {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 20px;
  border: 2px dashed rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  background: rgba(49, 40, 66, 0.9);
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
  cursor: pointer;
  transition: 0.3s ease;
}

.upload-box:hover {
  background: rgba(49, 40, 66, 1);
  border-color: rgba(255, 255, 255, 0.6);
}

.upload-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.7);
}

.upload-content p {
  font-size: 14px;
  margin: 0;
}

.upload-content span {
  color: #4CAF50;
  font-weight: bold;
  cursor: pointer;
}

.dragging-text {
  color: #4CAF50;
  font-weight: bold;
}

.file-info {
  display: flex;
  justify-content: center;
  gap: 20px;
  align-items: center;
}

.file-info p {
  font-size: 14px;
  margin-bottom: 10px;
}

.file-info button {
  background: #ff4d4d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.file-info button:hover {
  background: #e63939;
}
</style>
