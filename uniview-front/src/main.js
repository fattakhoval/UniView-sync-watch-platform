import './assets/main.css'

import { createApp, watch } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useThemeStore } from './stores/themeStore'

const app = createApp(App)
app.use(createPinia())
const themeStore = useThemeStore()
themeStore.setTheme(themeStore.theme)

watch(
    () => themeStore.theme,
    (newTheme) => {
      document.documentElement.className = newTheme; // 'light' или 'dark'
    },
    { immediate: true }
  );


app.use(router)

app.mount('#app')
