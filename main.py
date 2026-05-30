import requests

response = requests.get("https://statsapi.mlb.com/api/v1.1/game/824355/feed/live?hydrate=strikeZone")
data = response.json()


allPlays = data["liveData"]["plays"]["allPlays"]

pitchData = []
umpCall = []

for play in allPlays:
    for event in play["playEvents"]:
        if event.get("isPitch"):
            strikeZoneTop = event["pitchData"]["strikeZoneTop"]
            strikeZoneBottom = event["pitchData"]["strikeZoneBottom"]
            strikeZoneWidth = event["pitchData"]["strikeZoneWidth"]

            ump = event["pitchData"]["strikeZoneInfo"].get("isStrike")
            umpCall.append(ump)

            edge_position_ball = event["pitchData"]["strikeZoneInfo"]["edgePositionBall"]


            ballX = edge_position_ball.get("x")
            ballZ = edge_position_ball.get("z")

            pitch_entry = {
                "zone_top": strikeZoneTop,
                "zone_bottom": strikeZoneBottom,
                "zone_width": strikeZoneWidth,
                "ball_position": {
                    "x": ballX,
                    "z": ballZ
                },
                "strike": False
            }
            pitchData.append(pitch_entry)

def isStrike(pitch):
    ballX = pitch["ball_position"].get("x")
    ballZ = pitch["ball_position"].get("z")

    left = -((pitch["zone_width"]/2) / 12)
    right = ((pitch["zone_width"]/2) / 12)

    if (ballZ >= pitch["zone_bottom"] and ballZ <= pitch["zone_top"]) and (ballX >= left and ballX <= right):
        pitch["strike"] = True

right = 0
wrong = 0

for pitch, call in zip(pitchData, umpCall):
    isStrike(pitch)
    if pitch.get("strike") == call:
        right += 1
    else:
        wrong += 1
    

print("correct: ", right)
print("incorrect: ", wrong)
print("percentage: ", 100 * (right/(right + wrong)))
