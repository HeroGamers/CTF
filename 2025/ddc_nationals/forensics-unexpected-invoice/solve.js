function dec2(base64) {
    var xml = new ActiveXObject("MSXML2.DOMDocument.3.0");
    var el = xml.createElement("base64");
    el.dataType = "bin.base64";
    el.text = base64;
    var bin = el.nodeTypedValue;

    var stream = new ActiveXObject("ADODB.Stream");
    stream.Type = 1;
    stream.Open();
    stream.Write(bin);
    stream.Position = 0;
    stream.Type = 2;
    stream.Charset = "utf-8";
    var str = stream.ReadText();
    stream.Close();
    return str;
}

function dec(str, key) {
    str = dec2(str)
    var result = "";
    for (var i = 0; i < str.length; i++) {
        var charCode = str.charCodeAt(i);
        var keyCharCode = key.charCodeAt(i % key.length);
        result += String.fromCharCode(charCode ^ keyCharCode);
        
    }
    return result;
}

console.log(dec("NAIIFzAuMlg1AyQNDgRMMS1qcgpgKx4cMQAEaDs3PDIFXyccFAIBRhZkHCkvIVIwAxA7GxsWMTg8", "w8T@Y@V7Bpx^w"));
console.log(dec("dTVUDD0rbzYAVUlVH3d5FwolNWItAVNfCx1vMBdLJTUmc0UYXwhSNyQfADgqYToRVxZaTD0u", "XVteJYO^t!9&%"));