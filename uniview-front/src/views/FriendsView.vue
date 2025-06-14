<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';
import parseJwt from '@/utils';
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';

const friends = ref([]);
const requests = ref([]);
const searchQuery = ref('');

const token = Cookies.get('access_token');
let userId = null;

if (token) {
  const decoded = parseJwt(token);
  if (decoded) {
    userId = decoded.id_user;
  }
}

// Получение списка друзей
const fetchFriends = async () => {
  if (!userId) return;

  try {
    const response = await axios.get(`http://localhost:8000/friend/friends/${userId}`);
    friends.value = response.data;
    console.log(friends.value);
  } catch (error) {
    console.error('Ошибка при получении друзей:', error);
  }
};

const sendFriendRequest = async () => {
  if (!searchQuery.value) return;

  try {
    const response = await axios.post('http://localhost:8000/friend/request', {
      name_or_email: searchQuery.value,
      current_user: userId,
    });

    if (response.status === 201) {
      alert('Заявка отправлена!');
      searchQuery.value = '';
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Ошибка при отправке заявки');
  }
};

const fetchRequests = async () => {
  if (!userId) return;

  try {
    const response = await axios.get(`http://localhost:8000/friend/pending/${userId}`);
    requests.value = response.data;
  } catch (error) {
    console.error('Ошибка при получении заявок:', error);
  }
};

const acceptRequest = async (id_requester) => {
  try {
    await axios.post('http://localhost:8000/friend/accept', {
      id_requester,
      current_user: userId,
    });
    await fetchRequests(); // обновить список после принятия
    await fetchFriends(); // обновить список друзей
  } catch (error) {
    console.error('Ошибка при принятии заявки:', error);
  }
};

const declineRequest = async (id_requester) => {
  try {
    await axios.post('http://localhost:8000/friend/remove', {
      target_user_id: id_requester,
      current_user: userId,
    });
    await fetchRequests(); // обновить список после отклонения
  } catch (error) {
    console.error('Ошибка при отклонении заявки:', error);
  }
};

const removeFriend = async (targetUserId) => {
  try {
    await axios.post('http://localhost:8000/friend/remove', {
      target_user_id: targetUserId,
      current_user: userId,
    });
    await fetchFriends(); // обновим список друзей
  } catch (error) {
    console.error('Ошибка при удалении друга:', error);
  }
};


onMounted(async () => {
  await fetchFriends();
  await fetchRequests();  // ← добавь это
});




</script>

<template>
    <div class="container">
        <NavBar />
        <div class="friend-main">

            <div class="friends-page">
                <div class="send-request">
                    <input v-model="searchQuery" placeholder="Найти пользователя..." />
                    <MyButton class="send-fr" @click="sendFriendRequest">
                        Добавить в друзья
                    </MyButton>
                    <!-- <button @click="sendFriendRequest">Добавить в друзья</button> -->

                </div>

                <div class="fr-block">
                    <div class="my-fr">
                        <h2 class="h2">Друзья</h2>
                        <div class="ul">

                            <div v-if="friends.length === 0" class="frnd">Нет друзей</div>

                            <div v-for="friend in friends" :key="friend.id" class="frnd">
                                {{ friend.username }}
                                <button @click="removeFriend(friend.id)" class="btn-remove">Удалить</button>
                            </div>
                           

                        </div>

                    </div>

                    <div class="fr-apps">
                        <h2 class="h2">Заявки в друзья</h2>
                        <div class="ul">
                           
                            <div class="frnd" v-for="request in requests" :key="request.id">
                                {{ request.username }}

                                <div class="btn-grp">
                                    <button @click="acceptRequest(request.id)" class="btn-accept">Принять</button>
                                    <button @click="declineRequest(request.id)" class="btn-remove">Отклонить</button>

                                </div>
                            </div>
                        </div>
                    </div>



                </div>


            </div>

        </div>
    </div>

    <div class="page-container">
    </div>
</template>

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

.friend-main {
    display: flex;
    justify-content: center;
    align-items: center;


}

.friends-page {

    /* gap: 20px; */
    width: 90%;

}

.send-request {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}

.send-request input {
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 300;
    color: #A6A6A6;
    background-color: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease-in-out;
    width: 50%;
}

.send-request input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.send-request input:focus {
    border-color: #634D7A;
    background-color: var(--input-focus);

}

.send-fr {

    border-radius: 10px;
    padding: 5px 10px;
    height: 40px;
}

.fr-block {
    display: flex;
    justify-content: space-between;
}

.my-fr {
    background: rgba(108, 103, 128, 0.2);
    border-radius: 20px;
    border: 1px solid var(--input-border);
    padding: 20px 60px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 40%;

}

.fr-apps {
    background: rgba(108, 103, 128, 0.2);
    border-radius: 20px;
    border: 1px solid var(--input-border);
    padding: 20px 60px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 40%;
}

.fr-block .h2 {
    color: var(--accent-color);
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;

}

.fr-block .ul {

    display: flex;
    flex-direction: column;
    align-items: start;


}

.frnd {
    width: 90%;
    border: 1px solid #A6A6A6;
    border-radius: 15px;
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

.btn-remove {
    background-color: var(--btn-in);
    color: var(--btn-in-text);
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    padding: 10px 20px;
    border-radius: 10px;
    border: 1px solid rgba(213, 210, 210, 0.3);
    cursor: pointer;
    transition: background 0.3s ease;
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
}

.btn-remove:hover {
    background-color: var(--btn-in-hover);

}

.btn-grp {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
}

.btn-accept {
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

.btn-accept:hover {
    background-color: var(--base-button-color-hover);
}

.my-fr,
.fr-apps {
  max-height: 400px;
  overflow-y: auto;
}

@media screen and (max-width: 768px) {
  .fr-block {
    flex-direction: column;
    gap: 20px;
  }

  .my-fr,
  .fr-apps {
    width: 90%;
    max-height: 300px;
    overflow-y: auto;
    padding: 20px;
  }

  /* .send-request {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .send-request input {
    width: 100%;
  }

  .send-fr {
    width: 100%;
  } */
}

</style>