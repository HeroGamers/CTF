import aiohttp
import asyncio
import aiofiles
from lxml import etree
import qrcode
import requests
import qrcode.image.svg
from bs4 import BeautifulSoup

URL = "http://stcode-3983gi.hkcert23.pwnable.hk:28211"
session: aiohttp.ClientSession


async def generateQR(data: str) -> str:
    """
    Generates a QR code as SVG.
    """
    factory = qrcode.image.svg.SvgImage
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    #     image_factory=factory,
    # )
    # qr.add_data(data)
    # qr.make(fit=True)
    # img = qr.make_image(fill_color="black", back_color="white")
    #
    # image = img.get_image()

    img = qrcode.make(data, image_factory=factory)
    image = img.get_image()

    return etree.tostring(image).decode()


async def encodeST(st: str, qr_code: BeautifulSoup):
    """
    Encodes the given ST string into the QR code in binary.
    """
    binary = bin(int.from_bytes(st.encode(), "big"))[2:]
    print(binary)


async def decode_ST(svg: BeautifulSoup):
    # For each rect, check if rx is set, if it is read it into a list
    rx = ''
    for rect in svg.find_all("rect"):
        if "rx" in rect.attrs:
            rx += rect["rx"]
    # We get a binary string
    # print(rx)

    # Decode binary string to ascii
    # print(int(rx, 2))
    st = bytes.fromhex(hex(int(rx, 2))[2:]).decode("utf-8")
    return st


async def flag1():
    async with session.get(URL + "/flag1") as resp:
        svg = await resp.text()
        soup = BeautifulSoup(svg, 'xml')
        # print(soup.prettify())
        flag_1 = await decode_ST(soup)
    #     async with aiofiles.open("files/flag1.svg", "w") as f:
    #         await f.write(svg)
    # output = await readQR("files/flag1.svg")
    return svg, flag_1


async def flag2(flag_1):
    async with session.get(URL + "/flag2") as resp:
        res_text = await resp.text()
        soup = BeautifulSoup(res_text, 'html.parser')
        # print(soup.prettify())
        # Send an svg that contains the QRCode of flag1
        # curl http://stcode-3983gi.hkcert23.pwnable.hk:28211/flag2 -F svg=@YOUR_PAYLOAD_FILE --cookie "connect.sid="


    # Send flag_1 as file
    flag_1_qr = await generateQR(flag_1)
    print(flag_1_qr)


    data = aiohttp.FormData()
    payload_file = "files/flag1.svg"
    async with aiofiles.open(payload_file, "w") as f:
        await f.write(flag_1_qr)
    data.add_field('svg', open(payload_file, 'rb'))

    async with session.post(URL + "/flag2", data=data) as resp:
        res_text = await resp.text()
        soup = BeautifulSoup(res_text, 'html.parser')
        print(soup.prettify())


    # Try using requests
    files = {"svg": (payload_file, open(payload_file, 'rb'))}
    cookies = {"connect.sid": session.cookie_jar.filter_cookies(URL).get("connect.sid").value}
    resp = requests.post(URL + "/flag2", files=files, cookies=cookies)
    print(resp.text)


async def main():
    # flag = "hkcert23{ST_ST&s4_STegan0graphy--STeg0}"
    # qr_code_xml = await generateQR(flag)
    # soup = BeautifulSoup(qr_code_xml, 'xml')
    # async with aiofiles.open("files/flag1.svg", "w") as f:
    #     await f.write(qr_code_xml)
    # print(soup.prettify())
    #
    # return

    global session
    session = aiohttp.ClientSession()

    flag_1_svg, flag_1 = await flag1()
    print(f"Flag 1: {flag_1}")
    flag_2 = await flag2(flag_1)

    await session.close()
    pass

if __name__ == "__main__":
    asyncio.run(main())