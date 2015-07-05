from datetime import *

current_episode = int(input("Current Episode: "))
target_episode = int(input("Target Episode: "))
episodes_per_day = int(input("Episodes Per Day: "))

remaining_episodes = target_episode - current_episode
remaining_days = remaining_episodes / episodes_per_day

today = date.today()
finish_date = today + timedelta(remaining_days)

print(remaining_days, "days:",
      finish_date.strftime("%B %d, %Y"))
