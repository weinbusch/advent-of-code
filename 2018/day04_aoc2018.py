import re
from collections import defaultdict, Counter

guard_re = re.compile(r"Guard \#(\d+) begins shift")
minute_re = re.compile(r"\[\d+-\d+-\d+ \d+:(\d+)\]")

def solve(data):
  guard = None
  guards = defaultdict(list)
  for line in sorted(data.splitlines()):
    if mo := guard_re.search(line):
      if guard is not None:
        guards[guard].append(status)
      guard = int(mo.group(1))
      status = [False for _ in range(60)]
    else:
      minute = int(minute_re.match(line).group(1))
      asleep = "falls asleep" in line
      for i in range(minute, 60):
        status[i] = asleep

  sleep_statistics = {g: Counter(m for d in ds for m, a in enumerate(d) if a) for g, ds in guards.items()}

  most_common_minutes = {
    g: c.most_common()[0] for g, c in sleep_statistics.items() if c
  }

  sleeping_guards = list(most_common_minutes.keys())
  
  sleepy_guard = next(
    reversed(sorted(sleeping_guards, key=lambda g: sum(sleep_statistics[g].values())))
  )

  sleepy_minute = most_common_minutes[sleepy_guard][0]

  predictable_guard = next(
    reversed(sorted(sleeping_guards, key=lambda g: most_common_minutes[g][1]))
  )

  most_common_minute = most_common_minutes[predictable_guard][0]
  
  return sleepy_minute * sleepy_guard, predictable_guard * most_common_minute