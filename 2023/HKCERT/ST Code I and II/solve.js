// import fs from 'fs';
import fetch from "node-fetch";
import {FormData, Blob} from "node-fetch";
import QRCode from 'qrcode-svg';
import jsQR from 'jsqr';
import sharp from 'sharp';
import fs from 'fs';

const SERVER = 'http://stcode-3983gi.hkcert23.pwnable.hk:28211';
const flag1 = 'hkcert23{ST_ST&s4_STegan0graphy--STeg0}';
// const flag1ST = encodeST(flag1, encodeQR(flag0));

// encodeST and decodeST are based on RegExp
function encodeST(data, svg) {
    // Convert data to binary array
    const data_bin = data.split('').map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join('');
    console.log(data_bin);

    // Count number of rect elements in svg
    const num_rects = (svg.match(/<rect/g) || []).length;
    // If number of rects is not enough, add more
    if (num_rects < data_bin.length) {
        // First remove end tag
        svg = svg.replace('</svg>', '');
        // For each bit of data, add a rect element
        svg += '<rect x="0" y="0" width="0" height="0" fill="none" />';
        for (let i = 0; i < data_bin.length - num_rects; i++) {
            svg += '<rect x="0" y="0" width="0" height="0" fill="none" />';
        }
        // Add back end tag
        svg += '</svg>';
    }

    // Create the encoded svg by adding a rx attribute to all rect elements (except the first one)
    // each rx attribute is a bit of the data
    let i = -1;
    const encoded_svg = svg.replace(/<rect/g, (match, offset) => {
        i++;
        if (i === 0) {
            return match;
        }
        return `<rect rx="${data_bin[i - 1]}"`;
    });

    console.log(encoded_svg);

    return encoded_svg;
}

function decodeST(svg) {

}

function encodeQR(data) {
    return new QRCode(data).svg();
}

async function decodeQR(svg) {
    try {
        const {data, info} = await sharp(new Buffer(svg)).ensureAlpha().raw().toBuffer({resolveWithObject: true});
        const output = await jsQR(new Uint8ClampedArray(data.buffer), info.width, info.height);
        return output.data;
    } catch (e) {
        console.log(e);
        return null;
    }
}

async function uploadFile(file, cookies) {
    // Send POST request to flag2 with cookie and svg payload of flag1
    const data = new FormData();
    data.append("svg", new Blob([file]));
    const res2 = await fetch(SERVER + '/flag2', {
        method: 'POST',
        headers: {
            'Cookie': cookies,
        },
        body: data,
    });

    return await res2.text();
}

async function solve() {
    console.log("Getting session cookies...")
    // Send fetch request to flag2 to get cookie, do not allow redirects
    const res = await fetch(SERVER + "/flag2", {
        method: 'GET',
        redirect: 'manual'
    });
    // Get connect.sid cookie
    const cookies = res.headers.get('set-cookie');
    console.log("Cookies: " + cookies);

    console.log("Sending POST request to flag2...")

    const flag1_qr = encodeQR(flag1);
    // console.log(flag1_qr);

    // Save flag1 to file
    // fs.writeFileSync('files/flag1_2.svg', flag1_qr);

    // Try to decode
    const flag1_decoded = await decodeQR(flag1_qr);
    console.log("Decoded: " + flag1_decoded);

    // Send POST request to flag2 with cookie and svg payload of flag1
    let res_text = await uploadFile(flag1_qr, cookies);

    // Print response
    console.log(res_text);

    // Loop 15 times
    for (let i = 0; i < 15; i++) {
        // Get QRCode text ans STCode from res_text
        const qr_text = res_text.split("QRCode:")[1].split("STCode:")[0].trim();
        const st_text = res_text.split("STCode:")[1].split("Your have")[0].trim();

        // Generate QRCode from qr_text
        const qr = await encodeQR(qr_text);
        const st_encoded_qr = await encodeST(st_text, qr);

        // Upload ST-encoded QR to /flag2
        res_text = await uploadFile(st_encoded_qr, cookies);
        console.log(res_text);
    }
}

// Run solve (it's async)
solve();
