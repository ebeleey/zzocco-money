<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBar from '@/components/navbars/NavBar.vue';
</script>

<template>
  <div>
    <NavBar class="container"/>
    <RouterView class="container" />
  </div>

</template>

<style scoped>

</style>
