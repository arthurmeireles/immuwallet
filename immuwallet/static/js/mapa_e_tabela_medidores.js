var kWh_total; // isso é a soma total de kWh dos medidores (usado pra calcular cor maxima)

var classes_cluster = [
    'cluster-small',
    'cluster-medium',
    'cluster-large',
]

function html_popup(medidor) {
    return `<a href="/medidor/${medidor.numero}" target='_blank'><b>Medidor ${medidor.numero}</b></a>
    <div>${medidor.descricao}</div>
    <div>Tensão: ${medidor.tensao} V</div>
    <div>Corrente: ${medidor.corrente} A</div>
    <div>Total no período: ${numero_com_virgula(medidor.total_periodo)} kWh</div>
    <div>Tipo de medição: ${medidor.tipo_medicao}</div>
    <div>${medidor.data_ultima_leitura ? new Date(medidor.data_ultima_leitura).toLocaleString('pt-br') : ''}</div>`;
}

function cluster_tem_alerta(cluster) {
    for (var i of c.getAllChildMarkers()) {
        if (i.options.lista_status)
            // se o medidor estiver ok, lista_status não será uma string vazia
            return true;
    }
    return false;
}

function className(kwh, tipo, tem_alerta) {
    /**
     * Deve retornar a classe (pra dar a cor do cluster no mapa de calor)
     * de acordo com os medidores do cluster..
     * 
     * Todo cluster tem as seguintes classes:
     * - marker-cluster
     * - cluster-geracao ou cluster-consumo
     * - cluster-[small ou medium ou large]-[geracao ou consumo]
     */

    var posicao = kwh / kWh_total * classes_cluster.length | 0;
    posicao = posicao == classes_cluster.length ? classes_cluster.length - 1 : posicao;
    var classe_alerta = tem_alerta ? 'cluster-alerta' : '';
    return `marker-cluster cluster-${tipo} ${classe_alerta} ${classes_cluster[posicao]}-${tipo}`;
}

function iconCreateFunction(cluster) {
    /**
     * Pega o cluster e decide como ele deve ser renderizado
     */
    window.c = cluster;
    var childMarkers = cluster.getAllChildMarkers();

    // CONSUMO
    var kwh_medidores_consumo = childMarkers.filter((i) => i.options.tipo_medicao == "consumo").map((i) => Number(i.options.total_periodo))
    var kwh_consumo = kwh_medidores_consumo.reduce((a, b) => a + b, 0);
    // GERAÇÃO
    var kwh_medidores_geracao = childMarkers.filter((i) => i.options.tipo_medicao == "geracao").map((i) => Number(i.options.total_periodo))
    var kwh_geracao = kwh_medidores_geracao.reduce((a, b) => a + b, 0);

    // número que aparece no cluster
    var kwh = kwh_consumo - kwh_geracao;

    var tipo;
    if (kwh >= 0) tipo = 'consumo';
    else tipo = 'geracao';

    kwh = Math.abs(kwh);

    var tem_alerta = cluster_tem_alerta(cluster);

    // https://stackoverflow.com/a/47582871/6728529
    var icon = {
        html: '<div><span>' + numero_com_virgula(kwh, 0) + ' kWh</span></div>',
        className: className(kwh, tipo, tem_alerta),
        iconSize: new L.Point(40, 40)
    }
    return L.divIcon(icon);
}

var mapa_calor;
var markerClusters;

function updateMapaCalor(medidores) {
    /**
     * Essa função é chamada dentro da função updateMapa, que monta o mapa
     * normal (sem ser de calor). É só pra não repetir a requisição
     */

    // calculando o kWh para cor maxima
    kWh_total = medidores.reduce((a, b) => a + b.total_periodo, 0);

    mapa_calor = mapa_calor ? mapa_calor : L.map('mapa_calor')
    mapa_calor.setView([-5.78804, -36.8441], 8);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiaHVnb2dzb2FyZXMiLCJhIjoiY2sxeTV2MDlhMGphODNkbWxmZXBkYmM3byJ9.5Y03K4Lbi81PngyheSjRfA', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'your.mapbox.access.token'
    }).addTo(mapa_calor);

    $("#show_mapa_calor").click(() => { // justificando: https://stackoverflow.com/a/42400978/6728529 (isso desbuga o mapa)
        setTimeout(() => {
            mapa_calor.invalidateSize();
        }, 200);
    });

    if (markerClusters) markerClusters.clearLayers();
    else {
        markerClusters = L.markerClusterGroup({
            singleMarkerMode: true,
            iconCreateFunction
        });
    }

    medidores.forEach((medidor) => {
        // IGNORA OS QUE NÃO TEM COORDENADAS
        if (!medidor.lat || !medidor.lon) return;

        var marcador = L.marker([medidor.lat, medidor.lon], medidor);
        marcador.bindPopup(html_popup(medidor));
        markerClusters.addLayer(marcador)
    });

    window.p = mapa_calor.addLayer(markerClusters);

    indicador_mapa_carregando(false);
}

function updateMapa(data_inicio, data_fim, medidores_ids) {
    indicador_mapa_carregando(true);
    var params = {
        data_inicio,
        data_fim,
        medidores_ids,
    }
    var url = "/medicao/api/medidores?" + urlencode(params);
    // POSICIONA MEDIDORES
    $.ajax({
        url: url,
        dataType: 'json',
        headers: {
            Authorization: 'Token ' + token_api
        },
        success: function (data) {
            updateMapaCalor(data);
            updateTabela(data);
        }
    });
}

function indicador_mapa_carregando(flag) {
    EventBus.$emit('carregando_algo', flag);
    if (flag) {
        $("#indicador_mapa_carregando").removeClass('hidden');
    } else {
        $("#indicador_mapa_carregando").addClass('hidden');
    }
}





/**
 * COISAS DA TABELA
 */





var language = { lengthMenu: "_MENU_ medidores por página", zeroRecords: "Nenhum medidor", info: "Página _PAGE_ de _PAGES_", infoEmpty: "Nenhum medidor", infoFiltered: "(filtrado de _MAX_)", paginate: { first: "Primeira", last: "Última", next: "Próxima", previous: "Anterior" }, search: "Buscar por:" };

// ao receber respsota da API, vou salvar a ordem das chaves (descricao, numero, lat, lon...)
// isso me ajuda a saber o índice de uma propriedade no datatables
var chaves_objeto_medidor;

var styles = {
    ok:  {
        "classe_css": "badge badge-success",
        "texto": "OK",
        "codigo": "ok"
    },
    sobretensao:  {
        "classe_css": "badge badge-warning",
        "texto": "Sobretensão",
    },
    subtensao:  {
        "classe_css": "badge badge-warning",
        "texto": "Subtensão",
    },
    sobrecorrente:  {
        "classe_css": "badge badge-primary",
        "texto": "Sobrecorrente",
    },
    subcorrente:  {
        "classe_css": "badge badge-primary",
        "texto": "Subcorrente",
    },
    leitura_antiga:  {
        "classe_css": "badge badge-danger",
        "texto": "Leitura antiga",
    }
}

function createdRow(row, data, index) {
    var flag_index = chaves_objeto_medidor.indexOf('lista_status');
    var tem_problema = data[flag_index].indexOf(styles.leitura_antiga.texto) != -1;
    if (tem_problema)
        $(row).addClass("tem_problema");
    $(row).click(() => {
        var numero_index = chaves_objeto_medidor.indexOf('numero');
        window.location.href = `/medidor/${data[numero_index]}`;
    });
}

var columns = [
    null,                       // pode pesquisar por descrição
    null,                       // pode pesquisar por número
    { "searchable": false },
    { "searchable": false },
    { "searchable": false },
    { "searchable": false },
    { "searchable": false },
    null,                       // pode pesquisar por status
    { "searchable": false }
];

var datatable = $("#tabela_medidores").DataTable({ language, createdRow, columns });

formatar_lista_status = function (lista_status) {
    var string = '';
    var lista;
    
    if (!lista_status){
        lista = ['ok'];
    } else {
        lista = lista_status.split(',');
    }
    lista.forEach((i) => {
        string = `${string}<span class="${styles[i].classe_css}">${styles[i].texto}</span>`
    });
    return string;
}

formatar_ultima_leitura = function (ultima) {
    return ultima ? new Date(ultima).toLocaleString('pt-br') : '';
}

function updateTabela(dados) {
    
    if (!dados.length) {
        console.log('sem dados');
        return;
    }
    chaves_objeto_medidor = Object.keys(dados[0]);
    dados = dados.map((i) => {
        i.lista_status = formatar_lista_status(i.lista_status);
        i.data_ultima_leitura = formatar_ultima_leitura(i.data_ultima_leitura);
        return Object.values(i);
    })

    datatable.clear();
    datatable.rows.add(dados);
    datatable.draw();
}

function wrapperUpdateTabela(data_inicio, data_fim, medidores_ids) {
    // indicador_mapa_carregando(true);
    var params = {
        data_inicio,
        data_fim,
        medidores_ids,
    }

    var url = "/medicao/api/medidores?" + urlencode(params);

    $.ajax({
        url: url,
        dataType: 'json',
        headers: {
            Authorization: 'Token ' + token_api
        },
        success: function (data) {
            updateTabela(data);
        }
    });
}