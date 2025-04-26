<template>
    <div class="hr">
        <hr>
        <slot></slot>
        <hr>
    </div>
</template>

<script>
export default {
    name: 'hr-block'
}

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.hr {
    font-family: "Montserrat Alternates", sans-serif;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: #C0C0C0;
    
}

hr {
    width: 50%;
    /* Длина 50% от родительского контейнера */
    border: none;
    height: 2px;
    background-color: var(--hr);
    /* Цвет линии */
}
</style>