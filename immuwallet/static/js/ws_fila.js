protocolo = window.origin.split('://')[0];
host = window.origin.split('://')[1];

env = {
    WS_HOST: host,
    WS_PROTOCOL: protocolo == 'https' ? 'wss' : 'ws',
    WS_TIMEOUT: 10000, // quanto tempo esperar antes de tentar reconexão
}

function ligar_ws(url, { onopen, onerror, onclose, onmessage }) {
    var _ws = new WebSocket(url);
    _ws.onopen = onopen;
    _ws.onerror = onerror;
    _ws.onclose = onclose;
    _ws.onmessage = onmessage;
    return _ws;
}

class FilaWS {
    constructor(estabelecimento_id) {
        this.estabelecimento_id = estabelecimento_id;

        this.ativo = false;

        this.ws_url = `${env.WS_PROTOCOL}://${env.WS_HOST}/ws/fila/${estabelecimento_id}/`;

        this.ws_handlers = {
            onopen: () => {
                this.ativo = true;
            },
            onerror: (error) => console.error(error),
            onclose: (closeEvent) => {
                this.ativo = false;
                if (closeEvent.code != 1000) { // 1000 indica "fechei porque quis, não reconecte"
                    console.log('websocket caiu, tentando reconectar');
                    setTimeout(() => {
                        this.ws = ligar_ws(this.ws_url, this.ws_handlers);
                    }, env.WS_TIMEOUT)
                } else {
                    console.log('encerrando WS');
                }
            },
            onmessage: (message) => {
                var message = JSON.parse(message.data);
                // window.m = message;
                if (message.type == 'reload' && message.value == EventBus.variaveis.estabelecimento)
                    EventBus.$emit('select_estabelecimento');
            }
        }

        this.ws = ligar_ws(this.ws_url, this.ws_handlers);
    }

    destroy(mensagem) {
        this.ws.close(1000);
    }
}

var fila_ws = new FilaWS(EventBus.variaveis.estabelecimento);