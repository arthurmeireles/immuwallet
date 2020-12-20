<template>
  <div>
    <ul>
      <p v-if="!items.length">Vazio!</p>
      <card-horario
        v-else
        v-for="(item, i) in items"
        :key="i"
        :pk="item.pk"
        :mid="item.nome"
        :submid="item.estabelecimento.nome"
        :color="color(item)"
      />
    </ul>
  </div>
</template>

<script>

export default {
  data() {
    return {
      items: [],
    };
  },
  mounted() {
    this.update_items(usuario_estabelecimento);
  },
  methods: {
    color(item) {
      var cor = "blue";
      // if (item.paciente.id == usuario_id) cor = "lightblue";
      // if (item.status == HORA_STATUS.ATENDIMENTO) cor = "red";
      return cor;
    },
    update_items(key) {
      var params = {
        key,
      };

      var url = "/api/horarios_funcionamento/?" + urlencode(params);

      fetch(url)
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            return [];
          }
        })
        .then((data) => {
          this.items = data;
        });
    },
    click(item) {
      if (usuario_perfil == PERFIL.PACIENTE) return;
      if (item.status == HORA_STATUS.ATENDIMENTO) {
        Swal.fire({
          title: "O que deseja fazer?",
          showDenyButton: true,
          showCancelButton: true,
          confirmButtonText: `Concluir`,
          denyButtonText: `Voltar pra fila`,
        })
          .then((result) => {
            var data = {
              id: item.id,
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
            id: item.id,
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
