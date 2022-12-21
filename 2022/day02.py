def solve(data):
  rounds = [line.split() for line in data.splitlines()]

  # Part 1
  scores = [get_score(decode(*round, part=1)) for round in rounds]
  p1 = sum(scores)
  assert p1 == 14069

  # Part 2
  scores = [get_score(decode(*round, part=2)) for round in rounds]
  p2 = sum(scores)
  assert p2 == 12411

  return p1, p2

choices = "ABC"

def decode(opponent, player, part=1):
  index = "XYZ".find(player)
  if part == 2:
    index = choices.find(opponent)
    if player == "X": 
      index = (index - 1) % 3
    elif player == "Z":
      index = (index + 1) % 3
  decoded = choices[index]
  return opponent + decoded
        
player_wins = [
  # the 2nd symbol indicates the player
  "AB", # rock vs paper
  "BC", # paper vs scissors
  "CA", # scissors vs rock
]

def get_score(round):
  score = 1 + choices.find(round[1])
  if round[0] == round[1]:
    score += 3
  elif round in player_wins:
    score += 6
  return score