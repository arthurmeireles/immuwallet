import Vue from 'vue'
import Exemplo from './components/Exemplo.vue'

const EventBus = new Vue();
EventBus.variaveis = {};

window.EventBus = EventBus;

Vue.component('exemplo', require('./components/Exemplo.vue'));
Vue.component('fila', require('./components/Fila.vue'));
Vue.component('card', require('./components/Card.vue'));
Vue.component('card-horario', require('./components/CardHorario.vue'));
Vue.component('card-vacina', require('./components/CardVacina.vue'));
Vue.component('agenda', require('./components/Agenda.vue'));
Vue.component('cartao-vacinas', require('./components/CartaoVacinas.vue'));

const app = new Vue({
    el: '#appvue',
});
