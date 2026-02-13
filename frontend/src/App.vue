<script setup>
import NavigatorBar from './components/NavigatorBar.vue'
</script>

<template>
  <NavigatorBar />
  <main>
    <RouterView />
  </main>
</template>

<style>
/* Global styles can go here */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
}
</style>