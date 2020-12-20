

///////
//
/// Alerta
//
///////
Vue.component('alerta', {
  name: "Alerta",
  props: {
    url: { type: String, default: '#' },
    hora: { type: String, default: '' },
    descricao: { type: String, default: '' },
    medidor: { type: [String, Number], default: '' },
    bulletcolor: { type: String, default: 'green' },
    badgenew: { type: Boolean, default: false },
  },
  computed: {
    colorclass() {
      return {
        red: "dot-danger",
        yellow: "dot-warning",
        green: "dot-success",
        blue: "dot-info",
        black: "dot-dark",
        gray: "dot-cinza",
      }[this.bulletcolor];
    },
    message() {
      var descricao = `<strong>${this.hora}</strong> ${this.descricao} (#${this.medidor})`;
      return `<a href='${this.url}' style="color: black">${descricao}</a>`;
    }
  },
  template: `
<div class="vertical-timeline-item vertical-timeline-element"
  :class="colorclass">
  <div>
      <span class="vertical-timeline-element-icon bounce-in"></span>
      <div class="vertical-timeline-element-content bounce-in">
          <h4 class="timeline-title" v-html="message">
            <div class="badge badge-danger ml-2" v-if="badgenew">NOVO</div>
          </h4>
      </div>
  </div>
</div>
  `
});

///////
//
/// RegistroAlertas
//
///////
Vue.component('registroalertas', {
  name: "RegistroAlertas",
  props: {},
  data() {
    return {
      alertas: [],
    }
  },
  mounted() {
    this.updateAlarmes();
    EventBus.$on('refresh', this.updateAlarmes);
  },
  methods: {
    transforma_retorno_api(retorno) {
      var cores = {
        sobretensao: "red",
        subtensao: "red",
        sobrecorrente: "blue",
        subcorrente: "blue",
        meta: 'yellow',
        mkmes: 'yellow',
        leitura_antiga: 'gray'
      };
      return {
        url: `/medidor/${retorno.medidor}`,
        hora: retorno.criado_em,
        descricao: retorno.descricao,
        medidor: retorno.identificador,
        bulletcolor: cores[retorno.tipo]
      }
    },
    updateAlarmes() {
      var vm = this;
      var fetchConfig = {
        headers: {
          Authorization: 'Token ' + this.$token_api
        }
      };
      fetch('/medicao/api/notificacoes', fetchConfig).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          return [];
        }
      }).then((data) => {
        vm.alertas = data.map((i) => vm.transforma_retorno_api(i));
      });
    }
  },
  template: `
  <div class="col-lg-4 col-md-4 col-sm-12 mt-3">
    <div class="card-hover-shadow-2x mb-3 card">
        <div class="card-header-tab card-header">
            <div class="card-header-title font-size-lg text-capitalize font-weight-normal">
                Registro de alertas
            </div>
        </div>
        <div v-if="alertas.length" class="altura scroll-area-lg d-flex">
            <div class="scrollbar-container">
                <div class="p-4">
                    <div
                        class="vertical-time-simple vertical-without-time vertical-timeline vertical-timeline--animate vertical-timeline--one-column">
                        <alerta v-for="(alerta, index) in alertas"
                            :url="alerta.url"
                            :hora="alerta.hora"
                            :descricao="alerta.descricao"
                            :medidor="alerta.medidor"
                            :bulletcolor="alerta.bulletcolor"
                            :key="index"></alerta>
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="altura text-center d-flex justify-content-center" style="display: flex; align-items:center;">
          <p>Nenhum alarme.</p>
        </div>
        <!-- <div class="d-block text-center card-footer">
            <button class="btn-shadow btn-wide btn btn-focus">
                <span class="badge badge-dot badge-dot-lg badge-warning badge-pulse">Badge</span>
                Ver todos alarmes
            </button>
        </div> -->
    </div>
  </div>
  `
});




///////
//
/// Notificacao (na página de medidor)
//
///////
Vue.component('notificacao', {
  name: "Notificacao",
  props: {
    titulo: { type: String, default: '' },
    texto: { type: String, default: '' },
    hora: { type: String, default: '' },
    icone: { type: String, default: 'green' },
  },
  computed: {
    iconeclass() {
      return {
        red: "fa-exclamation-circle text-danger",
        yellow: "fa-exclamation-triangle text-warning",
        gray: "fa-exclamation-triangle text-cinza",
        green: "fa-check-circle text-success",
      }[this.icone];
    },
    borderclass() {
      return {
        red: "border-danger",
        yellow: "border-warning",
        gray: "border-cinza",
        green: "border-success",
      }[this.icone];
    }
  },
  template: `
  <div class="vertical-timeline-item vertical-timeline-element">
  <div>
      <span class="vertical-timeline-element-icon bounce-in">
          <div class="timeline-icon" :class="borderclass">
              <i class="fa" :class="iconeclass"></i>
          </div>
      </span>
      <div class="vertical-timeline-element-content bounce-in">
      <h4 class="timeline-title" v-html="titulo"></h4>
          <p>
              <span v-html="texto"></span>
              <small v-html="hora"></small>
          </p>
      </div>
  </div>
</div>
  `
});


///////
//
/// Notificacoes (na página de medidor)
//
///////
Vue.component('notificacoes', {
  name: "Notificacoes",
  props: {
    medidor: { type: Number, required: true },
    criado_em: { type: String, required: true }
  },
  data() {
    return {
      alertas: [],
    }
  },
  mounted() {
    this.updateAlarmes();
    EventBus.$on('refresh', this.updateAlarmes);
  },
  methods: {
    decidir_texto(alarme){
      return ``;
    },
    decidir_icone(alarme){
      return {
        sobretensao: "red",
        subtensao: "red",
        sobrecorrente: "red",
        subcorrente: "red",
        meta: 'yellow',
        mkmes: 'yellow',
        leitura_antiga: 'gray'

      }[alarme.tipo];
    },
    transforma_retorno_api(retorno) {
      return {
        hora: retorno.criado_em,
        texto: this.decidir_texto(retorno),
        titulo: retorno.descricao,
        icone: this.decidir_icone(retorno)
      }
    },
    updateAlarmes() {
      var vm = this;
      var fetchUrl = `/medicao/api/notificacoes?medidor=${this.medidor}`;
      var fetchConfig = {
        headers: {
          Authorization: 'Token ' + this.$token_api
        }
      };
      fetch(fetchUrl, fetchConfig).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          return [];
        }
      }).then((data) => {
        window.data = data; console.log('data:', data);
        var alerta_criado_em = {
          hora: vm.criado_em,
          texto: '',
          titulo: 'Medidor registrado com sucesso!',
          icone: 'green'
        }
        vm.alertas = [
          ...data.map((i) => vm.transforma_retorno_api(i)),
          alerta_criado_em
        ];
      });
    }
  },
  template: `
  <div class="col-sm-12 col-md-3 mt-0">
    <div class="main-card mb-3 card">
        <div class="card-body"><h5 class="card-title mb-3">Notificações</h5>
            <div class="scroll-area-md">
                <div class="scrollbar-container ps">
                    <div class="vertical-time-icons vertical-timeline vertical-timeline--animate vertical-timeline--one-column">
                        
                    <template v-if="alertas.length">
                      <notificacao  v-for="(alerta, index) in alertas"
                      :hora="alerta.hora"
                      :texto="alerta.texto"
                      :titulo="alerta.titulo"
                      :icone="alerta.icone"
                      :key="index"></notificacao>    
                    </template>

                    </div>
                <div class="ps__rail-x" style="left: 0px; bottom: 0px;"><div class="ps__thumb-x" tabindex="0" style="left: 0px; width: 0px;"></div></div><div class="ps__rail-y" style="top: 0px; right: 0px;"><div class="ps__thumb-y" tabindex="0" style="top: 0px; height: 0px;"></div></div></div>
            </div>
        </div>
    </div>
  </div>
  `
});


///////
//
/// Fim
//
///////

Vue.prototype.$token_api = token_api;

const app = new Vue({
  el: '#app',
});