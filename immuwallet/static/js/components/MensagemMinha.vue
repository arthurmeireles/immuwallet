<template>
  <li class="clearfix odd">
    <div class="chat-avatar">
      <img :src="imagem" />
    </div>
    <div class="conversation-text">
      <div class="ctext-wrap">
        <i>{{nome}}</i>
        <i>{{datetime}}</i>
        <p>{{texto}}</p>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  props: {
    texto: {type: String, required: true},
    nome: {type: String, required: true},
    timestamp: {type: Number, required: true},
    imagem: {type: String, required: true},
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {
    datetime(){
      var date = new Date(this.timestamp * 1000);
      return date.toLocaleString('pt-BR');
    }
  }
};
</script>

<style scoped>
#exemplo {
  color: red;
}
</style>
