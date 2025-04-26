<script setup>
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';



</script>

<template>
    <div class="container">
        <NavBar />
        <div class="friend-main">

            <div class="friends-page">
                <div class="send-request">
                    <input v-model="searchQuery" placeholder="Найти пользователя..." />
                    <MyButton class="send-fr">
                        Добавить в друзья
                    </MyButton>
                    <!-- <button @click="sendFriendRequest">Добавить в друзья</button> -->

                </div>

                <div class="fr-block">
                    <div class="my-fr">
                        <h2 class="h2">Друзья</h2>
                        <div class="ul">

                            <div class="frnd">
                                liza
                                <button @click="removeFriend(friend.id)" class="btn-remove">Удалить</button>
                            </div>
                            <div v-for="friend in friends" :key="friend.id" class="frnd">
                                {{ friend.name }}
                                <button @click="removeFriend(friend.id)" class="btn-remove">Удалить</button>
                            </div>

                        </div>

                    </div>

                    <div class="fr-apps">
                        <h2 class="h2">Заявки в друзья</h2>
                        <div class="ul">
                            <div class="frnd">
                                lira
                                <div class="btn-grp">
                                    <button @click="acceptRequest(request.id)" class="btn-accept">Принять</button>
                                    <button @click="declineRequest(request.id)" class="btn-remove">Отклонить</button>
                                </div>
                            </div>
                            <div class="frnd" v-for="request in requests" :key="request.id">
                                {{ request.from_name }}
                                <button @click="acceptRequest(request.id)">Принять</button>
                                <button @click="declineRequest(request.id)">Отклонить</button>
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
</style>