function numero_com_virgula(numero, casas_decimais = 2){
  try {
    return Number(numero).toFixed(casas_decimais).replace('.',',');
  } catch (e) {
    return (0).toFixed(casas_decimais).replace('.',',')
  }
  
}

function urlencode(obj) {
  var str = [];
  for (var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}