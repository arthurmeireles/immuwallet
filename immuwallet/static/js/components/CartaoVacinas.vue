<template>
  <div>
    <ul>
      <p v-if="!items.length">Vazio!</p>
      <card-vacina
        v-else
        v-for="(item, i) in items"
        :key="i"
        :pk="item.id"
        :top="item.data"
        :mid="item.vacina.nome"
        :submid="submid(item)"
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
    submid(item) {
      if (item.hora_marcada){
        return item.hora_marcada.estabelecimento.nome;
      }
    },
    color(item) {
      var cor = "blue";
      // if (item.paciente.id == usuario_id) cor = "lightblue";
      // if (item.status == HORA_STATUS.ATENDIMENTO) cor = "red";
      return cor;
    },
    update_items(key) {
      var url = `/api/vacinas/${usuario_id}/`;

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
  },
};
</script>

<style scoped>
</style>
