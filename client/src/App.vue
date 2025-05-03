<template>
  <div id="app">
    <!-- Persistent top-left Bill branding -->
    <div class="bill-header">
      <img src="/favicon.ico" alt="Bill" class="bill-logo" />
      <span class="bill-name">Bill</span>
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
.bill-header {
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

.bill-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}

.bill-name {
  font-weight: bold;
  font-size: 16px;
  color: #c4c4c4;
}
</style>
