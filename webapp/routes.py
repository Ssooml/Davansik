from flask import Blueprint, render_template

webapp_bp = Blueprint('webapp', __name__, template_folder='templates')

@webapp_bp.route('/webapp/<username>', methods=['GET'])
def webapp(username):
    return render_template('webapp.html', username=username)
