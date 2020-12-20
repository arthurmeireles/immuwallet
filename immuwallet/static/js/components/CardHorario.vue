<template>
  <div class="col-xs-12 col-sm-6 col-md-4 col-lg-4">
    <div class="widget widget-stats head-box" :style="style">
      <div class="stats-icon">
        <i class="fa fa-eyedropper"></i>
      </div>
      <div class="stats-info">
        <!-- <h4>{{ top }}</h4> -->
        <h4 class="stat-count">{{ mid }}</h4>
        <h6><i class="fa fa-home"></i> {{ submid }}</h6>
      </div>
      <div class="stats-link footer-link">
        <a>
          <span @click="clickEditar" class="pointer">
            <i class="fa fa-pencil-square-o"></i>
            Editar
          </span>
          <span @click="clickExcluir" class="pointer">
            <i class="fa fa-times"></i>
            Excluir
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pk: { type: Number, required: true },
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
  methods: {
    clickEditar() {
      window.location.href = `/editar_horario/${this.pk}`;
    },
    clickExcluir() {
      var vm = this;
      Swal.fire({
        title: "Tem certeza que deseja excluir?",
        showConfirmButton: false,
        showDenyButton: true,
        showCancelButton: true,
        denyButtonText: `Excluir`,
        cancelButtonText: `Cancelar`,
      })
        .then((result) => {
          if (!result.isDenied) return;
          var params = {
            pk: vm.pk,
          };
          var config = {
            method: "DELETE",
            headers: {
            //   "Content-type": "application/json; charset=UTF-8",
              "X-CSRFToken": getCookie("csrftoken"),
            },
          };
          var url = "/api/horarios_funcionamento/?" + urlencode(params);
          return fetch(url, config);
        })
        .then((response) => {
          if (response === undefined) return;
          if (response.ok) {
            Swal.fire("Feito!", "", "success").then((result) => {
              location.reload();
            });
          } else {
            Swal.fire("Houve um problema.", "", "error");
          }
        });
    },
  },
};
</script>

<style scoped>
.pointer {
  cursor: pointer;
}
</style>
