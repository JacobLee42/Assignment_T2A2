from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.gym import Gym

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
            user=users[0]
        ),
        Gym(
            title='Gym 2',
            name='Caboolture Boxing Club',
            address='15 Riverview Street Caboolture QLD',
            phone='0407627869',
            style='Boxing',
            description='Caboolture Boxing Clubs trainer Don Tindall has been training champion boxers for over 30 years experience in the sport and trains both amateur and pro boxers. Beginners welcome!',
            user=users[0]
        ),
        Gym(
            title='Gym 3',
            name='Infinity Martial Arts',
            address='Morayfield Shopping Centre Morayfield QLD',
            phone='0426283877',
            style='Mixed Martial Arts, Brizilian Jujitsu, Boxing, Muay Thai',
            description='Infinity Morayfield is a full time academy conveniently located at Morayfield Shopping Centre, Morayfield QLD. We hold classes from Parents and bub classes from 2-4 years old up to adult classes. Classes run 6 days a week Monday to Saturday with a variety of class times to suit everyone. Come on down and train with us!',
            user=users[0]
        ),
        Gym(
            title='Gym 4',
            name='Progressive Wing Chun Kung Fu',
            address='Shop 8/113-137 Morayfield Road Morayfield QLD',
            phone='0411261272',
            style='Wing Chun Kung Fu',
            description='Wing Chun Kung Fu is the martial art developed for everyone! We offer family self defence classes for both kids and adults! Wing Chun is a close-quarters system of self-defense.',
            user=users[0]
        ),
        Gym(
            title='Gym 5',
            name='Rhee Taekwondo',
            address='Morayfield East State School Hall, 107 Graham Road Morayfield QLD',
            phone='0487681849',
            style='Taekwondo',
            description='New, current and fromer members always welcome! All ages and fitness levels. Come along anytime! Founded in Australia in 1970 it is Australias first martial arst school, with branches Australia wide.',
            user=users[0]
        ),
    ]

    db.session.add_all(gyms)

    db.session.commit()



    print("Tables Seeded")
