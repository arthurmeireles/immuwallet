function getCookie(a) {
    return document.cookie.length > 0 && (c_start = document.cookie.indexOf(a + "="), c_start != -1) ? (c_start = c_start + a.length + 1, c_end = document.cookie.indexOf(";", c_start), c_end == -1 && (c_end = document.cookie.length), unescape(document.cookie.substring(c_start, c_end))) : ""
}
$.fn.serializeJSON = function() {
    var a = this.serializeArray(),
        b = "{";
    for (var c in a) {
        var d = a[c];
        b += '"' + d.name + '":"' + d.value + '",'
    }
    var e = b.length - 1;
    return b = b.substr(0, e), b += "}", JSON.parse(b)
}, $.fn.dataTable.pipeline = function(a) {
    var b = $.extend({
            pages: 5,
            url: "",
            data: null,
            method: "GET"
        }, a),
        c = -1,
        d = null,
        e = null,
        f = null;
    return function(a, g, h) {
        var i = !1,
            j = a.start,
            k = a.start,
            l = a.length,
            m = j + l;
        if (h.clearCache ? (i = !0, h.clearCache = !1) : c < 0 || j < c || m > d ? i = !0 : JSON.stringify(a.order) === JSON.stringify(e.order) && JSON.stringify(a.columns) === JSON.stringify(e.columns) && JSON.stringify(a.search) === JSON.stringify(e.search) || (i = !0), e = $.extend(!0, {}, a), i) {
            if (j < c && (j -= l * (b.pages - 1), j < 0 && (j = 0)), c = j, d = j + l * b.pages, a.start = j, a.length = l * b.pages, $.isFunction(b.data)) {
                var n = b.data(a);
                n && $.extend(a, n)
            } else $.isPlainObject(b.data) && $.extend(a, b.data);
            h.jqXHR = $.ajax({
                type: b.method,
                url: b.url,
                data: a,
                dataType: "json",
                cache: !1,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                success: function(a) {
                    a.data = a.result, delete a.result, f = $.extend(!0, {}, a), c != k && a.data.splice(0, k - c), l >= -1 && a.data.splice(l, a.data.length), (b.process) ? g(b.process(a)) : g(a)
                }
            })
        } else json = $.extend(!0, {}, f), json.draw = a.draw, json.data.splice(0, j - c), json.data.splice(l, json.data.length), g(json)
    }
}, $.fn.dataTable.Api.register("clearPipeline()", function() {
    return this.iterator("table", function(a) {
        a.clearCache = !0
    })
});
