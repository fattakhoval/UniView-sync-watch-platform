<template>
    <div class="chat">
        <p>ЧАТ</p>

        <div class="messages">

        </div>

        <div class="message-input">
            <slot></slot>
            <button>></button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'chat'
}

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');

.chat {
    background: rgba(73, 59, 97, 0.729);
    border-radius: 20px;
    border: 1px solid rgba(179, 176, 185, 0.858);
    height: 100%;


}

.chat p {
    font-family: "Raleway", sans-serif;
    font-size: 20px;
    font-weight: 400;
    color: rgb(208, 208, 208);
    margin: 0;

}

.message-input {
    display: flex;
    align-items: center;
    justify-content: space-around;
}

button {
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 300;
    color: #A6A6A6;
    background-color: rgba(174, 174, 174, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease-in-out;
}

button:focus {
    border-color: #634D7A;
    background-color: rgba(255, 255, 255, 0.15);
}
</style>