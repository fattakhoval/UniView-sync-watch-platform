<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import NavBar from '@/components/UI/NavBar.vue';
import FloatingInput from '@/components/UI/FloatingInput.vue';

const email = ref('');
const password = ref('');
const username = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const isLoading = ref(false);

const usernameError = ref('');
const emailError = ref('');
const passwordError = ref('');
const confirmPasswordError = ref('');

watch(email, (newValue) => {
    email.value = newValue.trim().toLowerCase();
});

const registerUser = async () => {
    usernameError.value = '';
    emailError.value = '';
    passwordError.value = '';
    confirmPasswordError.value = '';
    errorMessage.value = '';
    successMessage.value = '';

    const trimmedUsername = username.value.trim();
    const trimmedEmail = email.value.trim();
    const trimmedPassword = password.value.trim();
    const trimmedConfirm = confirmPassword.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let hasError = false;

    if (!trimmedUsername || trimmedUsername.length > 30) {
        usernameError.value = 'Имя должно быть не длиннее 30 символов.';
        hasError = true;
    }

    if (!emailRegex.test(trimmedEmail)) {
        emailError.value = 'Введите корректный email.';
        hasError = true;
    }

    if (trimmedPassword.length < 4) {
        passwordError.value = 'Пароль должен содержать минимум 4 символа.';
        hasError = true;
    }

    if (!email.value || !password.value || !confirmPassword.value) {
        errorMessage.value = 'Все поля должны быть заполнены!';
        return;
    }

    if (trimmedPassword !== trimmedConfirm) {
        confirmPasswordError.value = 'Пароли не совпадают.';
        hasError = true;
    }

    if (hasError) return;

    // if (password.value !== confirmPassword.value) {
    //     errorMessage.value = 'Пароли не совпадают!';
    //     return;
    // }

    try {
        isLoading.value = true;
        const response = await axios.post('http://127.0.0.1:8000/auth/register', {
            email: trimmedEmail,
            password: trimmedPassword,
            username: trimmedUsername

            // email: email.value,
            // password: password.value,
            // username: username.value
        });

        console.log(response.data); // Проверь, что приходит от сервера

        successMessage.value = 'Регистрация прошла успешно! Теперь вы можете войти.';
        email.value = '';
        password.value = '';
        username.value = '';
        confirmPassword.value = '';
    } catch (error) {
        console.error('Ошибка:', error); // Дополнительная отладка

        if (error.response?.data?.detail?.includes('already registered')) {
            emailError.value = 'Этот email уже зарегистрирован.';
        } else {
            errorMessage.value = error.response?.data?.detail || 'Ошибка регистрации!';
        }
        // errorMessage.value = error.response?.data?.detail || 'Ошибка регистрации!';
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

                <div v-if="errorMessage" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ errorMessage }}</span>
                </div>

                <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

                <!-- <input v-model="username" type="text" placeholder="Имя" class="input" /> -->
                <FloatingInput label="Имя" v-model="username" :error="usernameError" type="text" />
                <div v-if="usernameError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ usernameError }}</span>
                </div>

                <!-- <input v-model="email" type="email" placeholder="Email" class="input" /> -->
                <FloatingInput label="Email" v-model="email" :error="emailError" type="email" />
                <div v-if="emailError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ emailError }}</span>
                </div>

                <!-- <input v-model="password" type="password" placeholder="Пароль" class="input" /> -->
                <FloatingInput label="Пароль" v-model="password" :error="passwordError" type="password" />
                <div v-if="passwordError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ passwordError }}</span>
                </div>

                <!-- <input v-model="confirmPassword" type="password" placeholder="Повторите пароль" class="input" /> -->
                <FloatingInput label="Повторите пароль" v-model="confirmPassword" :error="confirmPasswordError"
                    type="password" />
                <div v-if="confirmPasswordError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ confirmPasswordError }}</span>
                </div>

                <button @click="registerUser" :disabled="isLoading" class="register-btn">
                    {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
                </button>

                <p>Есть аккаунт?
                    <router-link to="/login" class="p" v-if="!username">Войти</router-link>
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

.reg-form {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5%;
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
    color: var(--accent-color);
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
    /* background: #634d7a; */
    background: var(--sign-btn);
    color: var(--sign-btn-text);
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
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: rgba(255, 0, 0, 0.05);
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #510010;
    padding: 2px 6px;
    border-radius: 8px;
    margin-bottom: 2px;
    font-size: 12px;
    font-family: "Montserrat Alternates", sans-serif;

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

.field-error {
    font-size: 13px;
    color: #ad0a0a;
    margin-top: -12px;
    margin-bottom: 8px;
    padding-left: 2px;
    font-family: "Montserrat Alternates", sans-serif;
}


/* .error-message {
    color: #ff4a4a;
    margin-bottom: 10px;
} */

.success-message {
    color: #8da04e;
    margin-bottom: 10px;
}
</style>
