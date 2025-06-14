<script setup>
import MailIcon from '@/components/icons/MailIcon.vue';
import PeopleIcon from '@/components/icons/PeopleIcon.vue';
import PersonIcon from '@/components/icons/PersonIcon.vue';
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';
import Cookies from 'js-cookie';
import parseJwt from '@/utils';
import axios from 'axios';
import { ref, onMounted } from 'vue';

let count_friends = ref('');
let userId = null;
let userInfo = ref('');

let email = ref('');
let oldPassword = ref('');
let newPassword = ref('');


const token = Cookies.get('access_token');
if (token) {
  const decoded = parseJwt(token);
  if (decoded) {
    userId = decoded.id_user;
  }
}

onMounted(() => {
    get_count_friends();
    get_user_info();
});


async function get_count_friends(){

     try {
        const response = await axios.get(`/api/friend/friends/${userId}`);

        if (response) {
            count_friends.value = response.data.length;
        }
    } catch (error) {
        console.error(error);
        console.log(`Ошибка при get friends: ${error}`);
    }
};


async function get_user_info(){

     try {
        
        const response = await axios.get(`/api/user/info/${userId}`);

        if (response) {
            userInfo.value = response.data;
            email.value = userInfo.value.email;
        }

    } catch (error) {
        console.error(error);
        console.log(`Ошибка при получение данных о пользователе: ${error}`);
    }
};

async function update_user(){

     try {
        const response = await axios.put(`/api/user/update_profile/${userId}`, {
            email: email.value,
            old_password: oldPassword.value,
            new_password: newPassword.value,
        });

        if (response.status == 201){
            alert('Данные успешно обновлены');
        }

        email.value = response.data.email;
        oldPassword.value = '';
        newPassword.value = '';
    } catch (error) {
        console.error(error);
        let message = ''

        if (error.response?.status == 422){
            message = 'Некорректный почтовый адрес';
        } else {
            message = error.response?.data?.detail || 'Произошла ошибка при обновлении данных';
        }

        
       
        alert(message);
    }
};



</script>

<template>
    <div class="container">
        <NavBar />

        <div class="main">
            <div class="user_container">


                <div class="st-block">

                    <h1 class="h1">{{ userInfo.username }}</h1>

                    <div class="fr-count">
                        <p>
                            <PeopleIcon class="u-icon" /> Друзья
                        </p>
                        <div class="p">{{ count_friends }}</div>
                    </div>





                </div>

                <div class="u-info">


                    <div class="u-email">
                        <label for="email"><MailIcon class="u-icon"/> Почта</label>
                        <input type="email" v-model="email">

                    </div>

                    <div class="u-email">
                        <label for="password"> <PersonIcon class="u-icon" />Старый Пароль</label>
                        <input type="password" value="" v-model="oldPassword">

                    </div>

                    <div class="u-email">
                        <label for="password"> <PersonIcon class="u-icon" />Новый Пароль</label>
                        <input type="password" value="" v-model="newPassword">

                    </div>

                    <button @click="update_user()">Изменить</button>


                </div>
            </div>
        </div>




    </div>

    <div class="page-container">
    </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');

.container {
    position: absolute;
    z-index: 5;
    min-width: 99%;
    max-width: 100%;
    overflow: hidden;
}

.main {
    display: flex;
    justify-content: center;
    align-items: center;
}

.user_container {
    width: 90%;
    background: rgba(108, 103, 128, 0.2);
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: baseline;
    gap: 20%;

}

.st-block {
    padding: 40px;
}

.st-block .h1 {
    font-family: "Raleway", sans-serif;
    font-size: 40px;
    font-weight: 600;
    color: var(--accent-color);
    margin-bottom: 20px;
}

.fr-count p {
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    font-size: 24px;
    color: var(--text-p);
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0;
}

.u-icon {
    width: 30px;
    fill: var(--text-p);
}

.fr-count .p {
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    font-size: 24px;
    color: var(--text-p);

    padding: 5px 15px;
    background: var(--input-bg);
    border: none;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100px;

}

.u-info {

    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 40px;
    width: 30%;
}

.u-info input {
    border: 1px solid #A6A6A6;
    border-radius: 10px;
    background: var(--input-bg);
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--text-p);
    font-family: "Raleway", sans-serif;
    font-size: 18px;
    font-weight: 600;
}

.u-email {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.u-email label {
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    font-size: 18px;
    color: var(--text-p);
    display: flex;
    align-items: center;
    gap: 10px;
}

.u-info button {
    background-color: var(--base-button-color);
    /* Зеленый цвет из макета */
    color: white;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    padding: 10px 20px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.u-info button:hover {
    background-color: var(--base-button-color-hover);
}

@media (max-width: 1024px) {
    .user_container {
        flex-direction: column;
        align-items: center;
        gap: 40px;
        padding: 20px;
        width: 80%;
    }

    .st-block {
        padding: 20px;
        text-align: center;
    }

    .st-block .h1 {
        font-size: 32px;
    }

    .fr-count p,
    .fr-count .p {
        font-size: 20px;
    }

    .fr-count .p {
        width: auto;
        padding: 5px 10px;
    }

    .u-info {
        width: 100%;
        padding: 0 20px 20px 20px;
    }

    .u-info input {
        font-size: 16px;
        padding: 10px 15px;
    }

    .u-email label {
        font-size: 16px;
    }

    .u-info button {
        width: 100%;
        font-size: 16px;
    }
}

@media (max-width: 600px) {
    .st-block .h1 {
        font-size: 24px;
    }

    .fr-count p,
    .fr-count .p {
        font-size: 18px;
    }

    .u-icon {
        width: 24px;
    }

    .u-info input {
        font-size: 14px;
    }

    .u-info button {
        font-size: 14px;
        padding: 10px;
    }
}

</style>