import json
import pathlib

def analyze(challenges, rankings: list[dict]):
    unsolved_challs = [challenge for challenge in challenges['challenges'] if challenge['id'] not in [solved['challenge_id'] for solved in challenges['solved']]]
    current_score = sum([challenge['point'] for challenge in challenges['challenges'] if challenge['id'] in [solved['challenge_id'] for solved in challenges['solved']]])
    print(f"Current score: {current_score} points")
    # sort by solved count, then category, then name
    unsolved_challs.sort(key=lambda x: (x['solved'], x['category'], x['name']), reverse=True)
    print(f"Unsolved challenges: {len(unsolved_challs)}/{len(challenges['challenges'])}")
    print(f"Checking how many challs to solve to surpass teams, based on probability of solving unsolved challs with the most solves:")
    points = 0
    # take top 8 teams
    rankings.sort(key=lambda x: x['score'], reverse=True)
    # add a ranking to each team
    for i, team in enumerate(rankings):
        team['ranking'] = i + 1
    rankings = rankings[:8]
    for challenge in unsolved_challs:
        points += challenge['point']
        # if current points + current challenge points is greater than a team in rankings, remove that team, and get the team names
        surpass_teams = [team for team in rankings if current_score + points > team['score']]
        surpass_teams_string = ""
        if surpass_teams:
            ranking = min([team['ranking'] for team in surpass_teams])
            surpass_teams_string = f""" - Get #{ranking} with {current_score + points} (+{points}) points and surpass: {', '.join([f"{team['team_name']} ({team['score']})" for team in surpass_teams])}"""
            # remove surpassed teams
            rankings = [team for team in rankings if team not in surpass_teams]
        print(f"[{challenge['point']} points] {challenge['category']}: {challenge['name']} ({challenge['solved']} solves){surpass_teams_string}")


if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / 'challs.json', 'r') as f:
        challenges = json.load(f)
    with open(pathlib.Path(__file__).parent / 'ranking.json', 'r') as f:
        rankings = json.load(f)["scores"]
    rankings.sort(key=lambda x: x['score'], reverse=True)
    # remove every team after "Kalmarunionen"
    for i, team in enumerate(rankings):
        if team['team_name'] == "Kalmarunionen":
            rankings = rankings[:i]
            break
    # remove team if team name is "Kalmarunionen"
    rankings = [team for team in rankings if team['team_name'] != "Kalmarunionen"]
    analyze(challenges, rankings)