<template>
  <i class="mdi mdi-volume-high" :class="iconClass" @click="toggle"></i>
</template>

<script>
export default {
  props: {
    value: { type: Boolean }
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {
    iconClass() {
      return this.value ? "mdi-volume-high" : "mdi-volume-off";
    },
    flag: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    }
  },
  methods: {
    toggle() {
      this.flag = !this.flag;
    }
  }
};
</script>

<style scoped>
</style>
