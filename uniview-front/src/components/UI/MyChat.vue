<template>
  <div class="chat">
    <!-- <p>ЧАТ</p> -->
    <div class="chat-header">
      <p>ЧАТ</p>
      <span class="tooltip-container">
        <InfoIcon class="my-icon"/>
        <span class="tooltip-text">Можно обратиться к боту через !bot</span>
      </span>
    </div>


    <div ref="chatContainer" class="messages">
      <div class="mes-box" v-for="(msg, index) in messages" :key="index">
        <div class="message-header">
          <span class="sender">{{ msg.sender }}</span>
          <span class="time">{{ msg.time }}</span>
        </div>
        <div class="message-text">
          <template v-if="msg.type === 'voice' && msg.voice_path">
            <div class="voice-message">
              <CustomAudioPlayer :src="`api/messages/voices/${msg.voice_path}`" />

            </div>
          </template>
          <template v-else>
            {{ msg.text }}
          </template>
        </div>
      </div>
    </div>

    <div class="message-input">
      <input class="input" v-model="chatInput" @keyup.enter="sendMessage" placeholder="Введите сообщение..." />
      <!-- <button @click="sendMessage">></button> -->
      <button @mousedown="startRecording" @mouseup="stopRecording">
        <svg :class="{ recording: isRecording }" width="15" height="15" viewBox="0 0 40 40" fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M31.667 15C32.109 15 32.5329 15.1756 32.8455 15.4881C33.1581 15.8007 33.3337 16.2246 33.3337 16.6667C33.334 19.9142 32.1491 23.0502 30.0014 25.4861C27.8536 27.922 24.8907 29.4903 21.6687 29.8967L21.667 33.3333H26.667C27.109 33.3333 27.5329 33.5089 27.8455 33.8215C28.1581 34.134 28.3337 34.558 28.3337 35C28.3337 35.442 28.1581 35.8659 27.8455 36.1785C27.5329 36.4911 27.109 36.6667 26.667 36.6667H13.3337C12.8916 36.6667 12.4677 36.4911 12.1551 36.1785C11.8426 35.8659 11.667 35.442 11.667 35C11.667 34.558 11.8426 34.134 12.1551 33.8215C12.4677 33.5089 12.8916 33.3333 13.3337 33.3333H18.3337V29.8967C15.1113 29.4907 12.148 27.9225 9.99991 25.4866C7.85182 23.0507 6.66669 19.9144 6.66699 16.6667C6.66699 16.2246 6.84259 15.8007 7.15515 15.4881C7.46771 15.1756 7.89163 15 8.33366 15C8.77569 15 9.19961 15.1756 9.51217 15.4881C9.82473 15.8007 10.0003 16.2246 10.0003 16.6667C10.0003 19.3188 11.0539 21.8624 12.9293 23.7377C14.8046 25.6131 17.3482 26.6667 20.0003 26.6667C22.6525 26.6667 25.196 25.6131 27.0714 23.7377C28.9468 21.8624 30.0003 19.3188 30.0003 16.6667C30.0003 16.2246 30.1759 15.8007 30.4885 15.4881C30.801 15.1756 31.225 15 31.667 15ZM20.0003 1.66666C21.7684 1.66666 23.4641 2.36904 24.7144 3.61928C25.9646 4.86952 26.667 6.56521 26.667 8.33332V16.6667C26.667 18.4348 25.9646 20.1305 24.7144 21.3807C23.4641 22.6309 21.7684 23.3333 20.0003 23.3333C18.2322 23.3333 16.5365 22.6309 15.2863 21.3807C14.036 20.1305 13.3337 18.4348 13.3337 16.6667V8.33332C13.3337 6.56521 14.036 4.86952 15.2863 3.61928C16.5365 2.36904 18.2322 1.66666 20.0003 1.66666Z"
            fill="white" />
        </svg>
      </button>



    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { v4 as uuidv4 } from 'uuid'
import Cookies from 'js-cookie';
import parseJwt from '@/utils';
import CustomAudioPlayer from './CustomAudioPlayer.vue';
import InfoIcon from '../icons/InfoIcon.vue';


const chatInput = ref('');
const messages = ref([]);
const chatSocket = ref(null);
const chatContainer = ref(null);
const route = useRoute();
const roomId = route.params.id;
let username = null;
let userId = null;
let mediaRecorder = null;
let chunks = [];

const isRecording = ref(false);

const token = Cookies.get('access_token');
if (token) {
  const decoded = parseJwt(token);
  username = decoded.username;
  userId = decoded.id_user;
}

function addMessage() {
  nextTick(() => {
    const el = chatContainer.value;
    if (el) {
      const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight <= 150;

      if (atBottom) {
        el.scrollTop = el.scrollHeight;
      }
    }
  });
}


function sendMessage() {
  if (chatSocket.value && chatInput.value.trim()) {
    const message = {
      sender: username,
      text: chatInput.value,
      time: new Date().toLocaleTimeString(),  // Текущее время в формате HH:MM:SS
    };
    chatSocket.value.send(JSON.stringify(message));
    // chatSocket.value.send(chatInput.value);
    chatInput.value = '';

  }
}

onMounted(async () => {
  try {
    const response = await axios.get(`/api/messages/room_messages/${roomId}`);
    messages.value = response.data.map(msg => ({
      sender: msg.sender || msg.username || 'Unknown',
      text: msg.text || msg.message,
      type: msg.type,
      voice_path: msg.voice_path,
      time: new Date(msg.created_at).toLocaleTimeString(),
    }));
    console.log(messages.value);
    addMessage();
  } catch (err) {
    console.error('Ошибка при загрузке сообщений:', err);
  }

  //chatSocket.value = new WebSocket(`/ws/chat/${roomId}/${userId}`);
  chatSocket.value = new WebSocket(`ws://uniview.space/ws/chat/${roomId}/${userId}`);


  chatSocket.value.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    messages.value.push({
      sender: msg.sender,
      type: msg.type || 'text',
      text: msg.text || '',
      voice_path: msg.voice_path || msg.filename,
      time: new Date().toLocaleTimeString(),
    });
    addMessage();
  };
});

onBeforeUnmount(() => {
  chatSocket.value?.close();
});

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  chunks = [];

  isRecording.value = true;

  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

  mediaRecorder.onstop = async () => {
    isRecording.value = false;

    const blob = new Blob(chunks, { type: 'audio/webm' });
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64Audio = reader.result.split(',')[1];
      const voiceMessage = {
        sender: username,
        type: 'voice',
        filename: uuidv4(),
        data: base64Audio,
        time: new Date().toISOString(),
      };
      chatSocket.value.send(JSON.stringify(voiceMessage));
    };
    reader.readAsDataURL(blob);
  };

  mediaRecorder.start();
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');

.chat {
  background: rgba(73, 59, 97, 0.729);
  border-radius: 20px;
  border: 1px solid rgba(179, 176, 185, 0.858);
  height: 100%;


}

.chat p {
  font-family: "Raleway", sans-serif;
  font-size: 20px;
  font-weight: 400;
  color: rgb(208, 208, 208);
  margin: 0;

}


.message-input {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 5px;
}

button {
  padding: 10px 20px;
  font-size: 14px;
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  color: #A6A6A6;
  background-color: rgba(174, 174, 174, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  outline: none;
  transition: all 0.3s ease-in-out;
}

button:focus {
  border-color: #634D7A;
  background-color: rgba(255, 255, 255, 0.15);
}

.my-icon {
  width: 20px;
  height: 20px;
  color: #A6A6A6;
}

.input {
  padding: 10px 20px;
  font-size: 14px;
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  color: #A6A6A6;
  background-color: rgba(174, 174, 174, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  outline: none;
  transition: all 0.3s ease-in-out;
  width: 80%;
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.input:focus {
  border-color: #634D7A;
  background-color: rgba(255, 255, 255, 0.15);
}

.messages {
  display: flex;
  flex-direction: column;
  height: 80%;
  /* или сколько нужно */
  overflow-y: auto;
  padding: 10px;
  gap: 15px;
  scrollbar-width: thin;
  /* Firefox */
}

.message-header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.mes-box {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  margin-top: 6px;
  /* вместо margin-bottom */
  border-radius: 6px;
  background-color: rgba(174, 174, 174, 0.1);
  color: #fff;
  font-size: 14px;
  font-family: "Raleway", sans-serif;
  font-weight: 400;
  color: rgb(208, 208, 208);
  margin: 0;
  gap: 10px;
}

svg.recording {
  animation: blink 1s infinite;
  fill: red !important;
}

@keyframes blink {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.3;
  }
}


/* Контейнер для голосового сообщения */
/* .voice-message {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 300px;
  transition: background 0.3s ease;
}

.voice-message:hover {
  background: rgba(255, 255, 255, 0.1);
} */

/* Скрываем дефолтный фон аудио */
/* .voice-message audio {
  width: 100%;
  height: 32px;
  outline: none;
  background: transparent;
} */

/* Убираем ненужные элементы */
/* .voice-message audio::-webkit-media-controls-panel {
  background-color: transparent;
  border-radius: 0;
}

.voice-message audio::-webkit-media-controls-enclosure {
  background-color: transparent;
  border-radius: 0;
} */

/* Стилизация прогресс-бара */
/* .voice-message audio::-webkit-media-controls-timeline {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  height: 4px;
  margin: 0 8px;
} */

/* Прогресс заполнения */
/* .voice-message audio::-webkit-media-controls-current-time-display,
.voice-message audio::-webkit-media-controls-time-remaining-display {
  color: #aaa;
  font-size: 12px;
}

.voice-message audio::-webkit-media-controls-play-button {
  filter: invert(1);
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.voice-message audio::-webkit-media-controls-play-button:hover {
  opacity: 1;
} */

.chat-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.tooltip-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: help;
  font-size: 14px;
  color: #aaa;
  
}

.tooltip-text {
  visibility: hidden;
  background-color: rgba(174, 174, 174, 0.1);
  color: #fff;
  text-align: center;
  padding: 8px 10px;
  border-radius: 5px;
  position: absolute;
  bottom: 20px;
  z-index: 1;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  white-space: nowrap;
  font-family: "Raleway", sans-serif;
  font-weight: 400;
  border: 1px solid rgba(255, 255, 255, 0.3);

}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}
</style>