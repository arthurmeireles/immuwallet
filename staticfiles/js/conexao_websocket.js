function ligar_ws(url, { onopen, onerror, onclose, onmessage }) {
    var _ws = new WebSocket(url);
    _ws.onopen = onopen;
    _ws.onerror = onerror;
    _ws.onclose = onclose;
    _ws.onmessage = onmessage;
    return _ws;
}

var ws;
var protocolo = window.origin.split('://')[0];
protocolo = protocolo == 'https' ? 'wss' : 'ws';
var host = window.origin.split('://')[1];
var ws_url = `${protocolo}://${host}/ws/dashboard/`;
var handlers = {
    // onopen: () => {},
    onerror: (error) => console.log('erro!', error),
    onclose: (closeEvent) => {
        if (closeEvent.code != 1000) { // 1000 indica "fechei porque quis, não reconecte"
            setTimeout(() => {
                console.log('websocket caiu, tentando reconectar');
                ws = ligar_ws(ws_url, handlers);
            }, 5000)
        }
    },
    onmessage: (message) => {
        var data = JSON.parse(message.data);
        if (data.type == 'refresh') {
            EventBus.$emit('refresh');
            console.log('refreshing');
        }
    }
}

ws = ligar_ws(ws_url, handlers);