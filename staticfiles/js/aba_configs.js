// os onclick abaixo é porque
// precisa forçar o apex a re-renderizar, se não ele
// buga
// https://github.com/apexcharts/vue-apexcharts/issues/93#issuecomment-623201489
$("#aba_barra").click(function () {
  setTimeout(() => grafico_medicao_barra.updateOptions({}, true), 30)
});

$("#aba_acumulado").click(function () {
  setTimeout(() => grafico_acumulado.updateOptions({}, true), 30)
});

// CHECKBOXES DE MEDIDORES
$(".checkbox-medidor").change(function () {
  $(".config-btn-medidores").removeClass('active');
  var marcados = $(".checkbox-medidor:checked").length;
  var total = $(".checkbox-medidor").length;

  if (marcados == total)
    $("#config_btn_todos").addClass('active');
  else if (marcados == 0)
    $("#config_btn_nenhum").addClass('active');
});

$("#config_btn_todos").click(function () {
  $(".checkbox-medidor").map(function () { this.checked = true; });
});

$("#config_btn_nenhum").click(function () {
  $(".checkbox-medidor").map(function () { this.checked = false; });
});

// FIM CHECKBOXES DE MEDIDORES

// BOTAO VOLTAR PADRAO
$("#voltar_padrao_btn").click(function () {
  $(".config-btn-periodo").removeClass('active');
  $("#config_btn_mes").addClass('active');
  $("#div_periodo_personalizado").removeClass("slidedown").addClass("slideup");

  var inicio = hoje.slice(0, 8) + '01';
  inicio = inicio.split('-').reverse().join('/');
  var fim = hoje.slice(0, 10);
  fim = fim.split('-').reverse().join('/');

  $("#id_data_inicio").val(inicio);
  $("#id_data_fim").val(fim);

  // marcar checkboxes
  $(".checkbox-medidor").map(function () { this.checked = true; });
});

$(".config-btn-periodo").click(function () {
  if (this.id == 'config_btn_personalizado')
    $("#div_periodo_personalizado").removeClass("slideup").addClass("slidedown");
  else
    $("#div_periodo_personalizado").removeClass("slidedown").addClass("slideup");

  var fim = hoje.slice(0, 10).split('-').reverse().join('/');
  var inicio;

  switch (this.id) {
    case 'config_btn_dia':
      inicio = fim;
      legenda_box_consumo = 'Consumidos hoje';
      legenda_box_geracao = 'Gerados hoje';
      titulo_grafico = 'Hoje';
      break;
    case 'config_btn_mes':
      inicio = '01' + fim.substr(2);
      legenda_box_consumo = 'Consumidos nesse mês';
      legenda_box_geracao = 'Gerados nesse mês';
      titulo_grafico = 'Nesse mês';
      break;
    case 'config_btn_ano':
      inicio = '01/01' + fim.substr(5);
      legenda_box_consumo = 'Consumidos nesse ano';
      legenda_box_geracao = 'Gerados nesse ano';
      titulo_grafico = 'Nesse ano';
      break;
    default:
      inicio = '01' + fim.substr(2);
      legenda_box_consumo = '';     // deixando vazio pra preencher na hora de aplicar
      legenda_box_geracao = '';     // deixando vazio pra preencher na hora de aplicar
      titulo_grafico = '';          // deixando vazio pra preencher na hora de aplicar
      break;
  }

  $("#id_data_inicio").val(inicio);
  $("#id_data_fim").val(fim);
});


$("#aplicar_parametros_btn").click(function () {
  ///// captura os valores
  data_inicio = $("#id_data_inicio").val();
  data_fim = $("#id_data_fim").val();

  if (!legenda_box_consumo) { // se está vazio, vamos preencher
    legenda_box_consumo = `Consumidos entre ${data_inicio} e  ${data_fim}`;
    legenda_box_geracao = `Gerados entre ${data_inicio} e  ${data_fim}`;
    titulo_grafico = `Entre ${data_inicio} e  ${data_fim}`;
  }

  // de dd/mm/yyyy pra yyyy-mm-ddd
  data_inicio = data_inicio.split('/').reverse().join('-') + "T00:00:00-03:00";
  data_inicio_grafico = data_inicio + "T00:00:00-03:00";
  data_fim = data_fim.split('/').reverse().join('-') + "T23:59:59-03:00"
  medidores_ids = $(".checkbox-medidor:checked").map(function () { return this.getAttribute('data-medidor-id') }).toArray();

  ///// dispara novas chamadas à API

  // isso faz com que as funções de update sejam chamadas com os valores atualizados
  // de data. O true é pra sinalizar que é obrigatório.
  EventBus.$emit('refresh', true);
});

function preencher_configs_padrao() {
  var datepickerconfig = {
    format: "dd/mm/yyyy",
    endDate: new Date(), // não pode selecionar dias depois de hoje
    language: 'pt-BR',
    autoclose: true
  };
  var date = new Date();
  var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  var lastMonth = new Date();
  date.setDate(1);

  // setar data inicio
  $("#id_data_inicio").datepicker(datepickerconfig).datepicker('setDate', date);
  $("#id_data_fim").datepicker(datepickerconfig).datepicker('setDate', today);

  // marcar checkboxes
  $(".checkbox-medidor").map(function () { this.checked = true; });

  // grafico de barras
  titulo_grafico = 'Últimos 30 dias';
}

preencher_configs_padrao();

/**
 * Abaixo é pra eu botar o icone do botão de configurações
 * pra carregar dependendo se tem coisa carregando ou não.
 * Ao começar um processo, eu notifico nesse evento.
 * Ao encerrar um processo também.
 */
var total_coisas_carregando = 0;
EventBus.$on('carregando_algo', (flag) => {
  if (flag)
    total_coisas_carregando++;
  else
    total_coisas_carregando--;

  if (total_coisas_carregando)
    $("#TooltipDemo i").addClass('fa-spin');
  else
    $("#TooltipDemo i").removeClass('fa-spin');
});