<template>
  <div class="row">
    <!-- UTI -->

    <div class="col-lg-4">
      <div class="card-box">
        <h4 class="header-title">
          UTI
          <span class="float-right">
            <ControleSom v-model="tocar_uti" />
          </span>
        </h4>

        <ul class="sortable-list tasklist list-unstyled mt-4" id="upcoming">
          <card-disponibilidade
            v-for="(item, indice) in uti"
            :key="indice"
            :texto="item.nome"
            :numero="item.qtd"
            :timestamp="item.timestamp"
            :cor="'vermelho'"
          ></card-disponibilidade>

          <li class="task-placeholder centro" v-if="!uti.length">Nenhum leito de UTI</li>
        </ul>
      </div>
    </div>

    <!-- UCI -->

    <div class="col-lg-4">
      <div class="card-box">
        <h4 class="header-title">
          UCI
          <span class="float-right">
            <ControleSom v-model="tocar_uci" />
          </span>
        </h4>
        <ul class="sortable-list tasklist list-unstyled mt-4" id="inprogress">
          <card-disponibilidade
            v-for="(item, indice) in uci"
            :key="indice"
            :texto="item.nome"
            :numero="item.qtd"
            :timestamp="item.timestamp"
            :cor="'amarelo'"
          ></card-disponibilidade>

          <li class="task-placeholder centro" v-if="!uci.length">Nenhum leito de UCI</li>
        </ul>
      </div>
    </div>

    <!-- ENFERMARIA -->

    <div class="col-lg-4">
      <div class="card-box">
        <h4 class="header-title">
          Enfermaria
          <span class="float-right">
            <ControleSom v-model="tocar_enfermaria" />
          </span>
        </h4>

        <ul class="sortable-list tasklist list-unstyled mt-4" id="completed">
          <card-disponibilidade
            v-for="(item, indice) in enfermaria"
            :key="indice"
            :texto="item.nome"
            :numero="item.qtd"
            :timestamp="item.timestamp"
            :cor="'verde'"
          ></card-disponibilidade>

          <li class="task-placeholder centro" v-if="!enfermaria.length">Nenhum leito de Enfermaria</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import ControleSom from "./ControleSom.vue";

export default {
  components: {
    ControleSom
  },
  props: {
    central_id: { type: Number, required: true }
  },
  data() {
    return {
      ws_manager: new DisponibilidadeWS(this.central_id),
      audio_manager: new FilaAudioPlayer(),
      audios: undefined,
      should_play: false,
      tocar_uti: true,
      tocar_uci: true,
      tocar_enfermaria: true,
    };
  },
  beforeDestroy() {
    this.ws_manager.destroy();
  },
  mounted() {
    window.audio_manager = this.audio_manager;
    var json = "/static/assets/audio/audios.json";
    $.getJSON(json, data => {
      this.audios = data;
    }).then(() => {
      setTimeout(() => {
        this.should_play = true;
      }, 2000);
    });
  },
  watch: {
    uti(novo, antigo) {
      this.checar_novidade(novo, antigo, "uti");
    },
    uci(novo, antigo) {
      this.checar_novidade(novo, antigo, "uci");
    },
    enfermaria(novo, antigo) {
      this.checar_novidade(novo, antigo, "enfermaria");
    }
  },
  computed: {
    uti() {
      return this.ws_manager.uti;
    },
    uci() {
      return this.ws_manager.uci;
    },
    enfermaria() {
      return this.ws_manager.enfermaria;
    }
  },
  methods: {
    checar_novidade(novo, antigo, tipo) {
      for (var item of novo) {
        var qs_antigo = antigo.filter(i => i.id == item.id);
        if (!qs_antigo.length) {
          // não tinha nada desse lugar, agora tem
          this.tocar_audio(`${item.id}_${tipo}`);
        } else if (item.qtd > qs_antigo[0].qtd) {
          // já tinha, só que agora tem mais
          this.tocar_audio(`${item.id}_${tipo}`);
        }
      }
    },
    toggle() {
      console.log("toggle", arguments);
    },
    tocar_audio(chave) {
      if (!this.should_play) return;

      var tipo = chave.split("_")[1];
      if (!this[`tocar_${tipo}`]) return;

      var src = this.audios[chave]
        ? this.audios[chave]
        : this.audios["default"];
      this.audio_manager.play(src);
    }
  }
};
</script>

<style scoped>
.centro {
  text-align: center;
}
</style>
