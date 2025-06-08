<script setup>
import axios from 'axios';
import NavBar from '@/components/UI/NavBar.vue';
import MyButton from '@/components/UI/MyButton.vue';
import BlocksIcon from '@/components/UI/BlocksIcon.vue';
import BlockHr from '@/components/UI/BlockHr.vue';
import MyModal from '@/components/UI/MyModal.vue';

import { ref, onMounted } from 'vue';
import { useCookies } from "vue3-cookies";
import { useRoomStore } from '@/stores/roomStore';
import { useRouter } from 'vue-router';

import CameraIcon from '@/components/icons/CameraIcon.vue';
import CodeIcon from '@/components/icons/CodeIcon.vue';
import ShareIcon from '@/components/icons/ShareIcon.vue';
import PeopleIcon from '@/components/icons/PeopleIcon.vue';
import PlayIcon from '@/components/icons/PlayIcon.vue';

const { cookies } = useCookies();
const router = useRouter();
const roomLink = ref('');
const isModalOpen = ref(false);

const roomStore = useRoomStore();
const roomName = ref('');
const roomType = ref('public');
const roomPassword = ref(''); // Поле для пароля

const errorMessage = ref("");
const isLoading = ref(false);

// Функция для валидации
const validateForm = () => {
  if (!roomName.value) {
    errorMessage.value = "Название комнаты не может быть пустым.";
    return false;
  }
  if (roomName.value.length > 30) {
    errorMessage.value = "Название комнаты не может быть длиннее 30 символов.";
    return false;
  }
  if (roomType.value === 'private' && roomPassword.value.length < 3) {
    errorMessage.value = "Пароль должен быть не менее 3 символов.";
    return false;
  }
  return true;
};

// Функция создания комнаты
const createRoom = async () => {
  // Проверяем, что форма прошла валидацию
  if (!validateForm()) {
    return;
  }

  const token = cookies.get('access_token');

  if (!token) {
    errorMessage.value = "Вы должны быть авторизованы, чтобы создать комнату.";
    return;
  }

  const data = {
    name: roomName.value,
    type: roomType.value,
    password: roomType.value === 'private' ? roomPassword.value : null, // Пароль только если приватная
  };

  try {
    const room = await roomStore.createRoom(data.name, data.type, data.password);

    if (room && room.id) {
      resetModal(); // Сброс модального окна
 
    }
  } catch (error) {
    console.error('Ошибка при создании комнаты:', error);
  }
};

// Обработчик для кнопки "Войти в комнату"
const joinRoom = () => {

  const link = roomLink.value.trim();
  // Паттерн для допустимых ссылок (можно адаптировать под структуру твоего проекта)
  const roomLinkRegex = /(\/room\/|room\/)?([a-zA-Z0-9_-]{6,})$/;

  // Извлекаем ID комнаты из введенной ссылки
  const roomId = roomLink.value.split('/').pop(); // Предполагаем, что ссылка вида "/room/ID"

  const match = link.match(roomLinkRegex);
  if (match && match[2]) {
    const roomId = match[2];
    // Переходим на страницу комнаты с указанным ID
    router.push(`/room/${roomId}`);
  } else {
    alert('Неверная ссылка на комнату');
  }
};

// Функция сброса состояния
const resetModal = () => {
  roomName.value = '';
  roomType.value = 'public';
  roomPassword.value = '';
  isModalOpen.value = false;
};


onMounted(() => {
  document.title = `UniView`;
});

</script>

<template>
  <div class="container">

    <MyModal :isOpen="isModalOpen" @close="resetModal">
      <div class="modal-content">
        <p class="modal-title">Создание комнаты</p>

        <label class="input-label">Название комнаты</label>
        <input v-model="roomName" type="text" class="modal-input" placeholder="Введите название..." />

        <div class="radio-group">
          <label class="radio-label">
            <input type="radio" name="roomType" value="public" v-model="roomType" />
            <span class="custom-radio"></span>
            Публичная
          </label>
          <label class="radio-label">
            <input type="radio" name="roomType" value="private" v-model="roomType" />
            <span class="custom-radio"></span>
            Приватная
          </label>
        </div>

        <input v-if="roomType === 'private'" v-model="roomPassword" type="password" placeholder="Введите пароль"
          class="input fade-in" />

        <MyButton class="create-btn" @click="createRoom">
          Создать комнату
        </MyButton>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>


      </div>
    </MyModal>

    <NavBar />

    <div class="main-info">



      <div class="main">
        <div class="logo-info">
          <h1>UniView</h1>
          <p>Смотрите видео с друзьями в идеальной синхронизации. Делитесь моментами, реагируйте вместе и никогда не
            пропускайте ни одного момента</p>

          <div class="info-blocks">
            <BlocksIcon>
              <template #block-icon>
                <CameraIcon class="my-icon" />
                <!-- <img src="@/assets/camera.svg" width="50px" /> -->

              </template>
              Идеальная синхронизация
            </BlocksIcon>

            <BlocksIcon>
              <template #block-icon>
                <PeopleIcon class="my-icon" />
              </template>
              Совместный просмотр
            </BlocksIcon>

            <BlocksIcon>
              <template #block-icon>
                <ShareIcon class="my-icon" />
              </template>
              Легко делиться
            </BlocksIcon>

            <BlocksIcon>
              <template #block-icon>
                <CodeIcon class="my-icon" />
              </template>
              Смотрите любые видео
            </BlocksIcon>
          </div>
        </div>

        <div class="create-room">
          <div class="btn-form">
            <div class="block-text">
              <p class="p1">Смотри Прямо Сейчас</p>
              <p class="p2">Создай комнату или присоединяйся к друзьям</p>
            </div>


            <div class="btn-group">
              <MyButton @click="isModalOpen = true">

                <template #icon>
                  <PlayIcon class="play-icon" />
                </template>
                Создать Комнату
              </MyButton>

              <BlockHr>
                ИЛИ
              </BlockHr>

              <input v-model="roomLink" type="text" class="input" placeholder="Ссылка на комнату">
              <button class="btn-in" @click="joinRoom">Войти в комнату</button>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>

  <div class="page-container">
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.container {
  position: absolute;
  z-index: 5;
  min-width: 99%;
  max-width: 100%;
  overflow: hidden;
}

.main-info {
  display: flex;
  justify-content: center;
  align-items: center;


}

.main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* gap: 20px; */
  width: 90%;

}

.logo-info {
  width: 550px;
  display: flex;
  flex-direction: column;
  padding-top: 5%;
  gap: 30px;
}

.logo-info h1 {
  font-family: "Raleway", sans-serif;
  font-size: 100px;
  font-weight: 400;
  color: var(--accent-color);
  margin: 0;

}

.logo-info p {
  font-family: "Raleway", sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: var(--text-p);
  line-height: 140%;

}

.info-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.my-icon {
  width: 50px;
  height: 50px;
  fill: var(--icon-color);
  /* или color, если используется currentColor */
  transition: fill 0.3s ease;
}

.btn-form {
  background: rgba(108, 103, 128, 0.2);
  border-radius: 20px;
  border: 1px solid var(--input-border);
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  gap: 40px;

}

.btn-form .p1 {
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 500;
  font-style: normal;
  font-size: 18px;
  color: var(--p1);
}

.btn-form .p2 {
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  font-style: normal;
  font-size: 14px;
  color: var(--p2);
}

.btn-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 30px;
}

.input {
  padding: 20px 40px;
  font-size: 14px;
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  color: #A6A6A6;
  background-color: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 15px;
  outline: none;
  transition: all 0.3s ease-in-out;
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.input:focus {
  border-color: #634D7A;
  background-color: var(--input-focus);
  
}

.btn-in {
  background-color: var(--btn-in);
  color: var(--btn-in-text);
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 500;
  font-style: normal;
  padding: 20px 40px;
  border-radius: 15px;
  border: 1px solid rgba(213, 210, 210, 0.3);
  cursor: pointer;
  transition: background 0.3s ease;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
}

.btn-in:hover {
  background-color: var(--btn-in-hover);

}

/* модальное окно */

.modal-title {
  font-family: "Raleway", sans-serif;
  font-size: 26px;
  font-weight: 600;
  color: #a3bd5d;
}

.modal-content {
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  font-style: normal;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  color: #fff;
}



.modal-input {
  padding: 15px 30px;
  font-size: 12px;
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 300;
  color: #A6A6A6;
  background-color: rgba(174, 174, 174, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  outline: none;
  transition: all 0.3s ease-in-out;
}

.modal-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.modal-input:focus {
  border-color: #634D7A;
  background-color: rgba(255, 255, 255, 0.15);
}

.create-btn {
  padding: 15px 30px;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  cursor: pointer;
  position: relative;
}

/* Скрываем стандартные radio */
.radio-label input[type="radio"] {
  display: none;
}

/* Кастомный круг */
.custom-radio {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #634D7A;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

/* Внутренний кружок */
.custom-radio::after {
  content: "";
  width: 12px;
  height: 12px;
  background-color: #8DA04E;
  border-radius: 50%;
  transform: scale(0);
  transition: transform 0.3s ease;
}

/* При выборе радио-кнопки */
.radio-label input[type="radio"]:checked+.custom-radio {
  border-color: #3a2a50;
}

.radio-label input[type="radio"]:checked+.custom-radio::after {
  transform: scale(1);
}

@media (max-width: 768px) {
  .main {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 40px;
    width: 90%;
  }

  .logo-info {
    width: 100%;
    padding: 0 20px;
  }

  .logo-info h1 {
    font-size: 48px;
  }

  .logo-info p {
    font-size: 14px;
  }

  .info-blocks {
    justify-content: center;
    gap: 15px;
    margin-right: 10px;
  }

  .btn-form {
    padding: 30px 20px;
    width: 85%;
  }

  .btn-group {
    gap: 20px;
  }


  .btn-in {
    width: 100%;
    padding: 15px 20px;
  }

  .modal-content {
    padding: 10px;
  }


  .create-btn {
    width: 100%;
  }

  .radio-group {
    flex-direction: column;
    align-items: flex-start;
  }
}

.error-message {
  color: #ff6b6b;
  margin-top: 10px;
  text-align: center;
  width: 100%;
}
</style>
