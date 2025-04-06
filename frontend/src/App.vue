<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import NavbarComponent from '@/components/NavbarComponent.vue';
import {useUserStore} from "@/stores/userStore.ts";
import axios from 'axios';

const userStore = useUserStore();


onMounted(() => {
  userStore.initStore()
  const token = userStore.user.access
  if (token) {
    axios.defaults.headers.common["Authorization"] = "Bearer " + token
  } else {
    axios.defaults.headers.common["Authorization"] = ""
  }
})
</script>

<template>
  <div>
    <NavbarComponent />
    <main class="container mx-auto py-4">
      <Router-view />
    </main>
  </div>
</template>

<style scoped>

</style>
