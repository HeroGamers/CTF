from fastapi import FastAPI, Request
import aiohttp
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import datetime
import aiofiles
import json

MAIN_SERVER = "http://10.10.2.13:31337"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

session: aiohttp.ClientSession = None

# Define all teams from 0 to 10
teams = list(range(10))
games = {
    -1: {
    "your_turn": True,
    "game_result": "",
    "moves": [
        {
        "x": 0,
        "y": 2,
        "move_type": False,
        "move_number": 0
        },
        {
        "x": 1,
        "y": 1,
        "move_type": True,
        "move_number": 1
        }
    ]
    }
}

flag_times = {}
last_win = {}

async def recover_flags():
    global flag_times
    try:
        async with aiofiles.open("flag_times.json", "r") as f:
            flag_times = json.loads(await f.read())
        
        if not flag_times:
            print("No flag_times found")
            flag_times = {}
            return
        
        # convert time to datetime
        for flag in flag_times:
            flag_times[flag]["time"] = datetime.datetime.strptime(flag_times[flag]["time"], "%Y-%m-%d %H:%M:%S")
        
        print(f"Recovered flag_times: {flag_times}")
    except Exception as e:
        print(f"Error reading flag_times: {e}")


async def get_state(team_id):
    # Get the state of the game by making a POST request to the main server to /state with team_id in body
    print(f"Getting state for team {team_id}")
    if not team_id in games:
        games[team_id] = {}

    try:
        async with session.post(f"{MAIN_SERVER}/state", json={"team_id": team_id}) as response:
            response = await response.json()
            print(f"Response for team {team_id}: {response}")

            # Add flag if in game_result
            if "game_result" in response and "CTFZone" in response["game_result"]:
                flag = response["game_result"]
                
                # Update last win
                last_win[team_id] = datetime.datetime.now()

                # Add time when flag was received
                if flag not in flag_times:
                    flag_times[flag] = {
                        "team": team_id,
                        "time": datetime.datetime.now()
                    }

                    # cache the flag_times
                    async with aiofiles.open("flag_times.json", "w") as f:
                        serializable_flag_times = {flag: {"team": flag_times[flag]["team"], "time": flag_times[flag]["time"].strftime("%Y-%m-%d %H:%M:%S")} for flag in flag_times}
                        print(f"Writing flag_times: {serializable_flag_times}")
                        await f.write(json.dumps(serializable_flag_times))

            # Check if your_turn, game_result, moves are in the response
            if any(key not in response for key in ["your_turn", "game_result", "moves"]):
                print(f"Invalid response: {response}")
                games[team_id] = response
                return response
            games[team_id] = response
            return response
    except Exception as e:
        print(f"Error getting state for team {team_id}: {e}")
        games[team_id] = {"error": str(e)}
        return None

async def get_board(game):
    # Draw the board based on the game state, using HTML table
    board = '<table class="board">'
    for y in range(3):
        board += "<tr>"
        for x in range(3):
            cell = [cell for cell in game["moves"] if cell["x"] == x and cell["y"] == y]
            if not cell:
                board += "<td></td>"
                continue
            cell = cell[0]
            if cell["move_type"]:
                board += "<td>X</td>"
            else:
                board += "<td>O</td>"
        board += "</tr>"
    board += "</table>"
    return board


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global session
    if not session:
        session = aiohttp.ClientSession()
    if not flag_times:
        await recover_flags()

    # make a courotine task to get the state of the game for each team
    tasks = [get_state(team) for team in teams]
    await asyncio.gather(*tasks)

    # Get game state for each time and draw the boards for each team using HTML table
    team_responses = []
    for team in teams:
        team_response = []
        team_response.append('<div class="team column">')
        team_response.append(f"<h2>Team {team}</h2>")

        # recent_flag_times = [flag_times[flag] for flag in team_flags[team]]
        # # flag is recent if we have any flag in the last 2 minutes
        # is_recent = any([datetime.datetime.now() - datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") < datetime.timedelta(minutes=2) for time in recent_flag_times])

        if team in last_win and last_win[team]:
            team_response.append(f"""<p style = "color: {"green" if (datetime.datetime.now() - last_win[team] < datetime.timedelta(minutes=2)) else "red"}">Last win: {last_win[team].strftime("%Y-%m-%d %H:%M:%S")}</p>""")

        last_3_flags = sorted([flag for flag in flag_times if flag_times[flag]["team"] == team], key=lambda x: flag_times[x]["time"], reverse=True)[:3]

        flag_times_str_arr = [f'<p style="color: {"green" if (datetime.datetime.now() - flag_times[flag]["time"] < datetime.timedelta(minutes=3)) else "red"}">{flag_times[flag]["time"].strftime("%Y-%m-%d %H:%M:%S")}: {flag}</p>' for flag in last_3_flags]
        team_flags_str = "".join(flag_times_str_arr)
        team_response.append(f'<div class="flags">Last 3 flags: {team_flags_str}</div>')

        state = games[team]
        if not state or "error" in state:
            print(f"Error getting state when doing team {team}: {state}")
            team_response.append(f"<p>Error getting state: {state}</p>")
            team_response.append("</div>")
            team_responses.append(team_response)
            continue
        team_response.append(f"<p>Game result: {state['game_result'] if 'game_result' in state else 'Unknown'}</p>")
        team_response.append("<p>Your turn</p>" if state["your_turn"] else "<p>Not your turn</p>")
        board = await get_board(state)
        if not board:
            print(f"Invalid board for team {team}: {board}")
            team_response.append(f"<p>Invalid board: {board}</p>")
            team_response.append("</div>")
            team_responses.append(team_response)
            continue
        team_response.append(board)
        team_response.append("</div>")

        team_responses.append(team_response)
    
    response = []
    # For each second team, make a row with two teams
    for i in range(0, len(teams), 4):
        if i >= len(team_responses):
            break

        response.append('<div class="row">')
        if i < len(team_responses):
            response.extend(team_responses[i])
        if i + 1 < len(team_responses):
            response.extend(team_responses[i + 1])
        if i + 2 < len(team_responses):
            response.extend(team_responses[i + 2])
        if i + 3 < len(team_responses):
            response.extend(team_responses[i + 3])
        response.append('</div>')
    
    return templates.TemplateResponse(
        request=request, name="board.html", context={"board": "\n".join(response)}
    )
