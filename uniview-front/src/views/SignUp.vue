<script setup>
import { ref } from 'vue';
import axios from 'axios';
import NavBar from '@/components/UI/NavBar.vue';

const email = ref('');
const password = ref('');
const username = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const isLoading = ref(false);

const registerUser = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    if (!email.value || !password.value || !confirmPassword.value) {
        errorMessage.value = 'Все поля должны быть заполнены!';
        return;
    }

    if (password.value !== confirmPassword.value) {
        errorMessage.value = 'Пароли не совпадают!';
        return;
    }

    try {
    isLoading.value = true;
    const response = await axios.post('http://127.0.0.1:8000/auth/register', {
        email: email.value,
        password: password.value,
        username: username.value
    });

    console.log(response.data); // Проверь, что приходит от сервера

    successMessage.value = 'Регистрация прошла успешно! Теперь вы можете войти.';
    email.value = '';
    password.value = '';
    username.value = '';
    confirmPassword.value = '';
} catch (error) {
    console.error('Ошибка:', error); // Дополнительная отладка
    errorMessage.value = error.response?.data?.detail || 'Ошибка регистрации!';
} finally {
    isLoading.value = false;
}

};
</script>

<template>
    <div class="container">
        <NavBar />

        <div class="reg-form">



            <div class="register-container">

                <h2>Регистрация</h2>

                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
                <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

                <input v-model="username" type="text" placeholder="Имя" class="input" />
                <input v-model="email" type="email" placeholder="Email" class="input" />
                <input v-model="password" type="password" placeholder="Пароль" class="input" />
                <input v-model="confirmPassword" type="password" placeholder="Повторите пароль" class="input" />

                <button @click="registerUser" :disabled="isLoading" class="register-btn">
                    {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
                </button>
            </div>
        </div>
    </div>

    <div class="page-container">
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

.reg-form {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5%;
}

.register-container {
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

.register-btn {
    padding: 12px;
    background: #634d7a;
    color: #d6f879;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.3s;
}

.register-btn:hover {
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
