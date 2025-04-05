<template>
    <transition name="fade">
      <div v-if="isOpen" class="modal-overlay" @click="closeModal">
        <transition name="scale">
          <div v-if="isOpen" class="modal-content" @click.stop>
            <button class="close-btn" @click="closeModal">&times;</button>
            <slot></slot>
          </div>
        </transition>
      </div>
    </transition>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({ isOpen: Boolean });
  const emit = defineEmits(['close']);
  
  const closeModal = () => {
    emit('close');
  };
  </script>
  
  <style scoped>
  /* Затемнение заднего фона */
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  
  /* Анимация модального окна */
  .scale-enter-active, .scale-leave-active {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
  .scale-enter-from, .scale-leave-to {
    opacity: 0;
    transform: scale(0.8);
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: rgba(73, 59, 97, 0.729);
    padding: 40px 60px;
    border-radius: 20px;
    min-width: 300px;
    max-width: 500px;
    position: relative;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: aliceblue;
  }
  </style>
  