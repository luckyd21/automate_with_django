from django.core.management.base import BaseCommand
from dataentry.models import Student



# i want to add some data to database  using the custom command

class Command(BaseCommand):
    help = "It will be insert data to database"

    def handle(self, *args, **kwargs):
        #logic are here
        dataset = [
            {'roll_no': 1001,'name':'Sachin','age':20},
            {'roll_no': 1002,'name':'Rahul','age':21},
            {'roll_no': 1007,'name':'Shyam','age':20},
            {'roll_no': 1006,'name':'Lucky','age':20},

        ]
        for data in dataset:
            roll_no = data['roll_no']
            existing_record= Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                 Student.objects.create(roll_no=data['roll_no'],name = data['name'], age = data['age'])
            else:
                self.stdout.write(self.style.WARNING (f'Student with roll_no{roll_no} already exist'))

            
        self.stdout.write(self.style.SUCCESS('data inserted successfully'))

