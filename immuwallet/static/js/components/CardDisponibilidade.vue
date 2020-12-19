<template>
  <li class="task-low">
    <div class="widget-bg-color-icon">
      <div class="avatar-lg rounded-circle float-left" :class="colorclass">
        <span class="font-24 avatar-title text-white">{{numero}}</span>
      </div>
      <div class="text-right">
        <h3 class="text-dark mt-1">
          <span class="counter">{{texto}}</span>
        </h3>
      </div>
      <div class="clearfix"></div>
    </div>

    <div class="clearfix"></div>
    <div class="row">
      <div class="col">
        <div class="text-right">
          <p class="font-13 mt-2 mb-0">
            <i class="mdi mdi-calendar"></i>
            {{data}}
          </p>
        </div>
      </div>
    </div>
  </li>
</template>

<script>
const zeroPad = (num, places) => String(num).padStart(places, '0')

export default {
  props: {
    texto: { type: String, required: true },
    numero: { required: true },
    timestamp: { type: Number, required: true },
    cor: { type: String, required: true }
  },
  data() {
    var colorclass = {
      vermelho: "bg-icon-danger",
      verde: "bg-icon-success",
      amarelo: "bg-icon-warning"
    }[this.cor];
    return {
      colorclass: colorclass
    };
  },
  mounted() {},
  computed: {
    data() {
      var data = new Date(this.timestamp);
      var mes = zeroPad(data.getMonth() + 1, 2);
      return `${data.getHours()}:${data.getMinutes()} ${data.getDate()}/${mes}/${data.getFullYear()} `;
    }
  }
};
</script>

<style scoped>
</style>
