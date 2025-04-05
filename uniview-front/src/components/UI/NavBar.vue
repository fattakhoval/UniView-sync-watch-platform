<template>
    <nav class="navbar">
        <div class="nav-container">
            <ul class="nav-links">
                <li><router-link to="/" class="active">Главная</router-link></li>
                <li><router-link to="/rooms">Комнаты</router-link></li>
                <li><router-link to="/friends">Друзья</router-link></li>
                <li><router-link to="/calendar">Календарь</router-link></li>
            </ul>

            <div class="nav-actions">
                <router-link to="/profile" class="nav-button" v-if="username">{{ username
                    }}</router-link>
                <router-link to="/login" class="nav-button-in" v-if="!username" >Вход</router-link>
                <router-link to="/login" v-if="username" @click="userStore.logout" class="nav-button-in">Выйти</router-link>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';
import parseJwt from '@/utils';
import Cookies from 'js-cookie';  // Можно использовать js-cookie для работы с куками

const userStore = useUserStore();
let username = null;
const token = Cookies.get('access_token');
if(token){
    const decoded = parseJwt(token);
    console.log(decoded);
    username = decoded.username;
}


// userStore.fetchUser();

const isMenuOpen = ref(false);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.navbar {
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    font-size: 14px;
    display: flex;
    padding-top: 20px;
    justify-content: center;
    width: 100%;
    /* background: rgba(30, 30, 60, 0.8); */

}

.nav-container {
    width: 90%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-links {
    background: rgba(129, 124, 151, 0.2);
    padding: 20px 60px;
    border-radius: 20px;
    display: flex;
    gap: 60px;
}

.nav-links li {
    list-style: none;
}

.nav-links a {
    text-decoration: none;
    color: #fff;
    padding: 8px 16px;
    transition: 0.3s;
}

.nav-links a:hover,
.nav-links .active {
    color: #9db358;
}

.nav-actions {
    display: flex;
    gap: 12px;
}

.nav-button {
    padding: 20px 40px;
    text-decoration: none;
    color: white;
    transition: 0.3s;
}

.nav-button-in {
    background: rgba(129, 124, 151, 0.2);
    padding: 20px 20px;
    border-radius: 20px;
    text-decoration: none;
    color: white;
    transition: 0.3s;
}

.nav-button-in:hover {
    color: #c4ff57;

}
</style>