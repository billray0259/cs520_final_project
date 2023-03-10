# RouteRater

Currently, route setters specify the difficulty ratings of indoor rock climbing routes. These difficulty ratings can be arbitrary, leading to inconsistent ratings. We propose a web app that utilizes QR codes or unique route IDs visible at the bottom of each route. Climbers can scan the QR code or enter the route ID with their mobile device and be directed to a page where they can rate the route's difficulty and indicate if they could complete the route and, if so, how many times they attempted the route before completing it. The app will keep track of each climber's ratings and create a profile that reflects their climbing ability. This information will allow the app to provide a more accurate, data-driven difficulty rating for each route. Additionally, the system *may* offer other helpful information to climbers, such as:
* Viewing how they have progressed over time as a climber.
* Finding routes in their current gym that are an appropriate difficulty level for them.
* Sharing and viewing comments posted by other climbers on specific routes.

The high-level goal of this project is to develop a software system that determines, given user ratings and input, the true difficulty of indoor rock climbing routes.

## Components
Our software system will most likely have seven main components

1. Data model that represents the route profiles
2. Data model that represents the climber profiles
3. A component that populates the route profiles
    1. Add new routes to the system
    2. Add ratings/attempt information to existing routes
4. A component that populates the climber profiles
    1. Register an account
    2. Add account information
5. Data-driven route difficulty calculation algorithm
    1. Simple option: Average user difficulty ratings
    2. Advanced option: Based on completion information, the algorithm can compare the difficulty of different routes. From this, a rough ordering of routes can be obtained, which can then be mapped onto a difficulty scale based on the direct difficulty ratings provided by users
6. A component that renders the route profiles
7. A component that renders the climber profiles