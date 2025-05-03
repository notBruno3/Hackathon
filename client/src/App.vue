<template>
  <div id="app">
    <transition name="fade-page" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uid: crypto.randomUUID()
    };
  },
  provide() {
    return {
      globalUid: this.uid
    };
  },
  name: 'App'
};
</script>