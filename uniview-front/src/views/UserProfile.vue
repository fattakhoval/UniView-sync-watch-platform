<script setup>
import MyButton from '@/components/UI/MyButton.vue';
import NavBar from '@/components/UI/NavBar.vue';

import { ref } from 'vue';

</script>

<template>
    <div class="container">
        <NavBar />

        <div class="main">
            <div class="user_container">
                <div class="avatar">

                </div>

                <div class="info_block">
                    
                </div>
            </div>
        </div>

    


    </div>

    <div class="page-container">
    </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.container {
    position: absolute;
    z-index: 5;
    min-width: 99%;
    max-width: 100%;
    overflow: hidden;
}


</style>