<template>
  <header>
    <div class="wrapper">
      <h1>{{ $t('home.title') }}</h1>
      <nav>
        <router-link to="/product-overview">{{ $t('home.productLink') }}</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
</script>

<style scoped>
header {
  line-height: 1.5;
  text-align: center;
  padding: 2rem;
  min-height: calc(100vh - 80px); /* Account for navbar height */
  display: flex;
  justify-content: center;
  align-items: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

nav {
  margin-top: 1rem;
}

a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

a:hover {
  background-color: #36966f;
}

.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

@media (min-width: 1024px) {
  header {
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>