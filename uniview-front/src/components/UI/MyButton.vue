<template>
    <button class="base-button">
        <slot name="icon"></slot>
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: 'base-btn'
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.base-button {
    background-color: #8DA04E;
    /* Зеленый цвет из макета */
    color: white;
    font-family: "Montserrat Alternates", sans-serif;
    font-weight: 500;
    font-style: normal;
    padding: 20px 40px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
}

.base-button:hover {
    background-color: #73843c;
}
</style>