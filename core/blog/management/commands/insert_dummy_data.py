from django.core.management.base import BaseCommand
from django.utils.datetime_safe import datetime

from faker import Faker

from accounts.models import User, Profile
from blog.models import Post, Category


category_list = [
    'Pork',
    'Beef',
    'Sausage',
    'Ham'
]

class Command(BaseCommand):
    help = 'Inserting dummy data for blog posts.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(), password='far121269'
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for category_name in category_list:
            Category.objects.get_or_create(
                name=category_name
            )

        for _ in range(5):
            Post.objects.create(
                title=self.fake.sentence(nb_words=5),
                author=profile,
                content=self.fake.paragraph(nb_sentences=10),
                category=Category.objects.get(
                    name=self.fake.random_element(elements=category_list)
                ),
                status=self.fake.boolean(chance_of_getting_true=75),
                published_date=self.fake.date_time_between(
                    datetime(
                        year=2023, month=1, day=17, hour=19, minute=32, second=39
                    ),
                    datetime.now()
                )
            )