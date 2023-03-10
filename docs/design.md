| Object / Page     | Register | Profile | Edit Profile | Create Route | Route | Edit Route | Create Gym | Gym | Edit Gym |
|-------------------|----------|---------|--------------|--------------|-------|------------|------------|-----|----------|
| **Climber**       | C        | R       | UD           |              |       |            |            |     |          |
| **Route**         |          |         |              | C            | R     | UD         |            |     |          |
| **Gym**           |          |         |              |              |       |            | C          | R   | UD       |
| **Attempt**       |          | RUD     |              |              | C     |            |            |     |          |
| **GradeEstimate** |          |         |              |              | CRUD  |            |            |     |          |
| **Comment**       |          |         |              |              | CRUD  |            |            |     |          |



# Objects

## Climber
### Properties
* Display Name: str
* Gyms: list[Gym_id]
* Email: str
* Username: str
* Password: str
* Friends: list[Climber_id]

### CRUD Pages
* Create: Register page
* Read: Profile page
* Update: Edit profile page
* Delete: Edit profile page

## Route
### Properties
* _id: Route_id
* Color: str
* Gym: Gym_id


### CRUD Pages
* Create: Create route page
* Read: Route page
* Update: Edit Route page
* Delete: Edit route page

## Gym
### Properties
* Name: str
* Address: str
* Website: str
* Owner: Climber_id
* Admins: list[Climber_id]

### CRUD Pages
* Create: Create gym page
* Read: Gym page
* Update: Edit gym page
* Delete: Edit gym page

## Attempt
### Properties
* Success: bool
* Route: Route_id
* Climber: Climber_id
* Time: datetime

### CRUD Pages
* Create: Route page
* Read: Profile page
* Update: Profile page
* Delete: Profile page

## GradeEstimate
### Properties
* Grade: int
* Route: Route_id
* Climber: Climber_id
* Time: datetime

### CRUD Pages
* Create: Route page
* Read: Route page
* Update: Route page
* Delete: Route page

## Comment
### Properties
* Content: str
* Route: Route_id
* Climber: Climber_id
* Time: datetime

### CRUD Pages
* Create: Route page
* Read: Route page
* Update: Route page
* Delete: Route page



# Pages

## Register Page
* Create Climber
    * Enter email
    * Enter username
    * Enter display name
    * Enter password
    * Enter confirm password
    * Submit
    


## Profile Page
* Read Climber
    * Display name
    * Email
    * List of gyms
    * List of friends
* Read Attempt
    * Progression graph
    * List of attempts
* Update Attempt
    * Edit button
    * Toggle success
* Delete Attempt
    * Delete attempt button

## Edit Profile Page
* Update Climber
    * Update display name
    * Update username
    * Update email
    * Change password
    * Confirm password
    * Submit
    * Search for friends
    * Add friend
    * Remove friend
* Delete Climber
    * Delete account button

## Create Route Page
* Create Route
    * Select Gym
    * Enter ID
    * Enter Color
    * Submit

## Edit Route Page
* Update Route
    * Update Color
    * Submit
* Delete Route
    * Delete route button

## Route Page
* Read Route
    * Display ID
    * Display Color
    * Display Gym
* Create Attempt
    * I sent it button
    * I didn't send it button
* Read Attempt
    * Display inidicator of success if any attempt has succeeded
    * Display attempt list
* Create GradeEstimate
    * Enter grade
    * Submit
* Read GradeEstimate
    * Display grade
* Update GradeEstimate
    * Revize grade button
    * Submit
* Delete GradeEstimate
    * Delete grade estimate button
* Create Comment
    * Enter comment
    * Submit
* Read Comment
    * Display comment list
* Update Comment
    * Edit comment button
    * Submit
* Delete Comment
    * Delete comment button

## Create Gym Page
* Create Gym
    * Send email to developer with
        * Gym name
        * Gym address
        * Gym website
        * Gym owner username
    * backend endpoint to create gym

## Gym page
* Read Gym
    * Display name
    * Display address
    * Display website

## Edit Gym Page
* Update Gym
    * Update name
    * Update address
    * Update website
    * Submit
    * Add admin
    * Remove admin
    * Change owner
* Delete Gym
    * Delete gym button


# File Structure

```
rater/
    __init__.py
    models/
        __init__.py
        climber.py
        route.py
        gym.py
        attempt.py
        grade_estimate.py
        comment.py
    views/
        __init__.py
        climber.py
        route.py
        gym.py
        attempt.py
        grade_estimate.py
        comment.py
    templates/
        base.html
        climber/
            register.html
            profile.html
            edit_profile.html
        route/
            create.html
            read.html
            edit.html
        gym/
            create.html
            read.html
            edit.html
        error.html
    static/
        css/
        js/
    app.py
```


# Database Structure

```javascript

climber: {
    _id: ObjectId
    email: str,
    username: str,
    password_hash: str,
    gyms: [ObjectId],
    friends: [ObjectId]
}

route: {
    _id: ObjectId,
    color: str,
    gym: ObjectId
}

gym: {
    _id: ObjectId,
    name: str,
    address: str,
    website: str,
    owner: ObjectId,
    admins: [ObjectId]
}

attempt: {
    _id: ObjectId,
    success: bool,
    route: ObjectId,
    climber: ObjectId,
    time: datetime
}

grade_estimate: {
    _id: ObjectId,
    grade: int,
    route: ObjectId,
    climber: ObjectId,
    time: datetime
}

comment: {
    _id: ObjectId,
    content: str,
    route: ObjectId,
    climber: ObjectId,
    time: datetime
}

```