<template>
    <div class="block">
        <slot name="block-icon"></slot>
        <div class="content-slot">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'info-block'
}
</script>

<style>
.block {
    background: rgba(108, 103, 128, 0.2);
    border-radius: 20px;
    border: 1px solid #505050;
    width: 250px;
    height: 130px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    color: #fff;
    font-family: "Raleway", sans-serif;
    font-size: 16px;
    font-weight: 400;

}

.content-slot {
    width: 120px;
}
</style>