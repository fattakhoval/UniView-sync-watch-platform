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

const usernameError = ref('');
const passwordError = ref('');

const userStore = useUserStore();



const loginUser = async () => {

    usernameError.value = '';
    passwordError.value = '';
    errorMessage.value = '';
    successMessage.value = '';

    const trimmedUsername = username.value.trim();
    const trimmedPassword = password.value.trim();

    let hasError = false;

    if (!trimmedUsername) {
        usernameError.value = 'Введите имя пользователя.';
        hasError = true;
    }

    if (!trimmedPassword) {
        passwordError.value = 'Введите пароль.';
        hasError = true;
    }

    if (hasError) return;

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

                <div v-if="errorMessage" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ errorMessage }}</span>
                </div>

                <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

                <input v-model="username" type="text" placeholder="Имя" class="input" />
                <div v-if="usernameError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ usernameError }}</span>
                </div>

                <input v-model="password" type="password" placeholder="Пароль" class="input" />
                <div v-if="passwordError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ passwordError }}</span>
                </div>

                <button @click="loginUser" :disabled="isLoading" class="auth-btn">
                    {{ isLoading ? 'Вход...' : 'Войти' }}
                </button>

                <p>Нет аккаунта?
                    <router-link to="/register" class="p" v-if="!username">Зарегитрируйтесь</router-link>
                </p>
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
    color: var(--accent-color);
    margin-bottom: 20px;
}

p {
    font-family: "Montserrat Alternates", sans-serif;
    color: #1c2011;
    font-size: 14px;
    text-align: center;
}

.p {
    font-family: "Montserrat Alternates", sans-serif;
    color: var(--accent-color);
    font-size: 14px;
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
    /* background: #634d7a; */
    background: var(--sign-btn);
    color: var(--sign-btn-text);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.3s;
}

.auth-btn:hover {
    background: #4b3960;
}

/* .error-message {
    color: #ff4a4a;
    margin-bottom: 10px;
} */

.error-message {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: rgba(255, 0, 0, 0.05);
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #b00020;
    padding: 2px 6px;
    border-radius: 8px;
    margin-bottom: 2px;
    font-size: 12px;
}

.icon {
    fill: #b00020;
    flex-shrink: 0;
}

.animated-error {
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-2px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


.success-message {
    color: #8da04e;
    margin-bottom: 10px;
}
</style>
