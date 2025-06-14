<script setup>
import PeopleIcon from '@/components/icons/PeopleIcon.vue';
import LockIcon from '@/components/icons/LockIcon.vue';
import PublicRoom from '@/components/icons/PublicRoom.vue';
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';
import router from '@/router';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import MyModal from '@/components/UI/MyModal.vue';
import { useRoomStore } from '@/stores/roomStore';
import { useCookies } from "vue3-cookies";

const { cookies } = useCookies();

const rooms = ref([]);
const selectedType = ref('all'); // all | public | private
const isModalOpen = ref(false);

const roomStore = useRoomStore();
const roomName = ref('');
const roomType = ref('public');

const roomPassword = ref(''); // Поле для пароля

const errorMessage = ref("");

const searchQuery = ref('');
const filteredRooms = computed(() => {
    return rooms.value.filter(room => {
        const matchesName = room.name.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesType = selectedType.value === 'all' || room.room_type === selectedType.value;
        return matchesName && matchesType;
    });
});

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
            // location.href='/room/'+room.id;
            // router.push(`/room/${room.id}`); // Перенаправление на созданную комнату
        }
    } catch (error) {
        console.error('Ошибка при создании комнаты:', error);
    }
};

// Функция сброса состояния
const resetModal = () => {
    roomName.value = '';
    roomType.value = 'public';
    roomPassword.value = '';
    isModalOpen.value = false;
};

const enterRoom = async (room) => {
    // if (room.room_type === 'private') {
    //     const enteredPassword = prompt("Введите пароль для приватной комнаты:");
    //     if (!enteredPassword) return;

    //     try {
    //         const res = await fetch(`http://localhost:8000/rooms/verify_password`, {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({ room_id: room.id, password: enteredPassword }),
    //         });

    //         if (!res.ok) {
    //             alert("Неверный пароль.");
    //             return;
    //         }

    //         cookies.set("room_password", enteredPassword);
    //         router.push(`/room/${room.id}`);
    //     } catch (error) {
    //         console.error("Ошибка при проверке пароля:", error);
    //     }
    // } else {
        router.push(`/room/${room.id}`);
    
};


// const enterRoom = async (room) => {
//   if (room.room_type === 'private') {
//     const savedPassword = cookies.get(`room_${room.id}_password`);
//     if (!savedPassword) {
//       const inputPassword = prompt('Введите пароль для приватной комнаты:');
//       if (!inputPassword) return;
//       try {
//         const res = await roomStore.joinRoom(room.id, inputPassword);
//         cookies.set(`room_${room.id}_password`, inputPassword); // Сохраняем для автоперехода в будущем
//         router.push(`/room/${room.id}`);
//       } catch (err) {
//         alert('Неверный пароль или ошибка при входе');
//       }
//     } else {
//       try {
//         const res = await roomStore.joinRoom(room.id, savedPassword);
//         router.push(`/room/${room.id}`);
//       } catch (err) {
//         cookies.remove(`room_${room.id}_password`);
//         alert('Сохранённый пароль неверен. Попробуйте снова.');
//       }
//     }
//   } else {
//     // Публичная комната — просто переходим
//     router.push(`/room/${room.id}`);
//   }
// };




const fetchRooms = async () => {
    try {
        const res = await fetch('http://localhost:8000/rooms/get_rooms');
        const data = await res.json();
        rooms.value = data;
    } catch (err) {
        console.error('Ошибка при получении комнат:', err);
    }
};

const getRoomIcon = (type) => {
    console.log(type);
    return type === 'public' ? PublicRoom : LockIcon;
};

onMounted(() => {
    fetchRooms();
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

        <div class="rooms">
            <div class="rooms-box">




                <div class="room_search">
                    <div class="room_search_l">
                        <input type="text" placeholder="Найти комнату" v-model="searchQuery">
                        <select v-model="selectedType" class="room-filter">
                            <option value="all">Все</option>
                            <option value="public">Публичные</option>
                            <option value="private">Приватные</option>
                        </select>

                    </div>


                    <MyButton class="create-room" @click="isModalOpen = true">
                        Создать комнату
                    </MyButton>
                </div>

                <div class="room-list">
                    <div class="room-card" v-for="room in filteredRooms" :key="room.id" @click="enterRoom(room)">
                        <div class="room-title">
                            <h3 class="h3">{{ room.name }}</h3>
                            <span>

                                <component :is="getRoomIcon(room.room_type)" class="icon" />
                                <!-- <PublicRoom class="icon"/> -->

                            </span>
                        </div>

                        <div class="room-inf">
                            <div class="peoples">
                                <PeopleIcon class="icon-gray" /> Участники комнаты
                            </div>
                            <div class="room-count">{{ room.count }}</div>
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

.rooms {
    display: flex;
    justify-content: center;
    align-items: center;


}

.rooms-box {

    /* gap: 20px; */
    width: 90%;

}

.room_search {
    display: flex;
    flex: 1;
    justify-content: space-between;
    margin-bottom: 40px;
}

.room_search_l {
    display: flex;
    flex: 1;
    gap: 20px;
    align-items: center;
    margin-bottom: 40px;
}

.room_search input {
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 300;
    color: #f1f1f1;
    background-color: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease-in-out;
    width: 50%;
}

.room_search input::placeholder {
    color: rgba(236, 236, 236, 0.799);
}

.room_search input:focus {
    border-color: #634D7A;
    background-color: var(--input-focus);

}

.create-room {

    border-radius: 10px;
    padding: 5px 10px;
    height: 40px;
}

.room-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 35px;
    /* justify-items: center; */


}

.room-card {
    background: rgba(108, 103, 128, 0.2);
    border-radius: 20px;
    border: 1px solid var(--block-border);
    width: 400px;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 30px;
    align-items: center;
    color: #fff;
    font-family: "Raleway", sans-serif;
    font-size: 16px;
    font-weight: 400;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.room-card:hover {
  transform: scale(1.02);
}

.room-title,
.room-inf {
    width: 90%;
    display: flex;
    justify-content: space-between;
    align-items: center;

}

.room-title .h3 {
    margin: 0;
}

.room-inf .icon-gray {
    width: 20px;
    height: 20px;
    fill: var(--text-p);
}

.room-inf .peoples {
    display: flex;
    align-items: center;
    color: var(--text-p);
    gap: 10px;
}

.room-inf .room-count {
    padding: 2px 15px;
    background: #8a8a8a80;
    border: none;
    border-radius: 10px;

}

.room-filter {
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Montserrat Alternates", sans-serif;
    color: #ececec;
    background-color: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease-in-out;
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

    .room_search {
    display: block;
    flex: 1;
    gap: 20px;
    align-items: center;
    margin-bottom: 40px;
}

.room-card {
    width: 85%;
}
}

.error-message {
    color: #ff6b6b;
    margin-top: 10px;
    text-align: center;
    width: 100%;
}
</style>