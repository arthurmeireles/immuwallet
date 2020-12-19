import Vue from 'vue'
// import VueResource from 'vue-resource'
import Exemplo from './components/Exemplo.vue'
import Discussao from './components/Discussao.vue'
import Diario from './components/Diario.vue'
// import lodash from 'lodash'

// Vue.use(VueResource, lodash)

window.Vue = Vue;
window.Exemplo = Exemplo;
window.Discussao = Discussao;
window.Diario = Diario;

Vue.component('exemplo', require('./components/Exemplo.vue'));
Vue.component('mensagem-minha', require('./components/MensagemMinha.vue'));
Vue.component('mensagem-dele', require('./components/MensagemDele.vue'));
Vue.component('card-disponibilidade', require('./components/CardDisponibilidade.vue'));
Vue.component('quadro-disponibilidade', require('./components/QuadroDisponibilidade.vue'));

const app = new Vue({
    el: '#appvue',
});
