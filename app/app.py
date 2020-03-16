from flask import Flask, escape, request, render_template
import requests
import logging
from logging.config import dictConfig
import os

# todo figure out this
# https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files

# https://flask.palletsprojects.com/en/1.0.x/logging/
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
# https://palletsprojects.com/p/flask/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

@app.route('/diffweb', methods=['GET', 'POST'])
def root():
    """Diff 2 text."""
    return show_diff()

def show_diff():
    form_base_text = request.form.get("base_text", "")
    form_new_text = request.form.get("new_text", "")
    form_new_text_url = request.form.get("new_text_url", "")
    form_base_text_url = request.form.get("base_text_url", "")
    f=open("/run/secrets/git_password","r")
    lines=f.readlines()
    form_username=lines[0].replace('\n','').replace('\r','')
    form_password=lines[1].replace('\n','').replace('\r','')
    f.close()

    #app.logger.info("form_new_text_url = %s",form_new_text_url)
    #app.logger.info("form_base_text_url = %s",form_base_text_url)

    if not form_base_text.strip() and form_base_text_url.strip():
      form_base_text = requests.get(form_base_text_url,auth=(form_username, form_password),verify=False).text
    if not form_new_text.strip() and form_new_text_url.strip():
      form_new_text = requests.get(form_new_text_url,auth=(form_username, form_password),verify=False).text
    return render_template('diff.html',base_text=form_base_text,new_text=form_new_text,base_text_url=form_base_text_url,new_text_url=form_new_text_url)

# run the application
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)