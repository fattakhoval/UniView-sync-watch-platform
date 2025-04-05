<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';
import NavBar from '@/components/UI/NavBar.vue';
import router from '@/router';
import parseJwt from '@/utils';
import Cookies from 'js-cookie';  // Можно использовать js-cookie для работы с куками


const username = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);

const userStore = useUserStore();



const loginUser = async () => {
    try {
        isLoading.value = true;
        await userStore.login(username.value, password.value);
        const token = Cookies.get('access_token');
        const decoded = parseJwt(token);
        console.log(decoded);
        router.push('/');

    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        isLoading.value = false;
    }
};
</script>


<template>
    <div class="container">
        <NavBar />

        <div class="auth-form">
            <div class="auth-container">
                <h2>Вход</h2>

                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
                <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

                <input v-model="username" type="text" placeholder="Имя" class="input" />
                <input v-model="password" type="password" placeholder="Пароль" class="input" />

                <button @click="loginUser" :disabled="isLoading" class="auth-btn">
                    {{ isLoading ? 'Вход...' : 'Войти' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    position: absolute;
    z-index: 5;
    min-width: 99%;
    max-width: 100%;
    overflow: hidden;
}

.auth-form {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5%;
}

.auth-container {
    width: 100%;
    max-width: 400px;
    background: rgba(108, 103, 128, 0.2);
    padding: 30px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
}

h2 {
    font-family: "Montserrat Alternates", sans-serif;
    color: #d6f879;
    margin-bottom: 20px;
}

.input {
    padding: 12px;
    font-size: 14px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    color: #fff;
    outline: none;
}

.input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.auth-btn {
    padding: 12px;
    background: #634d7a;
    color: #d6f879;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.3s;
}

.auth-btn:hover {
    background: #4b3960;
}

.error-message {
    color: #ff4a4a;
    margin-bottom: 10px;
}

.success-message {
    color: #8da04e;
    margin-bottom: 10px;
}
</style>
