from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flasgger import Swagger
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notebook.db'
db = SQLAlchemy(app)
swagger = Swagger(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(120))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date)
    photo = db.Column(db.String(255))

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    company = fields.Str()
    phone = fields.Str(required=True)
    email = fields.Str(required=True)
    birthday = fields.Date()
    photo = fields.Str()

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

@app.route('/api/v1/notebook/', methods=['GET', 'POST'])
def contacts():
    """
    Получить список всех контактов или добавить новый контакт
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: Contact
          required:
            - full_name
            - phone
            - email
          properties:
            full_name:
              type: string
              description: ФИО
            company:
              type: string
              description: Компания
            phone:
              type: string
              description: Телефон
            email:
              type: string
              description: Email
            birthday:
              type: string
              description: Дата рождения
            photo:
              type: string
              description: Фото
    responses:
      200:
        description: Возвращает список всех контактов или добавленный контакт
    """
    if request.method == 'GET':
        contacts = Contact.query.all()
        return jsonify(contacts_schema.dump(contacts))
    
    if request.method == 'POST':
        try:
            contact = contact_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        new_contact = Contact(**contact)
        db.session.add(new_contact)
        db.session.commit()
        return contact_schema.jsonify(new_contact), 201

@app.route('/api/v1/notebook/<int:id>/', methods=['GET', 'POST', 'DELETE'])
def single_contact(id):
    """
    Получить, обновить или удалить контакт по ID
    ---
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Возвращает информацию о контакте или обновленный контакт
      204:
        description: Контакт успешно удален
    """
    contact = Contact.query.get_or_404(id)
    
    if request.method == 'GET':
        return contact_schema.jsonify(contact)

    if request.method == 'POST':
        try:
            updated_contact = contact_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        for key, value in updated_contact.items():
            setattr(contact, key, value)
        db.session.commit()
        return contact_schema.jsonify(contact)

    if request.method == 'DELETE':
        db.session.delete(contact)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
