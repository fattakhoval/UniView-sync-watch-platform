<template>
    <div class="floating-label">
      <input
        :type="type"
        :id="id"
        v-model="inputValue"
        :required="required"
        class="input"
        @focus="isFocused = true"
        @blur="onBlur"
      />
      <label :for="id" :class="{ active: isFocused || inputValue }">{{ label }}</label>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    modelValue: String,
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    id: {
      type: String,
      required: true
    },
    required: {
      type: Boolean,
      default: false
    }
  });
  
  const emit = defineEmits(['update:modelValue']);
  
  const inputValue = ref(props.modelValue || '');
  const isFocused = ref(false);
  
  watch(() => props.modelValue, val => inputValue.value = val);
  watch(inputValue, val => emit('update:modelValue', val));
  
  function onBlur() {
    if (!inputValue.value) isFocused.value = false;
  }
  </script>
  
  <style scoped>
  .floating-label {
    position: relative;
    margin-top: 10px;
    width: 100%;
    font-family: "Montserrat Alternates", sans-serif;

  }
  
  .input {
    width: 94%;
    padding: 12px;
    font-size: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    color: #fff;
    outline: none;
  }
  
  .floating-label label {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    transition: 0.2s ease all;
    color: rgba(255, 255, 255, 0.6);
    pointer-events: none;
    background: transparent;
    padding: 0 4px;
  }
  
  .floating-label label.active {
    top: -12px;
    left: 5px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }
  </style>
  