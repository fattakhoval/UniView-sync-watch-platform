<template>
  <div class="chat">
    <p>ЧАТ</p>

    <div ref="chatContainer" class="messages">
      <div class="mes-box" v-for="(msg, index) in messages" :key="index">
        <div class="message-header">
          <span class="sender">{{ msg.sender }}</span>
          <span class="time">{{ msg.time }}</span>
        </div>
        <div class="message-text">
          <template v-if="msg.type === 'voice' && msg.voice_path">
            <audio controls :src="`http://localhost:8000/messages/voices/${msg.voice_path}`"></audio>
          </template>
          <template v-else>
            {{ msg.text }}
          </template>
        </div>
      </div>
    </div>

    <div class="message-input">
      <input class="input" v-model="chatInput" @keyup.enter="sendMessage" placeholder="Введите сообщение..." />
      <button @click="sendMessage">></button>
      <button @mousedown="startRecording" @mouseup="stopRecording">🎤</button>
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


const chatInput = ref('');
const messages = ref([]);
const chatSocket = ref(null);
const chatContainer = ref(null);
const route = useRoute();
const roomId = route.params.id;
let username = null;
let mediaRecorder = null;
let chunks = [];

const token = Cookies.get('access_token');
if (token) {
  const decoded = parseJwt(token);
  username = decoded.username;
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
    const response = await axios.get(`http://localhost:8000/messages/room_messages/${roomId}`);
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

  chatSocket.value = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}`);

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

  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

  mediaRecorder.onstop = async () => {
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

<style>
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
  height: 80%; /* или сколько нужно */
  overflow-y: auto;
  padding: 10px;
  gap: 15px;
  scrollbar-width: thin; /* Firefox */
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
  margin-top: 6px; /* вместо margin-bottom */
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
</style>