# Description
This web app is designed to improve the accuracy of difficulty ratings for indoor climbing routes. Currently, the difficulty ratings are set by the route setters and can be arbitrary, leading to inconsistent and inaccurate ratings.

The proposed solution is a web app that utilizes QR codes placed at the bottom of each route. Climbers can scan the QR code with their mobile device and be directed to a page where they can rate the route's difficulty and indicate if they were able to complete the route and how many attempts it took. The app will keep track of each climber's ratings and create a profile that reflects their climbing ability. This information will allow the app to provide a more accurate and data-driven difficulty rating for each route.

In addition to improving the accuracy of difficulty ratings, the app will enable climbers to track their skill progress over time and view their personal growth.

To use the app, simply scan the QR code at the bottom of the climbing route and rate the difficulty. Your profile will keep track of your progress and the app will update the route's difficulty rating based on the collective ratings of all climbers.

# Stakeholders

1. Rock climbers: They would be the primary users of the app, and it's essential to ensure that the app provides a valuable and enjoyable experience for them.

2. Route setters: They would be interested in knowing how their routes are being received by the climbing community, and the app could provide valuable feedback.

3. Climbing gyms: They would be interested in having a tool that provides a data-driven difficulty rating for their routes, which could be useful for marketing and promoting their gym.

4. Climbing enthusiasts: They would be interested in the app as a way to connect with other climbers and track their personal progress.

5. Data privacy advocates: It's important to ensure that the app handles user data responsibly and protects the privacy of its users.

6. App developers: They would be interested in ensuring that the app is built with a user-friendly interface, high-quality code, and robust security measures.


# User Stories
1. As a beginner climber, I want to be able to track my progress and see how I'm improving over time.

2. As a seasoned climber, I want to be able to rate the difficulty of routes I've climbed and see how my ratings compare to others.

3. As a route setter, I want to be able to view feedback from climbers on the difficulty of my routes and use that information to make adjustments.

4. As a climbing gym owner, I want to be able to see a data-driven difficulty rating for each of my routes to help attract new customers and retain existing ones.

5. As a climbing enthusiast, I want to be able to connect with other climbers and see what routes they've completed and what their difficulty ratings are.

6. As a data privacy advocate, I want to ensure that my personal information is secure and that the app is transparent about how it uses my data.

7. As an app developer, I want to ensure that the app is built with a user-friendly interface, high-quality code, and robust security measures.


# Features and Requirements

1. User profiles: The app must allow climbers to create a profile that tracks their progress and stores their difficulty ratings for routes they've climbed.

2. Route tracking: The app must allow climbers to log the routes they've climbed and provide a difficulty rating for each route.

3. Difficulty ratings: The app must provide a data-driven difficulty rating for each route based on the ratings provided by climbers.

4. Route setter feedback: The app must allow route setters to view feedback from climbers on the difficulty of their routes and use that information to make adjustments.

5. Social connectivity: The app must allow climbers to connect with other climbers and see what routes they've completed and what their difficulty ratings are.

6. Data privacy: The app must have robust privacy measures in place to protect the personal information of its users.

7. User-friendly interface: The app must have a user-friendly interface that is easy to navigate and use.

8. High-quality code: The app must be built with high-quality code that is maintainable, scalable, and secure.


# Action Plan

1. [X] Plan the architecture: Start by sketching out the overall architecture of the app, including the components of the front-end, the backend, and the database.

2. [X] Set up the environment: Set up the development environment by installing the necessary software, including a code editor, a local web server, and a MongoDB database.

3. [ ] Design the front-end: Design the front-end of the app using HTML, JavaScript, and CSS. This should include the user interface, navigation, and any other necessary components.

4. [ ] Build the backend: Build the backend using Flask. This should include the routes and logic necessary to support the front-end and interact with the database.

5. [ ] Integrate the database: Integrate MongoDB into the app to store the climbers' data and route information.

6. [ ] Test and debug: Test the app thoroughly, fixing any bugs and issues that arise during development.

7. [ ] Deploy the app: Deploy the app to a web server, making it accessible to users.

8. [ ] Continuously improve: Continuously improve the app by adding new features and fixing any issues that arise after deployment.

9. [ ] Maintain security: Ensure that the app is secure and that user data is protected.

10. [ ] Monitor performance: Monitor the performance of the app and make any necessary optimizations to ensure that it runs smoothly and efficiently.


# Pages

1. Login/Registration page: A page where users can create an account or log in to an existing account.
   1. Login form: A form that allows users to log in to their account using their email address and password.
   2. Registration form: A form that allows users to create a new account by entering their email address, password, and profile information.
   3. Forgotten password link: A link that allows users to reset their password if they forget it.
   4. Social login buttons: Buttons that allow users to log in using their social media accounts, such as Facebook or Google.
   5. Terms of use checkbox: A checkbox that requires users to agree to the terms of use before creating an account.
   6. Privacy policy link: A link to the app's privacy policy page.
   7. Error messages: Error messages that appear if there is an issue with the user's login or registration information, such as an incorrect email address or password.
   8. Loading indicator: A loading indicator that appears while the app is processing the user's login or registration information.
   9. Branding/logo: A visual representation of the app's brand or logo.

2. Route page: A page that displays information about the route and allows users to rate the difficulty.
   1. Route Information: A display of the basic information about the route, such as its name, location, and setter
   2. Difficulty Rating Form: A form that allows users to rate the difficulty of the route on a scale (e.g., V0-V16).
   3. Difficulty Rating Display: A display that shows the average difficulty rating for the route based on the ratings provided by other climbers.
   4. Send/Attempt Tracker: A form that allows users to indicate whether they were able to complete the route and, if so, if they sent it on their first try, during their first session, or if it took them multiple sessions to complete.
   5. Comments Section: A section that allows users to leave comments about the route and view comments left by other climbers.
   6. QR Code Scanner: A QR code scanner that allows users to quickly access the Route page by scanning a QR code at the bottom of the route.
   7. Navigation: A navigation bar that allows users to easily access other pages within the app.

3. Social connectivity page: A page where climbers can connect with other climbers and see what routes they've completed and what their difficulty ratings are.
   1. Route explorer: A widget that allows climbers to view all the routes in the gym and see the difficulty ratings provided by others.
   2. Connect with other climbers: A widget that enables climbers to connect with other climbers and communicate with them through the app.
   3. Climber directory: A widget that displays a directory of climbers the user has connected with, including their profiles and the routes they've completed and their difficulty ratings.
   4. Search function: A widget that allows climbers to search for specific routes or climbers and view their information.

4. Profile page: A page where users can view their progress and edit their profile information.
   1. User information: This would include the user's name, email, and any other information they have provided in their profile.
   2. Route history: A list of the routes the user has completed and their difficulty ratings, along with the dates they completed the routes.
   3. Progress chart: A visual representation of the user's progress over time, showing how their skill level has changed.
   4. Edit profile button: A button that allows the user to edit their profile information, including their name, email, and other details.
   5. Logout button: A button that allows the user to log out of their account.
   6. Change password button: A button that allows the user to change their password.
   7. Delete account button: A button that allows the user to delete their account, along with all their data.

5. Privacy policy page: A page that outlines the app's privacy policy and how user data is handled.

6. Terms of use page: A page that outlines the terms of use for the app and the responsibilities of its users.