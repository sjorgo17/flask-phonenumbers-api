from flask import Blueprint, jsonify,request
from . import db
from .models import User, PhoneNumber

main=Blueprint('main',__name__)


@main.route('/general_add', methods=['POST'])
def general_add():
    #Get user data
    user_data=request.get_json()

    #Create and add new user
    new_user=User(name=user_data['name'],surname=user_data['surname'])
    db.session.add(new_user)
    db.session.commit()

    numbers=user_data['numbers']
    number_objects=[]

    #Create the PhoneNumber objects associated with the user
    for number_data in numbers:
        new_number=PhoneNumber(uid=new_user.id,phoneNumber=number_data['phoneNumber'],type=number_data['type'])
        number_objects.append(new_number)

    #Add the phone numbers in the db
    db.session.add_all(number_objects)
    db.session.commit()

    return jsonify(success=True)


@main.route('/users/<int:page_num>', methods=['GET'])
def users(page_num):
    
    #Get parameters if provided
    order=request.args.get('order',None)
    mod=request.args.get('mod',None)
    perPage=int(request.args.get('perPage',10))

    #Sort and paginate data according to parameters.
    if order=="name":
        user_list= User.query.order_by(User.name.desc() if mod=="desc" else User.name.asc()).paginate(per_page=perPage,page=page_num,error_out=True)
    
    elif order=="surname":     
        user_list= User.query.order_by(User.surname.desc() if mod=="desc" else User.surname.asc()).paginate(per_page=perPage,page=page_num,error_out=True)
     
    else:
        user_list= User.query.paginate(per_page=perPage,page=page_num,error_out=True)

    #Create list of users to store all the data
    users=[]

    for user in user_list.items:
        record={}
        record['id']=user.id
        record['name']=user.name
        record['surname']=user.surname
        record['numbers']=[]
        for number in user.numbers:
            record['numbers'].append({'id':number.id ,'phoneNumber':number.phoneNumber,'type':number.type})
        users.append(record)

    return jsonify({'users':users})


@main.route('/numberOfUsers')
def numberOfUsers():
    
    #Get total number of users.
    allUsers= User.query.count()
    return jsonify({'allUsers':allUsers})


