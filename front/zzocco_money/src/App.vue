<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBar from '@/components/navbars/NavBar.vue';
</script>

<template>
  <div class="app-wrapper">
    <div class="nav">
      <NavBar class="container"/>
    </div>
    <div class="content">
      <RouterView class="container" />
    </div>
    <footer>
      <br>
      Copyrights ⓒ 2024 zcmn All Rights reserved.
    </footer>
  </div>
</template>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
}

.nav {
  background-color: #3f2411;
}

footer {
  margin-top: 40px;
  height: 100px;
  background-color: #3f2411;
  text-align: center;
  color: white;
  font-size: 12px;
  padding: 20px 0;
}
</style>