import os
import random

# djagno
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

from faker import Faker

from common.models import Tag
from posts.models import Post
from questions.models import Question, Set



def cap_range(n, m, k):
    return min(n, k), min(m, k)


# mixins
class TagsMixin:
    @staticmethod
    def add_tags(n, m, objects, tags):
        n, m = cap_range(n, m, len(tags))
        for obj in objects:
            k = random.randint(n, m)
            obj.tags.add(*random.sample(set(tags), k))


class LikesMixin:
    @staticmethod
    def add_likes(n, m, objects, users):
        n, m = cap_range(n, m, len(users))
        for obj in objects:
            k = random.randint(n, m)
            obj.likes.add(*random.sample(set(users), k))


class TextMixin:
    def titles(self, k):
        return set([self.fake.text(max_nb_chars=30) for _ in range(k)])


# managers
class ModelManager:
    def __init__(self, fake=Faker()):
        self.fake = fake


class UserManager(ModelManager):
    @staticmethod
    def usernames():
        return set(['QuizMaster', 'John', 'Anne', 'BatMan', 'Joker', 'jackal02'])

    def email(self):
        return self.fake.safe_email()

    @staticmethod
    def set_password(user):
        user.set_password('Password1234')  # for comedic effect

    def user_iter(self, usernames):
        for username in usernames:
            user = User(
                username=username,
                email=self.email(),
                is_staff=True,
            )
            self.set_password(user)
            yield user

    def create_bulk(self):
        User.objects.bulk_create(iter(self.user_iter(self.usernames())))


class TagManager(ModelManager):
    def names(self, k):
        return set(filter(lambda x: len(x) > 2, self.fake.words(k)))

    def create_bulk(self, k):
        Tag.objects.bulk_create([
            Tag(name=name) for name in self.names(k)
        ])


class QuestionManager(ModelManager, TagsMixin, LikesMixin):
    @staticmethod
    def difficulty():
        return random.randint(1, 5)

    def text(self):
        text = self.fake.text(max_nb_chars=255)
        return text[:-1] + '?'
    
    def answer(self):
        return self.fake.word()

    def alternate_answer(self):
        return self.fake.word() if random.random() > 0.8 else ''

    @staticmethod
    def answer_widget():
        return Question.TEXT

    def create_bulk(self, users, k):
        Question.objects.bulk_create([
            Question(
                created_by=random.choice(users),
                difficulty=self.difficulty(),
                text=self.text(),
                answer=self.answer(),
                alternate_answer=self.alternate_answer(),
                answer_widget=self.answer_widget(),
            )
            for _ in range(k)
        ])


class SetManager(ModelManager, TagsMixin, LikesMixin, TextMixin):
    def description(self):
        return self.fake.text(max_nb_chars=255)

    @staticmethod
    def add_questions(n, m, sets, questions):
        n, m = cap_range(n, m, len(questions))
        for set_ in sets:
            k = random.randint(n, m)
            set_.questions.add(*random.sample(set(questions), k))

    def create_bulk(self, users, k):
        Set.objects.bulk_create([
            Set(
                created_by=random.choice(users),
                title=title,
                description=self.description(),
            )
            for title in self.titles(k)
        ])


class PostManager(ModelManager, TextMixin):
    def lead(self):
        return self.fake.text(max_nb_chars=255)

    def body(self):
        return self.fake.text(max_nb_chars=1023)

    @staticmethod
    def image():
        return ''
    
    def create_bulk(self, users, k):
        staff = users.filter(is_staff=True)
        return Post.objects.bulk_create([
            Post(
                created_by=random.choice(staff),
                title=title,
                lead=self.lead(),
                body=self.body(),
                image=self.image(),
            )
            for title in self.titles(k)
        ])


if __name__ == '__main__':
    UserManager().create_bulk()
    users = User.objects.only('pk', 'is_staff')

    TagManager().create_bulk(1000)
    tags = Tag.objects.only('pk')

    QuestionManager().create_bulk(users, 1000)
    questions = Question.objects.only('pk')
    QuestionManager.add_tags(1, 5, questions, tags)
    QuestionManager.add_likes(0, len(users), questions, users)

    SetManager().create_bulk(users, 150)
    sets = Set.objects.only('pk')
    SetManager.add_tags(3, 15, sets, tags)
    SetManager.add_likes(0, len(users), sets, users)
    SetManager.add_questions(15, 100, sets, questions)

    PostManager().create_bulk(users, 50)
