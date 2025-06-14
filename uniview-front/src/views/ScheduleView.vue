<template>
    <div class="container">
        <NavBar />

        <div class="schedule-container">
            <div class="top-section">
                <div class="form-section">
                    <h2>Запланировать просмотр</h2>

                    <input type="text" v-model="title" placeholder="Название комнаты" />
                    <input type="time" v-model="time" />

                    <h3>Пригласить друзей</h3>
                    <div v-for="friend in friends" :key="friend.id" class="friend-row">
                        <span>{{ friend.username }}</span>
                        <!-- <button @click="invite(friend)" class="invite-btn"><PeopleIcon class="p-icon"/> Пригласить</button> -->

                        <button @click="toggleInvite(friend.id)" class="invite-btn">
                            <PeopleIcon class="p-icon" />
                            {{ isInvited(friend.id) ? 'Убрать' : 'Пригласить' }}
                        </button>
                    </div>

                    <button class="submit-btn" @click="scheduleParty">
                        Запланировать просмотр
                    </button>
                </div>

                <div class="calendar-wrapper">
                    <Datepicker v-model="selectedDate" :enable-time-picker="false" auto-apply inline :teleport="false"
                        :highlight="highlightedDates" />
                </div>
            </div>

            <div class="upcoming-section">
                <h2>Запланированные Встречи</h2>
                <div v-if="!scheduled.length">No watch parties scheduled</div>
                <ul>
                    <li v-for="party in scheduled" :key="party.id">
                        {{ party.title }} — {{ party.formatted }}
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="page-container">
    </div>
</template>

<script setup>
import NavBar from '@/components/UI/NavBar.vue';
import { ref, onMounted } from 'vue';
import 'vue-cal/dist/vuecal.css'
import VueCal from 'vue-cal'
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import PeopleIcon from '@/components/icons/PeopleIcon.vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import parseJwt from '@/utils';

const selectedDate = ref(null);

const token = Cookies.get('access_token');
let userId = null;

if (token) {
    const decoded = parseJwt(token);
    if (decoded) {
        userId = decoded.id_user;
    }
}

const title = ref('');
const date = ref('');
const time = ref('');
const friends = ref([]);

const invitedIds = ref([]); // выбранные друзья
const scheduled = ref([]);
const highlightedDates = ref([]);

const toggleInvite = (friendId) => {
    if (invitedIds.value.includes(friendId)) {
        invitedIds.value = invitedIds.value.filter(id => id !== friendId);
    } else {
        invitedIds.value.push(friendId);
    }
};

const isInvited = (friendId) => invitedIds.value.includes(friendId);

const invite = (friend) => {
    alert(`Invited ${friend.name}`);
};

const scheduleParty = async () => {
    if (!title.value || !selectedDate.value || !time.value) {
        alert('Заполните все поля');
        return;
    }

    // const eventDateTime = new Date(selectedDate.value);
    const [hours, minutes] = time.value.split(':').map(Number);
    const eventDateTime = new Date(selectedDate.value);
    eventDateTime.setHours(hours);
    eventDateTime.setMinutes(minutes);
    eventDateTime.setSeconds(0);
    eventDateTime.setMilliseconds(0);

    const now = new Date();

    if (eventDateTime < now) {
        alert("Нельзя создать событие на прошедшую дату");
        return;
    }
    try {
        console.log(selectedDate.value);

        const response = await axios.post('/api/event/create', {
            title: title.value,
            date: selectedDate.value.toISOString().split('T')[0],
            time: time.value,
            id_creator: userId,
            invited_list: invitedIds.value
        });


        if (response.data.Status) {
            alert('Просмотр успешно запланирован!');
            title.value = '';
            time.value = '';
            selectedDate.value = null;
            invitedIds.value = [];
            await loadEvents();
        }
    } catch (error) {
        console.error(error);
        alert('Ошибка при создании события');
    }
};

const loadFriends = async () => {
    if (!userId) return;

    try {
        const response = await axios.get(`/api/friend/friends/${userId}`);
        friends.value = response.data;
        console.log(friends.value);
    } catch (error) {
        console.error('Ошибка при получении друзей:', error);
    }
};

const loadEvents = async () => {
    try {
        const response = await axios.get(`/api/event/user_event/${userId}`);
        scheduled.value = response.data.map(event => {
            const dateObj = new Date(event.datetime_start);

            const options = {
                day: '2-digit',
                month: 'long',
                hour: '2-digit',
                minute: '2-digit'
            };

            const formatted = new Intl.DateTimeFormat('ru-RU', options).format(dateObj);

            return {
                ...event,
                formatted, // добавим отформатированную строку
                dateOnly: dateObj.toISOString().split('T')[0]
            };
        });

        highlightedDates.value = [...new Set(scheduled.value.map(e => e.dateOnly))];
    } catch (error) {
        console.error('Ошибка загрузки событий:', error);
    }
};


onMounted(() => {
    if (!userId) {
        alert('Ошибка: пользователь не найден в cookies.');
        return;
    }
    loadFriends();
    loadEvents();
});

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.container {
    position: absolute;
    z-index: 5;
    min-width: 99%;
    max-width: 100%;
    overflow: hidden;
}

.p-icon {
    width: 20px;
    height: 20px;
    fill: #fff;
}

.schedule-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
    width: 90%;
    margin: auto;
}

.top-section {
    display: flex;
    gap: 2rem;
    background: rgba(108, 103, 128, 0.2);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}

.form-section {
    flex: 1;
    background: rgba(108, 103, 128, 0.2);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #A6A6A6;
    display: flex;
    flex-direction: column;
    color: var(--p2);
    font-family: "Raleway", sans-serif;
    font-size: 16px;
    font-weight: 600;
}

.form-section input,
input::placeholder {

    color: #e5e7eb;
}

.form-section h2 {
    color: var(--accent-color);
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;

}

.calendar-wrapper {
    flex: 1;
    background: rgba(108, 103, 128, 0.2);
    padding: 1.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.dp__flex_display {
    display: block;
}

.dp__main {
    width: 80%;
}

/* Календарь */
.dp__cell_inner.dp__active_date {
    background-color: #111827;
    background: var(--input-bg);
    border-radius: 8px;
}

.dp__month_year_select,
.dp__calendar_header {
    font-weight: bold;
    font-size: 1.2em;
}

.dp__inner_nav {
    background: none;
    border: none;
}

.dp__inner_nav svg {
    width: 20px;
    height: 20px;
    color: #4b5563;
}

.dp__calendar_header_item {
    color: #6b7280;
}

.dp__calendar_item.dp__outside {
    background: var(--input-bg);
}

.dp__cell_inner:hover {
    background-color: var(--input-bg);
}

.selected-date {
    margin-top: 10px;
    text-align: center;
    font-weight: bold;
}

/* Инпуты */
input[type="text"],
input[type="time"],
input[type="date"] {
    display: block;
    /* width: 100%; */
    margin-bottom: 1rem;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: var(--input-bg);

}

/* Друзья */
.friend-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--input-bg);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
    border: 1px solid var(--input-border);
}

.invite-btn {
    background: var(--base-button-color);
    border: 1px solid #aaa;
    padding: 0.3rem 0.7rem;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    color: #fff;
}

/* Кнопка отправки */
.submit-btn {
    background: var(--base-button-color);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
    width: 100%;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-size: 16px;
}

/* Upcoming */
.upcoming-section {
    margin-top: 2rem;
    background: rgba(108, 103, 128, 0.2);
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);

}

.upcoming-section ul {
    list-style-type: none;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-size: 18px;
    color: var(--p2);

}

.upcoming-section li {
    width: 100%;
    height: 60px;

    max-height: 300px; /* ограничение по высоте */
    overflow-y: auto;  /* вертикальная прокрутка */
    scrollbar-width: thin; /* Firefox */

}

.upcoming-section h2 {
    font-family: "Raleway", sans-serif;
    font-weight: 600;
    color: var(--accent-color);
}

:deep(.dp__theme_light) {
    color: #e5e7eb;
    /* светлый текст */
    border-radius: 12px;
    padding: 1rem;
    --dp-background-color: var(--input-bg);
}

:deep(.dp__calendar_header) {
    color: #91959c;
    /* сероватый текст заголовка */
    font-weight: 600;
}

:deep(.dp__calendar_header_item) {
    color: #dee5f0;
    /* дни недели сероватые */
}

:deep(.dp__cell_inner) {
    color: #d1d5db;
    border-radius: 8px;
    transition: background-color 0.2s;
}

:deep(.dp__cell_inner:hover) {
    background-color: rgba(255, 255, 255, 0.1);
    /* лёгкий подсвет при наведении */
}

:deep(.dp__cell_inner.dp__active_date) {
    background-color: #6366f1;
    /* фиолетовый выделенный день */
    color: white;
}

:deep(.dp__calendar_item.dp__outside) {
    opacity: 0.3;
    /* затемнение дат не из текущего месяца */
}

:deep(.dp__today .dp__cell_inner) {
    border: 1px solid #6366f1;
    /* подсветка сегодняшней даты */
}

/* Стрелочки навигации */
:deep(.dp__inner_nav svg) {
    color: #ffffff;
    transition: color 0.2s;
}

:deep(.dp__inner_nav svg:hover) {
    color: #ffffff;
}

@media (max-width: 1024px) {
    .top-section {
        flex-direction: column;
        gap: 1.5rem;
        padding: 1.5rem;
    }

    .form-section,
    .calendar-wrapper {
        width: 90%;
    }

    .dp__main {
        width: 100%;
    }

    .friend-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .invite-btn {
        width: 100%;
        justify-content: center;
    }

    input[type="text"],
    input[type="time"],
    input[type="date"] {
        width: 90%;
    }
}

@media (max-width: 640px) {
    .schedule-container {
        padding: 1rem;
        width: 90%;
    }

    .top-section {
        padding: 1rem;
    }

    .form-section {
        padding: 1rem;
    }

    .calendar-wrapper {
        padding: 1rem;
    }

    .submit-btn {
        font-size: 14px;
        padding: 0.6rem 1rem;
    }

    .upcoming-section {
        padding: 1rem;
    }

    .upcoming-section li {
        font-size: 14px;
        height: auto;
    }
}

</style>