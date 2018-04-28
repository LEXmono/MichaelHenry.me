from flask import Flask, render_template, request, abort, jsonify
from flask_recaptcha import ReCaptcha
from config.site_config import configure_app
from custom_exceptions import InvalidUsage
from datetime import datetime
from dateutil import rrule
from github import get_repos
from send_email import send_email

import logging


logger = logging.getLogger()
app = Flask(__name__)
configure_app(app)

recaptcha = ReCaptcha()
recaptcha.init_app(app)


@app.route('/')
def index():
    repos = get_repos()[:3]
    resume_url = app.config['RESUME_URL']
    weeks = rrule.rrule(rrule.WEEKLY,
                        dtstart=datetime(2011, 10, 2),
                        until=datetime.now())
    counts = {'coffee': 6 * (datetime.now() - datetime(2006, 4, 1)).days,
              'hours': weeks.count() * 40,
              'ideas': weeks.count() * 2}
    return render_template('index.html', repos=repos, resume_url=resume_url,
                           counts=counts)


@app.route('/send_email', methods=['POST'])
def email():
    recaptcha_response = recaptcha.verify()
    if recaptcha_response:
        logger.debug("Request: {}".format(request.form))
        name = request.form.get('name')
        email_address = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        message = request.form.get('message')
        status = send_email(name=name, email=email_address, phone=phone,
                            company=company, message=message)
        if status:
            response = 'OK'
        else:
            response = False
    else:
        logger.error("Bot Tried to submit: {}".format(request))
        raise InvalidUsage('No Bots Allowed!', status_code=450)
    return response

@app.route('/500')
def show_500():
    return render_template('500.html')

@app.errorhandler(404)
def page_not_found(e):
    logger.info("[404 ERROR] - {} - e".format(request, e))
    return render_template('404.html'), 404

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
