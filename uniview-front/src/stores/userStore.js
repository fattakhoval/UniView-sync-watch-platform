import { defineStore } from 'pinia';  // Импортируем defineStore из Pinia
import axios from 'axios';
import Cookies from 'js-cookie';  // Можно использовать js-cookie для работы с куками
import router from '@/router';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
  }),

  actions: {
    async fetchUser() {
      try {
        const response = await axios.get('/api/auth/me', {
          withCredentials: true,  // Передаём куки для авторизации
        });
        this.user = response.data;
      } catch {
        this.user = null;
      }
    },

    async login(username, password) {
      try {
        const response = await axios.post('/api/auth/login', {
          username,
          password,
        });

        // Сохраняем токен в куки
        Cookies.set('access_token', response.data.access_token, { expires: 1 });
        // await this.fetchUser();
      } catch (error) {
        throw new Error(error.response?.data?.detail || 'Ошибка входа');
      }
    },

    logout() {
      // Очистка куки с токеном
      Cookies.remove('access_token');

      // Очистка состояния пользователя в Pinia
      this.user = null;

      // Перенаправление на страницу входа
      router.push('/login');  // Можно перенаправить на страницу входа
    },
  },
});
