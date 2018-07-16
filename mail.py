#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api()

with open('cfg.json', 'r') as f:
    cfg = json.load(f)


def make_response(message, status, code):
    return {"message": message, "status": status, "code": code}


class Mail(Resource):
    post_parse = reqparse.RequestParser()
    post_parse.add_argument('tos')
    post_parse.add_argument('subject')
    post_parse.add_argument('content')

    def post(self, token=None):

        if cfg['http']['token'] == "":
            t = None
        else:
            t = cfg['http']['token']

        if token != t:
            return jsonify(make_response(message="no privilege", status="Failed", code=401))

        status = self.__email()

        if status:
            return jsonify(make_response(message="Send Complete", status="Success", code=200))
        else:
            return jsonify(make_response(message="Send Failed", status="Failed", code=500))

    def __email(self):
        args = self.post_parse.parse_args()
        tos = args.tos.replace(',', ';')

        if cfg['smtp']['port'] == 465:
            smtp = smtplib.SMTP_SSL(host=cfg['smtp']['addr'], port=cfg['smtp']['port'])
        else:
            smtp = smtplib.SMTP(host=cfg['smtp']['addr'], port=cfg['smtp']['port'])

        try:
            msg = MIMEMultipart()
            msg['From'] = cfg['smtp']['from']
            msg['To'] = tos
            msg['Subject'] = args.subject
            msg.attach(MIMEText(args.content))

            smtp.login(cfg['smtp']['username'], cfg['smtp']['password'])
            smtp.sendmail(cfg['smtp']['from'], tos, msg.as_string())
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            smtp.quit()


api.add_resource(Mail, '/sender/mail/<token>', '/sender/mail', endpoint='mail')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=cfg['debug'], host=cfg['http']['host'], port=cfg['http']['port'])
