<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBar from '@/components/navbars/NavBar.vue';
</script>

<template>
  <div>
    <div class="nav">
      <NavBar class="container"/>
    </div>
    
    <RouterView class="container" />
  </div>

</template>

<style scoped>
.nav {
  background-color: #3f2411;
}
</style>