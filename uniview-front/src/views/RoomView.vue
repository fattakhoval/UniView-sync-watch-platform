<script setup>
import AddVideo from '@/components/UI/AddVideo.vue';
import MyButton from '@/components/UI/MyButton.vue';
import MyChat from '@/components/UI/MyChat.vue';
import NavBar from '@/components/UI/NavBar.vue';

import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';
import router from '@/router';
import VideoComponent from '@/components/UI/VideoComponent.vue';

const route = useRoute();
const roomId = route.params.id;
const inviteLink = ref('');

const roomName = ref('');
const roomTitle = ref('');

// Получаем название комнаты из куки
onMounted(() => {
  const storedRoomName = Cookies.get(`room_info${roomId}`);
  if (storedRoomName) {
    roomName.value = JSON.parse(storedRoomName);
    document.title = `Комната: ${roomName.value.name}`;

  } else {
    roomName.value = 'Комната не найдена';
  }
});


async function checkRoomAccess(roomId) {
    const room_info = Cookies.get(`room_info${roomId}`);
    const token = Cookies.get('access_token');

if (!token) {
  router.push('/');
}
    
    if (!room_info) {
        const inputPassword = prompt('Введите пароль для комнаты:');
        if (!inputPassword) {
            alert('Пароль обязателен!');
            router.push('/'); // Если пароль не введён, перенаправляем на главную
            return;
        }
        try{
            const response = await axios.post('http://127.0.0.1:8000/rooms/join_room', {
                room_id: roomId,
                password: inputPassword
            }, { headers: { 'Content-Type': 'application/json' } });
            console.log(`AAAAAA ${response.data.room.id}`);
            //Cookies.set(`room_password${roomId}`, inputPassword, { expires: 1 });
        }
        catch (error) {
            console.error('Ошибка при подключении комнаты: Not access password');
            if (!error.response.data.access) {
                alert('Неверный пароль!');
                router.push('/'); // Если пароль неверный, возвращаем на главную
            }
        }
    }
}

// Генерация ссылки на текущую комнату
function generateInviteLink() {
  const link = `${window.location.origin}/room/${roomId}`; // ссылка на текущую комнату
  inviteLink.value = link;
  copyToClipboard(link); // Автоматически копируем ссылку в буфер обмена
}

// Копирование ссылки в буфер обмена
function copyToClipboard(text) {
  const el = document.createElement('textarea');
  el.value = text;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
  alert('Ссылка скопирована в буфер обмена!');
}

// Запускаем проверку при загрузке компонента
onMounted(() => {
    checkRoomAccess(roomId);
});


// const roomId = route.params.room_id;
// const roomPassword = ref(cookies.get("room_password") || "");
// const roomType = ref(cookies.get("room_type") || "public");
// const error = ref(null);
// const loading = ref(true);
// const showPasswordInput = ref(false);

// const joinRoom = async () => {
//     try {
//         const response = await axios.post(
//             "http://127.0.0.1:8000/rooms/join_room",
//             { room_id: roomId, password: roomPassword.value },
//             { headers: { "Content-Type": "application/json" } } // <-- Явно указываем JSON
//         );

//         if (!response.data.access) {
//             throw new Error("Доступ запрещен");
//         }

//         // Сохраняем пароль в cookies, если он был введён вручную
//         if (roomPassword.value) {
//             cookies.set("room_password", roomPassword.value, "1h");
//         }

//         error.value = null;
//     } catch (err) {
//         error.value = err.response?.data?.detail || "Ошибка входа";
//         showPasswordInput.value = true;
//     } finally {
//         loading.value = false;
//     }
// };

// onMounted(() => {
//     if (roomType.value === "private" && !roomPassword.value) {
//         showPasswordInput.value = true;
//     } else {
//         joinRoom();
//     }
// });


</script>

<template>
    <div class="container">

        <div v-if="loading">Загрузка...</div>
        <NavBar />

        <div v-if="error">
        <p class="error-message">{{ error }}</p>
        <input v-model="roomPassword" type="password" placeholder="Введите пароль" v-if="showPasswordInput" />
        <button @click="joinRoom" v-if="showPasswordInput">Войти</button>
    </div>

        <div class="room-info">
            <h3>Комната: {{ roomName.name }}</h3>

            <MyButton class="share-btn"  @click="generateInviteLink">
                Пригласить
            </MyButton>





        </div>

        <AddVideo />

        <div class="cine-container">
            <div class="cine-box">
                    <VideoComponent />

                <div class="chat-box">
                    <MyChat />
                </div>
            </div>
        </div>


    </div>

    <div class="page-container">
    </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.container {
    position: absolute;
    z-index: 5;
    min-width: 99%;
    max-width: 100%;
    overflow: hidden;
}

.room-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 30px;
    height: 50px;
}

.room-info h3 {
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 400;
    font-style: normal;
    font-size: 26px;
    color: #fff;
}

.share-btn {

    width: 120px;
    height: 40px;
}

.cine-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 20px;
}

.cine-box {
    width: 100%;
    height: 600px;
    display: flex;
    justify-content: space-between;

}

.chat-box {
    width: 23%;
    height: 80%;

}

.chat {
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.video {
    width: 100%;
    height: 100%;

    background-color: black;
}

.video-player {
    width: 75%;
    height: 100%;

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
</style>