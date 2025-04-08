<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Бургер -->
      <div class="burger" @click="isMenuOpen = !isMenuOpen">
        <span :class="{ open: isMenuOpen }"></span>
        <span :class="{ open: isMenuOpen }"></span>
        <span :class="{ open: isMenuOpen }"></span>
      </div>

      <!-- Навигация -->
      <ul class="nav-links" :class="{ open: isMenuOpen }">
        <li><router-link to="/" class="active">Главная</router-link></li>
        <li><router-link to="/rooms">Комнаты</router-link></li>
        <li><router-link to="/friends">Друзья</router-link></li>
        <li><router-link to="/calendar">Календарь</router-link></li>
      </ul>

      <!-- Кнопки -->
      <div class="nav-actions">
        <router-link to="/profile" class="nav-button" v-if="username">{{ username }}</router-link>
        <router-link to="/login" class="nav-button-in" v-if="!username">Вход</router-link>
        <button v-if="username" @click="userStore.logout" class="nav-button-in">Выйти</button>
        <!-- <router-link to="/login" v-if="username" @click="userStore.logout" class="nav-button-in">Выйти</router-link> -->
      </div>
    </div>
  </nav>
</template>


<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import parseJwt from '@/utils';
import Cookies from 'js-cookie';  // Можно использовать js-cookie для работы с куками

const userStore = useUserStore();

const username = computed(() => {
  const token = Cookies.get('access_token');
  if (token) {
    const decoded = parseJwt(token);
    return decoded.username;
  }
  return null;
});


// userStore.fetchUser();

const isMenuOpen = ref(false);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:wght@400;500;600&display=swap');

.navbar {
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 500;
  font-size: 14px;
  display: flex;
  justify-content: center;
  padding: 20px 0;
  width: 100%;
  position: relative;
}

.nav-container {
  width: 90%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

/* Навигация */
.nav-links {
  background: rgba(129, 124, 151, 0.2);
  padding: 20px 60px;
  border-radius: 20px;
  display: flex;
  gap: 60px;
  list-style: none;
  transition: all 0.3s ease;
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

/* Кнопки */
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
  border: none;
  border-radius: 20px;
  text-decoration: none;
  color: white;
  transition: 0.3s;
}

.nav-button-in:hover {
  color: #c4ff57;
}

/* Бургер-меню */
.burger {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
  cursor: pointer;
}

.burger span {
  display: block;
  height: 3px;
  width: 100%;
  background-color: white;
  border-radius: 3px;
  transition: all 0.3s ease;
}

/* transform при открытии */
.burger span.open:nth-child(1) {
  transform: translateY(7.5px) rotate(45deg);
}

.burger span.open:nth-child(2) {
  opacity: 0;
}

.burger span.open:nth-child(3) {
  transform: translateY(-7.5px) rotate(-45deg);
}

/* Мобильная адаптация */
@media (max-width: 768px) {
  .nav-links {
    position: absolute;
    top: 70px;
    left: 0;
    width: 100%;
    flex-direction: column;
    background-color: rgba(30, 30, 60, 0.95);
    padding: 20px 0;
    gap: 20px;
    display: none;
  }

  .nav-links.open {
    display: flex;
    z-index: 99;
  }

  .burger {
    display: flex;
  }

  .nav-actions {
    font-size: 10px;
  }

  .nav-button-in {
    font-size: 10px;

  }
}
</style>
