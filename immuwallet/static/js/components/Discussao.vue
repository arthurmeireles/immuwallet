<template>
  <div class="chat-conversation">
    <ul class="conversation-list slimscroll" ref="janela">
      <template v-for="(mensagem, indice) in mensagens">
        <mensagem-minha
          v-if="mensagem.usuario_id == usuario_id"
          :texto="mensagem.texto"
          :nome="mensagem.nome"
          :timestamp="mensagem.timestamp"
          :imagem="mensagem.imagem"
          :key="indice"
        />
        <mensagem-dele
          v-else
          :texto="mensagem.texto"
          :nome="mensagem.nome"
          :timestamp="mensagem.timestamp"
          :imagem="mensagem.imagem"
          :key="indice"
        />
      </template>
    </ul>
    <div class="row">
      <div class="col-sm-9">
        <input
          type="text"
          class="form-control chat-input"
          placeholder="Insira sua mensagem"
          v-model="textoDigitado"
          @keyup.enter="addMensagem"
          :disabled="!ativo"
        />
      </div>
      <div class="col-sm-3">
        <button
          type="submit"
          ref="botao"
          class="btn btn-primary chat-send btn-block waves-effect waves-light"
          @click="addMensagem"
          :disabled="!ativo"
        >Enviar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    usuario_id: { type: [String, Number], required: true },
    usuario_nome: { type: String, required: true },
    solicitacao_id: { type: [String, Number], required: true },
    usuario_imagem_src: { type: String, required: true },
  },
  data() {
    return {
      textoDigitado: undefined,
      discussao_manager: undefined,
    };
  },
  watch: {
    mensagens(){
      this.scroll();
      audio_notificacao_manager.play();
    }
  },
  computed: {
    mensagens() {
      return this.discussao_manager ? this.discussao_manager.mensagens : [];
    },
    ativo() {
      return this.discussao_manager ? this.discussao_manager.ativo : false;
    }
  },
  mounted() {
    this.discussao_manager = new DiscussaoWS(this.solicitacao_id);
  },
  beforeDestroy(){
    this.discussao_manager.destroy();
  },
  methods: {
    addMensagem() {
      if (!this.textoDigitado) return;
      if (!this.ativo) return;

      var adicionou = this.discussao_manager.addMensagem({
        texto: this.textoDigitado,
        usuario_id: this.usuario_id,
        nome: this.usuario_nome,
        imagem: this.usuario_imagem_src
      });

      this.textoDigitado = undefined;
      this.scroll();
    },
    scroll() {
      $(this.$refs.janela)
        .stop()
        .animate(
          {
            scrollTop: $(this.$refs.janela)[0].scrollHeight
          },
          500
        );
    }
  }
};
</script>

<style scoped>
ul {
  max-height: 100%;
  min-height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
}
</style>
