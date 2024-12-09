from flask import render_template_string

def configure_routes(app):
    @app.route('/webapp/<username>', methods=['GET'])
    def webapp(username):
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Web App</title>
        </head>
        <body>
            <h1>Привет, {{ username }}</h1>
        </body>
        </html>
        """, username=username)
