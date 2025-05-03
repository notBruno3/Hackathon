<template>
  <div id="app">
    <!-- Persistent top-left Peter branding -->
    <div class="peter-header">
      <img src="/favicon.ico" alt="Peter" class="peter-logo" />
      <span class="peter-name">Peter</span>
    </div>

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

<style>
.peter-header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  background-color: rgb(48, 48, 48);
  padding: 8px 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom-right-radius: 12px;
}

.peter-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}

.peter-name {
  font-weight: bold;
  font-size: 16px;
  color: #c4c4c4;
}
</style>
