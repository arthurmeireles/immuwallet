<template>
  <div class="col-xs-12 col-sm-6 col-md-4 col-lg-4">
    <div
      class="widget widget-stats head-box"
      :style="style"
    >
      <div class="stats-icon">
        <i class="fa fa-eyedropper"></i>
      </div>
      <div class="stats-info">
        <h4>{{ top }}</h4>
        <p class="stat-count">{{ mid }}</p>
        <h6>{{ submid }}</h6>
      </div>
      <div class="stats-link footer-link">
        <a>
          <i class="fa fa-clock-o"></i>
          {{ bottom1 }}
          <i class="fa fa-h-square"></i>
          {{ bottom2 }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    top: { type: String, required: true },
    mid: { type: String, required: true },
    submid: { type: String, required: true },
    bottom1: { type: String, required: true },
    bottom2: { type: String, required: true },
    color: { type: String, required: true, default: 'blue'},
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {
    style() {
      return {
        'blue': 'background-color: #0062A3; #727CB6;',
        'lightblue': 'background-color:#348FE2;  #00ACAC;',
        'red': 'background-color:#810020;  #BA262B;',
      }[this.color]
    },
  },
};
</script>

<style scoped>
#exemplo {
  color: red;
}
</style>
