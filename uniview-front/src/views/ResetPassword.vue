<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import FloatingInput from '@/components/UI/FloatingInput.vue';
import NavBar from '@/components/UI/NavBar.vue';

const route = useRoute();
const router = useRouter();

const token = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const passwordError = ref('');
const confirmError = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);

onMounted(() => {
    token.value = route.query.token || '';
    if (!token.value) {
        errorMessage.value = 'Недействительная или отсутствующая ссылка восстановления.';
    }
});

const resetPassword = async () => {
    passwordError.value = '';
    confirmError.value = '';
    errorMessage.value = '';
    successMessage.value = '';

    if (newPassword.value.length < 6) {
        passwordError.value = 'Пароль должен быть не менее 6 символов.';
        return;
    }

    if (newPassword.value !== confirmPassword.value) {
        confirmError.value = 'Пароли не совпадают.';
        return;
    }

    try {
        isLoading.value = true;

        const response = await fetch('/api/user/reset_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                token: token.value,
                new_password: newPassword.value
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при сбросе пароля');
        }

        successMessage.value = 'Пароль успешно обновлён. Сейчас вы будете перенаправлены...';
        setTimeout(() => router.push('/login'), 3000);
    } catch (error) {
        errorMessage.value = error.message || 'Произошла ошибка';
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
                <h2>Новый пароль</h2>

                <div v-if="errorMessage" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ errorMessage }}</span>
                </div>

                <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

                <FloatingInput v-model="newPassword" type="password" id="new-password" label="Новый пароль" required />
                <div v-if="passwordError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ passwordError }}</span>
                </div>

                <FloatingInput v-model="confirmPassword" type="password" id="confirm-password"
                    label="Подтвердите пароль" required />
                <div v-if="confirmError" class="error-message animated-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" width="18" height="18">
                        <path fill="currentColor"
                            d="M12 2a10 10 0 1 0 10 10A10.01 10.01 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>{{ confirmError }}</span>
                </div>

                <button @click="resetPassword" :disabled="isLoading" class="auth-btn">
                    {{ isLoading ? '...' : 'Сбросить пароль' }}
                </button>
            </div>
        </div>
    </div>
    <div class="page-container"></div>

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
    color: #5b0011;
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


.success-message {
    color: #8da04e;
    margin-bottom: 10px;
}
</style>
