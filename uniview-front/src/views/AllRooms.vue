<script setup>
import PeopleIcon from '@/components/icons/PeopleIcon.vue';
import LockIcon from '@/components/icons/LockIcon.vue';
import PublicRoom from '@/components/icons/PublicRoom.vue';
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';
import router from '@/router';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const rooms = ref([]);

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
        <NavBar />

        <div class="rooms">
            <div class="rooms-box">




                <div class="room_search">
                    <input type="text" placeholder="Найти комнату">
                    <MyButton class="create-room">
                        Создать комнату
                    </MyButton>
                </div>

                <div class="room-list">
                    <div class="room-card" v-for="room in rooms" :key="room.id">
                        <div class="room-title">
                            <h3 class="h3">{{ room.name }}</h3>
                            <span>

                                <component :is="getRoomIcon(room.room_type)" class="icon" />
                                <!-- <PublicRoom class="icon"/> -->

                            </span>
                        </div>

                        <div class="room-inf">
                            <div  class="peoples"><PeopleIcon class="icon-gray"/> Участники комнаты</div>
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
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}

.room_search input {
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 300;
    color: #A6A6A6;
    background-color: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease-in-out;
    width: 50%;
}

.room_search input::placeholder {
    color: rgba(255, 255, 255, 0.6);
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
    grid-template-columns: repeat(auto-fill, minmax(440px, 1fr));
    gap: 40px;
    justify-items: center;


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
}

.room-title, .room-inf {
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
</style>