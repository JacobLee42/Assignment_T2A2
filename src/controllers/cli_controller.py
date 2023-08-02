from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.gym import Gym
from models.comment import Comment
from datetime import date


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print("Tables Dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email="admin@admin.com",
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    gyms = [
        Gym(
            title='Gym 1',
            name='Northside Aikido',
            address='Caboolture PCYC, 2 Toovey Street Caboolture QLD',
            phone='0434094244',
            style='Aikido',
            description='Northside Aikido Osu Dojo is located at the Caboolture Police citizens Youth Club at 2 Toovey St Caboolture. Aikido is a non-aggressive, non-competitive and is a purely defensive art. It places great emphasis on relaxation and calmness of mind and physical strength plays no part. Because of this, anyone can learn the art of Aikido.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 2',
            name='Caboolture Boxing Club',
            address='15 Riverview Street Caboolture QLD',
            phone='0407627869',
            style='Boxing',
            description='Caboolture Boxing Clubs trainer Don Tindall has been training champion boxers for over 30 years experience in the sport and trains both amateur and pro boxers. Beginners welcome!',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 3',
            name='Infinity Martial Arts',
            address='Morayfield Shopping Centre Morayfield QLD',
            phone='0426283877',
            style='Mixed Martial Arts, Brizilian Jui-jitsu, Boxing, Muay Thai',
            description='Infinity Morayfield is a full time academy conveniently located at Morayfield Shopping Centre, Morayfield QLD. We hold classes from Parents and bub classes from 2-4 years old up to adult classes. Classes run 6 days a week Monday to Saturday with a variety of class times to suit everyone. Come on down and train with us!',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 4',
            name='Progressive Wing Chun Kung Fu',
            address='Shop 8/113-137 Morayfield Road Morayfield QLD',
            phone='0411261272',
            style='Wing Chun Kung Fu',
            description='Wing Chun Kung Fu is the martial art developed for everyone! We offer family self defence classes for both kids and adults! Wing Chun is a close-quarters system of self-defense.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 5',
            name='Rhee Taekwondo',
            address='Morayfield East State School Hall, 107 Graham Road Morayfield QLD',
            phone='0487681849',
            style='Taekwondo',
            description='New, current and fromer members always welcome! All ages and fitness levels. Come along anytime! Founded in Australia in 1970 it is Australias first martial arst school, with branches Australia wide.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 6',
            name='Kaos Martial Arts',
            address='299 Morayfield Road Morayfield QLD',
            phone='0407579796',
            style='Boxing, Karate, Kickboxing, Muay Thai, MMA',
            description='Kaos Martial Arts is a full-contact gym located in Morayfield in Brisbanes North. We have been open for over 11 years offering a mixture of martial arts including Karate, Muay Thai, Boxing, Kickboxing and MMA. Whether you want to learn basic martial arts, train for a competition or just get back into shape, Kaos Martial Arts can help you achieve your goals.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 7',
            name='Red Dragon Martial Arts',
            address='Unit 5/379 Morayfield Road Morayfield QLD',
            phone='1800627842',
            style='Karate, Kickboxing, Kung Fu, Jiu Jitsu, MMA',
            description='No description given. Please contact on phone number provided for class times.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 8',
            name='Phoenix Rising Martial Arts',
            address='3/265 Morayfield Road Morayfield QLD',
            phone='0411234734',
            style='Karate, Kickboxing, MMA, Brazilian Jiu Jitsu, Kali sticks',
            description='Sensei Chris Marshall has over 19 years experience and has run Phoenix Rising Martial Arts since February 2014. We strive to provide a family-friendly and affordable martial arts and we welcome everyone into our martial arts school who wishes to train, get fit and have fun.',
            date=date.today(),
            user=users[0]
        ),
        Gym(
            title='Gym 9',
            name='Morayfield Martial Arts',
            address='7/30-36 Dickson Road Caboolture South QLD',
            phone='0412839569',
            style='Japanese Jujitsu, Traditional Weapons',
            description='Morayfield Martial Arts is a school that provides training in several styles of Japanese jujitsu. Chief Instructor Michael Pitt has been training in this style since the 1980s and is currently holds a 5th Degree Blackbelt in the art. Please contact the school for class training times.',
            date=date.today(),
            user=users[0]
        ),



















    ]

    db.session.add_all(gyms)

    comments = [
        Comment(
            message="Northside Aikido was fun! ",
            user=users[0],
            gym=gyms[0]
        ),
        Comment(
            message="Caboolture boxing club has been established for over 30 years at the PCYC in Caboolture. Cheap training costs and keeps you fit!",
            user=users[1],
            gym=gyms[1]

        ),
        Comment(
            message="Rhee Taekwondo was a lot of fun. They took great care and patience with me when I was a beginner. I would recommend to anyone wanting to give it a go!",
            user=users[1],
            gym=gyms[4]

        )

    ]

    db.session.add_all(comments)

    db.session.commit()



    print("Tables Seeded")
