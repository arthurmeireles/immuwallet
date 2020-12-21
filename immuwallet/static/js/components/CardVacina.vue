<template>
  <div class="col-xs-12 col-sm-6 col-md-4 col-lg-4">
    <div class="widget widget-stats head-box" :style="style">
      <div class="stats-icon">
        <i class="fa fa-eyedropper"></i>
      </div>
      <div class="stats-info">
        <h5>{{ top }}</h5>
        <h4 class="stat-count">{{ mid }}</h4>
        <h6><i class="fa fa-home"></i> {{ submid }}</h6>
      </div>
      <div class="stats-link footer-link">
        <a> </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pk: { type: Number, required: true },
    top: { type: String, required: true },
    mid: { type: String, required: true },
    submid: { type: String, required: true },
    color: { type: String, required: true, default: "blue" },
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {
    style() {
      return {
        blue: "background-color: #0062A3; #727CB6;",
        lightblue: "background-color:#348FE2;  #00ACAC;",
        red: "background-color:#810020;  #BA262B;",
      }[this.color];
    },
  },
  methods: {},
};
</script>

<style scoped>
.pointer {
  cursor: pointer;
}
</style>
