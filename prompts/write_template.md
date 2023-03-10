Can you write a rater/templates/climber/register.html file?

It should extend this base.html file
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}RouteRater{% endblock %}</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
  {% block styles %}{% endblock %}
</head>
<body>
  <nav class="navbar navbar-expand-md navbar-light bg-light mb-4">
    <div class="container">
      <a class="navbar-brand" href="/">RouteRater</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        {% if current_user.is_authenticated %}
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="/routes">Routes</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/gym">Gyms</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/profile">Profile</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/logout">Logout</a>
          </li>
        </ul>
        {% else %}
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="/route">Routes</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/gym">Gyms</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/sign-up">Sign Up</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
          </li>
        </ul>
        {% endif %}
      </div>
    </div>
  </nav>

  <div class="container">
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class=flashes>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
  </div>

  <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa698ZN0HTieTq6TpAQq6wdtaO+M/trLvyEULt6vVTTEdhgJL6cypnvYj2N9AF" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper-base.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

And be compatible with this climber.register route
```python
@climber_bp.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        username = request.form['username']
        display_name = request.form['display_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form data
        if not email or not username or not display_name or not password or not confirm_password:
            error = 'All fields are required.'
            return render_template('climber/register.html', error=error)
        elif password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('climber/register.html', error=error)

        # Create new climber
        climber = Climber(email=email, username=username, display_name=display_name)
        climber.set_password(password)

        # Save climber to database
        try:
            climber.save()
        except ValueError as e:
            error = str(e)
            return render_template('climber/register.html', error=error)

        # Redirect to index page
        return redirect(url_for('index'))

    # Render sign-up page
    return render_template('climber/register.html')
```