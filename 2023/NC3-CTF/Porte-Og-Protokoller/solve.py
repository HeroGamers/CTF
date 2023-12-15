from enum import Enum
import pandas as pd
import aiohttp
import asyncio

df = pd.read_csv('service-names-port-numbers.csv')
print(df.head())


# Hvilke porte og protokoller benytter den service, der har beskrivelsen <b>VisualAge Pacbase server</b>?
# Hvilke porte og protokoller benytter den service, der har beskrivelsen <em>VisualAge Pacbase server</em>?
# Hvilken service dækker beskrivelsen 'CCSS QSystemMonitor' over?
# <i>Iliad-Odyssey Protocol</i> beskrivelsen bruger hvilke porte og protokoller?
# Hvilke porte og protokoller er <u>web2host</u> registeret til?
# Hvilke services er registreret til 9321/udp?
# 1145/udp bliver brugt af hvilke services?
# Hvad er navnet på de(n) service, der har beskrivelsen <em>dpkeyserv</em>?


# make enum for type of question
class Question(Enum):
    SERVICE_PORTS = 0
    SERVICE_NAME = 1


WEB = "http://77.75.26.174/"
PHPSESSID = ""

current_question = 0
async def answer(session: aiohttp.ClientSession, response):
    print(response)

    if "Dit svar var ikke korrekt." in response:
        print("Wrong answer :/")
        exit(1)

    global current_question
    question_number = int(response.split("<h3>")[1].split("</h3>")[0].split("nr. ")[1].split(":")[0])
    if question_number == current_question:
        print("Already answered")
        return
    else:
        current_question = question_number
    question = response.split("</h3>")[1].split("<form")[0].split("<p>")[1].split("</p>")[0].strip()
    print(question)

    item = None
    port = None
    send_answer = None

    if any(x in question for x in ["porte og protokoller"]):
        question_type = Question.SERVICE_PORTS
    elif any(x in question for x in ["service", "navn"]):
        question_type = Question.SERVICE_NAME
    else:
        print("Unknown question type")
        exit(1)
    print(question_type)

    if ">" in question and "</" in question:
        item = question.split(">")[1].split("</")[0]
    elif "'" in question:
        item = question.split("'")[1]
    elif '"' in question:
        item = question.split('"')[1]
    print(item)

    if "/tcp" in question:
        port_number = question.split("/")[0].strip()
        if " " in port_number:
            port_number = port_number.split(" ")[-1]
        port = (port_number, "tcp")
    elif "/udp" in question:
        port_number = question.split("/")[0].strip()
        if " " in port_number:
            port_number = port_number.split(" ")[-1]
        port = (port_number, "udp")
    print(port)

    if question_type == Question.SERVICE_PORTS:
        if item is not None:
            try:
                send_answer = df[df["Service Name"] == item][["Port Number", "Transport Protocol"]].values.tolist()
            except KeyError:
                pass
            if send_answer is None or len(send_answer) == 0:
                send_answer = df[df["Description"] == item][["Port Number", "Transport Protocol"]].values.tolist()
        else:
            print("No question variables")
            exit(1)
    elif question_type == Question.SERVICE_NAME:
        if port is not None:
            # get Service Name(s) for elements where Port Number and Transport Protocol match
            send_answer = df[(df["Port Number"] == port[0]) & (df["Transport Protocol"] == port[1])]["Service Name"].values.tolist()
        elif item is not None:
            send_answer = df[df["Description"] == item]["Service Name"].values.tolist()
        else:
            print("No question variables")
            exit(1)

    print(send_answer)
    if send_answer is None or len(send_answer) == 0:
        print("No answer :/")
        exit(1)

    # Check if 1D or 2D list
    if isinstance(send_answer[0], list):
        send_answer = ", ".join(set([f"{x[0]}/{x[1]}" for x in send_answer]))
    else:
        send_answer = ", ".join(set(send_answer))
    print(send_answer)

    data = {
        "answer": send_answer,
    }
    print(data)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": WEB + "?play",
        "Origin": WEB,
        "Host": WEB.split("//")[1].split("/")[0],
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Cookie": f"PHPSESSID={PHPSESSID}",
    }

    async with session.post(WEB + "?play", data=data, headers=headers) as response:
        print(response.status)
        res = await response.text()
    await answer(session, res)


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB + "?play") as response:
            print(response.status)
            res = await response.text()

            # Get session cookie PHPSESSID
            global PHPSESSID
            PHPSESSID = str(response.cookies["PHPSESSID"]).split("=")[1].split(";")[0]
            print(PHPSESSID)

            await answer(session, res)

    # NC3{trivia_m4st3r_s4y_wh47_b7c5a01e}


if __name__ == '__main__':
    asyncio.run(main())
