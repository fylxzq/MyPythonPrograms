from flask import render_template

from . import auth
@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@auth.errorhandler(500)
def internal_sever_error(e):
    return  render_template('500.html'),500