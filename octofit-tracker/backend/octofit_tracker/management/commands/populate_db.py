from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djongo import models
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        marvel_team = {'name': 'Team Marvel', 'members': ['Iron Man', 'Captain America', 'Thor', 'Hulk']}
        dc_team = {'name': 'Team DC', 'members': ['Superman', 'Batman', 'Wonder Woman', 'Flash']}
        teams = [marvel_team, dc_team]
        db.teams.insert_many(teams)

        users = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Steve Rogers', 'email': 'cap@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'team': 'Team DC'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'team': 'Team DC'},
        ]
        db.users.insert_many(users)

        activities = [
            {'user': 'Tony Stark', 'activity': 'Running', 'duration': 30},
            {'user': 'Steve Rogers', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Clark Kent', 'activity': 'Swimming', 'duration': 60},
            {'user': 'Bruce Wayne', 'activity': 'Boxing', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {'team': 'Team Marvel', 'points': 120},
            {'team': 'Team DC', 'points': 110},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {'user': 'Tony Stark', 'workout': 'Chest Press', 'reps': 20},
            {'user': 'Steve Rogers', 'workout': 'Push Ups', 'reps': 50},
            {'user': 'Clark Kent', 'workout': 'Deadlift', 'reps': 30},
            {'user': 'Bruce Wayne', 'workout': 'Pull Ups', 'reps': 25},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
