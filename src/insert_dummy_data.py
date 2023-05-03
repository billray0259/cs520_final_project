# Generate some random gyms and routes to populate the databse


# Example gym:
{
  "_id": {
    "$oid": "640b7ae3bd361de601fd4c30" # new gym id
  },
  "name": "Central Rock Gym, Hadley",
  "address": "165 Russell St, Hadley, MA 01035",
  "website": "https://centralrockgym.com/hadley/",
  "owner": {
    "$oid": "640b7a4d28e749de50500f6c" # keep the same owner
  },
  "admins": []
}

# Example route:
{
  "_id": {
    "$oid": "6449a15e4eeeb4ea0a217283" # new route id
  },
  "name": "First Route",
  "color": "Red",
  "gym": {
    "$oid": "640b7ae3bd361de601fd4c30" # gym id of existing gym
  }
}

import random
from rater.models import Gym, Route, Climber


owner = Climber.find_by_username('bill')


n_gyms = 10
n_routes_per_gym = 10

for i in range(n_gyms):
    gym = Gym(name=f'Gym {i}', address=f'Address {i}', website=f'gym{i}.com', owner_id=owner.id)
    gym.save()
    for j in range(n_routes_per_gym):
        colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Pink', 'Purple', 'Orange']
        rand_color = random.choice(colors)
        route = Route(name=f'Route {i}-{j}', color=rand_color, gym_id=gym.id)
        route.save()
