<template>
  <div>
    <ul>
      <p v-if="!horas_marcadas.length">Vazio!</p>
      <card
        v-else
        v-for="(hora, i) in horas_marcadas"
        :key="i"
        :top="hora.vacina.nome"
        :mid="`${i + 1} - ${hora.paciente.get_full_name}`"
        :submid="submid(hora)"
        :bottom1="hora.data"
        :bottom2="hora.estabelecimento.nome"
        :color="color(hora)"
        @click.native="click(hora)"
      />
    </ul>
  </div>
</template>

<script>
const HORA_STATUS = {
  MARCADO: 0,
  ATENDIMENTO: 1,
  CANCELADO: 2,
  CONCLUIDO: 3,
};
export default {
  data() {
    return {
      horas_marcadas: [],
    };
  },
  mounted() {
    var self = this;
    EventBus.$on("select_estabelecimento", function () {
      self.update_horas_marcadas(EventBus.variaveis.estabelecimento);
    });
  },
  methods: {
    submid(hora) {
      return {
        [HORA_STATUS.MARCADO]: "Aguardando",
        [HORA_STATUS.ATENDIMENTO]: "Em atendimento",
        [HORA_STATUS.CANCELADO]: "Cancelado",
        [HORA_STATUS.CONCLUIDO]: "Concluído",
      }[hora.status];
    },
    color(hora) {
      var cor = "blue";
      if (hora.paciente.id == usuario_id) cor = "lightblue";
      if (hora.status == HORA_STATUS.ATENDIMENTO) cor = "red";
      return cor;
    },
    update_horas_marcadas(estabelecimento) {
      var params = {
        estabelecimento,
      };

      var url = "/api/horas_marcadas/?" + urlencode(params);

      fetch(url)
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            return [];
          }
        })
        .then((data) => {
          this.horas_marcadas = data;
        });
    },
    click(hora) {
      if (usuario_perfil == PERFIL.PACIENTE) return;
      if (hora.status == HORA_STATUS.ATENDIMENTO) {
        Swal.fire({
          title: "O que deseja fazer?",
          showDenyButton: true,
          showCancelButton: true,
          confirmButtonText: `Concluir`,
          denyButtonText: `Voltar pra fila`,
        })
          .then((result) => {
            var data = {
              id: hora.id,
              status: HORA_STATUS.CONCLUIDO,
            };
            var config = {
              method: "POST",
              body: JSON.stringify(data),
              headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": getCookie("csrftoken"),
              },
            };
            if (result.isConfirmed) {
              return fetch("/api/horas_marcadas/", config);
            } else if (result.isDenied) {
              data.status = HORA_STATUS.MARCADO;
              config.body = JSON.stringify(data);
              return fetch("/api/horas_marcadas/", config);
            }
          })
          .then((response) => {
            if (response === undefined) return;
            if (response.ok) {
              Swal.fire("Feito!", "", "success");
            } else {
              Swal.fire("Houve um problema.", "", "error");
            }
          });
        return;
      }
      Swal.fire({
        title: "O que deseja fazer?",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Atender`,
        denyButtonText: `Remover da fila`,
      })
        .then((result) => {
          var data = {
            id: hora.id,
            status: HORA_STATUS.ATENDIMENTO,
          };
          var config = {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
              "Content-type": "application/json; charset=UTF-8",
              "X-CSRFToken": getCookie("csrftoken"),
            },
          };
          if (result.isConfirmed) {
            return fetch("/api/horas_marcadas/", config);
          } else if (result.isDenied) {
            data.status = HORA_STATUS.CONCLUIDO;
            config.body = JSON.stringify(data);
            return fetch("/api/horas_marcadas/", config);
          }
        })
        .then((response) => {
          if (response === undefined) return;
          if (response.ok) {
            Swal.fire("Feito!", "", "success");
          } else {
            Swal.fire("Houve um problema.", "", "error");
          }
        });
    },
  },
};
</script>

<style scoped>
</style>
