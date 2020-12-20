import Vue from 'vue'
// import VueResource from 'vue-resource'
import Exemplo from './components/Exemplo.vue'

const EventBus = new Vue();
EventBus.variaveis = {};

window.EventBus = EventBus;

Vue.component('exemplo', require('./components/Exemplo.vue'));
Vue.component('teste', require('./components/Teste.vue'));
Vue.component('card', require('./components/Card.vue'));

const app = new Vue({
    el: '#appvue',
});
