<template>
  <div class="chat">
    <p>ЧАТ</p>

    <div ref="chatContainer" class="messages">
      <div class="mes-box" v-for="(msg, index) in messages" :key="index">{{ msg }}</div>
    </div>

    <div class="message-input">
      <input class="input" v-model="chatInput" @keyup.enter="sendMessage" placeholder="Введите сообщение..." />
      <button @click="sendMessage">></button>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute } from 'vue-router';


const chatInput = ref('');
const messages = ref([]);
const chatSocket = ref(null);
const route = useRoute();


const roomId = route.params.id;

const chatContainer = ref(null);

function addMessage() {
  nextTick(() => {
    const el = chatContainer.value;
    if (el) {
        const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight <= 50;
      
      if (atBottom) {
        el.scrollTop = el.scrollHeight;
      }
    }
  });
}


function sendMessage() {
  if (chatSocket.value && chatInput.value.trim()) {
    chatSocket.value.send(chatInput.value);
    chatInput.value = '';
    
  }
}

onMounted(() => {
  chatSocket.value = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}`);

  chatSocket.value.onmessage = (event) => {
    messages.value.push(event.data);
    addMessage();
  };
});

onBeforeUnmount(() => {
  chatSocket.value?.close();
});

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
  scrollbar-width: thin; /* Firefox */
}

.mes-box {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-top: 6px; /* вместо margin-bottom */
  border-radius: 6px;
  background-color: rgba(174, 174, 174, 0.1);
  color: #fff;
  font-size: 14px;
}
</style>