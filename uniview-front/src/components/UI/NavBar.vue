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
        <li><router-link to="/schedule">Календарь</router-link></li>
        <li class="theme-toggle" @click="themeStore.toggleTheme">
          <span class="theme-icon" :class="themeStore.theme">

            <svg v-if="themeStore.theme === 'light'" class="icon" width="40" height="40" viewBox="0 0 50 50" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M25 39.5833C25.5525 39.5833 26.0824 39.8028 26.4731 40.1935C26.8638 40.5842 27.0833 41.1141 27.0833 41.6666V43.75C27.0833 44.3025 26.8638 44.8324 26.4731 45.2231C26.0824 45.6138 25.5525 45.8333 25 45.8333C24.4474 45.8333 23.9175 45.6138 23.5268 45.2231C23.1361 44.8324 22.9166 44.3025 22.9166 43.75V41.6666C22.9166 41.1141 23.1361 40.5842 23.5268 40.1935C23.9175 39.8028 24.4474 39.5833 25 39.5833ZM38.2583 35.3125L39.7312 36.7854C40.1107 37.1783 40.3207 37.7046 40.316 38.2508C40.3112 38.797 40.0921 39.3196 39.7058 39.7058C39.3196 40.0921 38.797 40.3112 38.2508 40.3159C37.7046 40.3207 37.1783 40.1107 36.7854 39.7312L35.3125 38.2583C34.933 37.8654 34.723 37.3391 34.7277 36.7929C34.7325 36.2466 34.9516 35.7241 35.3378 35.3378C35.7241 34.9516 36.2466 34.7325 36.7929 34.7277C37.3391 34.723 37.8654 34.933 38.2583 35.3125ZM11.7416 35.3125C12.1165 34.9388 12.6196 34.7219 13.1487 34.7057C13.6777 34.6896 14.1931 34.8754 14.5901 35.2255C14.9871 35.5756 15.236 36.0636 15.2862 36.5905C15.3364 37.1175 15.1842 37.6437 14.8604 38.0625L14.6875 38.2583L13.2146 39.7312C12.8396 40.1049 12.3366 40.3218 11.8075 40.3379C11.2784 40.3541 10.7631 40.1683 10.3661 39.8182C9.96905 39.4681 9.72017 38.9801 9.66997 38.4531C9.61978 37.9262 9.77203 37.3999 10.0958 36.9812L10.2687 36.7854L11.7416 35.3125ZM25 12.5C28.3152 12.5 31.4946 13.8169 33.8388 16.1611C36.183 18.5053 37.5 21.6848 37.5 25C37.5 28.3152 36.183 31.4946 33.8388 33.8388C31.4946 36.183 28.3152 37.5 25 37.5C21.6848 37.5 18.5053 36.183 16.1611 33.8388C13.8169 31.4946 12.5 28.3152 12.5 25C12.5 21.6848 13.8169 18.5053 16.1611 16.1611C18.5053 13.8169 21.6848 12.5 25 12.5ZM25 16.6666C22.7898 16.6666 20.6702 17.5446 19.1074 19.1074C17.5446 20.6702 16.6666 22.7898 16.6666 25C16.6666 27.2101 17.5446 29.3297 19.1074 30.8925C20.6702 32.4553 22.7898 33.3333 25 33.3333C27.2101 33.3333 29.3297 32.4553 30.8925 30.8925C32.4553 29.3297 33.3333 27.2101 33.3333 25C33.3333 22.7898 32.4553 20.6702 30.8925 19.1074C29.3297 17.5446 27.2101 16.6666 25 16.6666ZM8.3333 22.9166C8.8643 22.9172 9.37504 23.1205 9.76115 23.4851C10.1473 23.8496 10.3796 24.3478 10.4107 24.8779C10.4419 25.408 10.2694 25.9299 9.92859 26.3371C9.58777 26.7443 9.10434 27.006 8.57705 27.0687L8.3333 27.0833H6.24997C5.71897 27.0827 5.20824 26.8794 4.82212 26.5149C4.436 26.1503 4.20365 25.6521 4.17253 25.1221C4.14141 24.592 4.31388 24.07 4.65469 23.6628C4.9955 23.2556 5.47894 22.9939 6.00622 22.9312L6.24997 22.9166H8.3333ZM43.75 22.9166C44.3025 22.9166 44.8324 23.1361 45.2231 23.5268C45.6138 23.9175 45.8333 24.4474 45.8333 25C45.8333 25.5525 45.6138 26.0824 45.2231 26.4731C44.8324 26.8638 44.3025 27.0833 43.75 27.0833H41.6666C41.1141 27.0833 40.5842 26.8638 40.1935 26.4731C39.8028 26.0824 39.5833 25.5525 39.5833 25C39.5833 24.4474 39.8028 23.9175 40.1935 23.5268C40.5842 23.1361 41.1141 22.9166 41.6666 22.9166H43.75ZM10.2687 10.2687C10.6275 9.91001 11.1047 9.69453 11.6111 9.66269C12.1174 9.63086 12.6179 9.78485 13.0187 10.0958L13.2146 10.2687L14.6875 11.7416C15.0611 12.1165 15.278 12.6196 15.2942 13.1487C15.3104 13.6777 15.1245 14.1931 14.7745 14.5901C14.4244 14.9871 13.9363 15.236 13.4094 15.2862C12.8825 15.3364 12.3562 15.1842 11.9375 14.8604L11.7416 14.6875L10.2687 13.2145C9.87816 12.8239 9.65875 12.2941 9.65875 11.7416C9.65875 11.1892 9.87816 10.6594 10.2687 10.2687ZM39.7312 10.2687C40.1218 10.6594 40.3412 11.1892 40.3412 11.7416C40.3412 12.2941 40.1218 12.8239 39.7312 13.2145L38.2583 14.6875C38.0661 14.8864 37.8362 15.0452 37.5821 15.1543C37.3279 15.2635 37.0545 15.321 36.7779 15.3234C36.5013 15.3258 36.2269 15.2731 35.9709 15.1683C35.7149 15.0636 35.4823 14.9089 35.2866 14.7133C35.091 14.5177 34.9363 14.2851 34.8316 14.029C34.7268 13.773 34.6741 13.4987 34.6765 13.222C34.6789 12.9454 34.7364 12.672 34.8456 12.4179C34.9548 12.1637 35.1135 11.9338 35.3125 11.7416L36.7854 10.2687C37.1761 9.87814 37.7059 9.65874 38.2583 9.65874C38.8107 9.65874 39.3405 9.87814 39.7312 10.2687ZM25 4.16663C25.5525 4.16663 26.0824 4.38612 26.4731 4.77682C26.8638 5.16752 27.0833 5.69743 27.0833 6.24996V8.33329C27.0833 8.88583 26.8638 9.41573 26.4731 9.80643C26.0824 10.1971 25.5525 10.4166 25 10.4166C24.4474 10.4166 23.9175 10.1971 23.5268 9.80643C23.1361 9.41573 22.9166 8.88583 22.9166 8.33329V6.24996C22.9166 5.69743 23.1361 5.16752 23.5268 4.77682C23.9175 4.38612 24.4474 4.16663 25 4.16663Z"
                fill="white" />
            </svg>
            <svg v-else width="40" height="40" viewBox="0 0 45 45" class="icon" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"
                stroke-width="2"
                d="M20.6569 5.25375C17.4023 5.60173 14.3127 6.86354 11.745 8.89335C9.17736 10.9232 7.23647 13.6381 6.14666 16.7244C5.05686 19.8108 4.86263 23.1425 5.58643 26.3345C6.31022 29.5266 7.92249 32.4487 10.2369 34.7631C12.5513 37.0775 15.4734 38.6898 18.6655 39.4136C21.8575 40.1374 25.1892 39.9431 28.2756 38.8533C31.3619 37.7635 34.0768 35.8226 36.1066 33.255C38.1365 30.6873 39.3983 27.5977 39.7462 24.3431C38.5582 25.8526 37.0638 27.0932 35.3614 27.9831C33.659 28.873 31.7874 29.3919 29.8698 29.5058C27.9522 29.6197 26.0323 29.3258 24.2366 28.6437C22.4409 27.9615 20.8101 26.9065 19.4518 25.5482C18.0935 24.1899 17.0385 22.5591 16.3563 20.7634C15.6742 18.9677 15.3803 17.0478 15.4942 15.1302C15.6081 13.2126 16.127 11.341 17.0169 9.6386C17.9068 7.93622 19.1474 6.44177 20.6569 5.25375ZM2.34375 22.5C2.34375 11.3681 11.3681 2.34375 22.5 2.34375C23.8444 2.34375 24.5156 3.41438 24.6319 4.2675C24.7425 5.08875 24.4388 6.13313 23.4956 6.70313C22.0949 7.54849 20.9049 8.70155 20.0159 10.075C19.1268 11.4484 18.562 13.0061 18.3642 14.6301C18.1664 16.2542 18.3408 17.902 18.8742 19.4486C19.4076 20.9953 20.286 22.4003 21.4429 23.5571C22.5997 24.714 24.0047 25.5924 25.5514 26.1258C27.098 26.6592 28.7458 26.8336 30.3699 26.6358C31.9939 26.438 33.5516 25.8732 34.925 24.9841C36.2985 24.0951 37.4515 22.9051 38.2969 21.5044C38.8669 20.5612 39.9113 20.2575 40.7325 20.3681C41.5856 20.4844 42.6562 21.1556 42.6562 22.5C42.6562 33.6319 33.6319 42.6562 22.5 42.6562C11.3681 42.6562 2.34375 33.6319 2.34375 22.5Z"
                fill="white" />
            </svg>

          </span>
        </li>
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
import { useThemeStore } from '@/stores/themeStore';

const themeStore = useThemeStore();
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
  align-items: center;
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
  color: var(--accent-color);
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

.theme-toggle {
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: color 0.3s;
}

.theme-icon {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: transform 0.3s ease;
}

.theme-icon:hover {
  transform: rotate(20deg);
}

.theme-icon.dark {
  color: #fdd835;
  /* жёлтый */
}

.theme-icon.light {
  color: #90caf9;
  /* голубой */
}

.icon {
  width: 24px;
  height: 24px;
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
