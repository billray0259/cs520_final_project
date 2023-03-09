from flask import render_template
from rater import app

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', title='404 Not Found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', title='500 Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
