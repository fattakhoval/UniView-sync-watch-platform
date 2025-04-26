<template>
    <div class="container">
        <NavBar />

        <div class="schedule-container">
            <div class="top-section">
                <div class="form-section">
                    <h2>Запланировать просмотр</h2>

                    <input type="text" v-model="title" placeholder="Watch party title" />
                    <input type="time" v-model="time" />

                    <h3>Пригласить друзей</h3>
                    <div v-for="friend in friends" :key="friend.id" class="friend-row">
                        <span>{{ friend.name }}</span>
                        <button @click="invite(friend)" class="invite-btn"><PeopleIcon class="p-icon"/> Пригласить</button>
                    </div>

                    <button class="submit-btn" @click="scheduleParty">
                        Запланировать просмотр
                    </button>
                </div>

                <div class="calendar-wrapper">
                    <Datepicker v-model="selectedDate" :enable-time-picker="false" auto-apply inline
                        :teleport="false" />
                </div>
            </div>

            <div class="upcoming-section">
                <h2>Upcoming Watch Parties</h2>
                <div v-if="!scheduled.length">No watch parties scheduled</div>
                <ul>
                    <li v-for="party in scheduled" :key="party.id">
                        {{ party.title }} — {{ party.date }} at {{ party.time }}
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
import { ref } from 'vue';
import 'vue-cal/dist/vuecal.css'
import VueCal from 'vue-cal'
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import PeopleIcon from '@/components/icons/PeopleIcon.vue';

const selectedDate = ref(null)

const title = ref('');
const date = ref('');
const time = ref('');
const friends = ref([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
    { id: 3, name: 'Charlie' }
]);
const scheduled = ref([]);

const invite = (friend) => {
    alert(`Invited ${friend.name}`);
};

const scheduleParty = () => {
    if (title.value && date.value && time.value) {
        scheduled.value.push({
            id: Date.now(),
            title: title.value,
            date: date.value,
            time: time.value
        });
        title.value = '';
        date.value = '';
        time.value = '';
    } else {
        alert('Заполните все поля');
    }
};
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

:deep(.dp__theme_light) {
    color: #e5e7eb; /* светлый текст */
    border-radius: 12px;
    padding: 1rem;
    --dp-background-color: var(--input-bg);
}

:deep(.dp__calendar_header) {
    color: #91959c; /* сероватый текст заголовка */
    font-weight: 600;
}

:deep(.dp__calendar_header_item) {
    color: #dee5f0; /* дни недели сероватые */
}

:deep(.dp__cell_inner) {
    color: #d1d5db;
    border-radius: 8px;
    transition: background-color 0.2s;
}

:deep(.dp__cell_inner:hover) {
    background-color: rgba(255, 255, 255, 0.1); /* лёгкий подсвет при наведении */
}

:deep(.dp__cell_inner.dp__active_date) {
    background-color: #6366f1; /* фиолетовый выделенный день */
    color: white;
}

:deep(.dp__calendar_item.dp__outside) {
    opacity: 0.3; /* затемнение дат не из текущего месяца */
}

:deep(.dp__today .dp__cell_inner) {
    border: 1px solid #6366f1; /* подсветка сегодняшней даты */
}

/* Стрелочки навигации */
:deep(.dp__inner_nav svg) {
    color: #ffffff;
    transition: color 0.2s;
}

:deep(.dp__inner_nav svg:hover) {
    color: #ffffff;
}



</style>