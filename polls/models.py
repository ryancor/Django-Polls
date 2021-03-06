import datetime
import collections
from collections import Counter
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone
from datetime import datetime, timedelta

class MyUser(models.Model):
	username = models.CharField(default='guest', max_length=255, unique=True)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	date_of_birth = models.DateField()
	joined = models.DateTimeField('date joined')
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	class Meta:
		db_table = u'my_user'

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'date_of_birth']

	def create_user(self, username, email, date_of_birth, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			username=self.normalize_username(username),
			email=self.normalize_email(email),
			date_of_birth=date_of_birth,
        )

		user.set_password(password)
		user.save(using=self._db)
		return user

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.username

	def get_short_name(n):
		x = n.username
		chunks, chunk_size = len(x), len(x)//2
		return ' '.join([ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ])

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - timedelta(days=1)

	def total_votes(q):
		if q.choice_set.count() == 2:
			c1 = q.choice_set.first()
			c2 = q.choice_set.last()
			calculate_votes = c1.votes + c2.votes
		elif q.choice_set.count() == 3:
			c1 = q.choice_set.all()[0]
			c2 = q.choice_set.all()[1]
			c3 = q.choice_set.all()[2]
			calculate_votes = c1.votes + c2.votes + c3.votes
		else:
			error = 'None'
			return error
		return calculate_votes

	def search(query):
		question = Question.objects.filter(question_text__startswith=query)
		for x in question:
			print(x.question_text)

	def post_date(q):
		return q.pub_date.strftime("%m/%d/%Y")

	def latest_questions(h):
		now = datetime.now()
		earlier = now - timedelta(hours=h)
		question = Question.objects.filter(pub_date__range=(earlier,now))
		for x in question:
			print(x.question_text)

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

	def title(self):
		return self.question.question_text

	def max_and_min(self):
		self.objects.all().aggregate(max(votes),
			sum(votes) / float(len(votes)), min(votes))

	def exists(c):
		choice = Choice.objects.all()
		choice = choice.filter(choice_text__iexact=c)
		if choice.exists() == True:
			return True
		else:
			return False

	def count(c):
		choice = Choice.objects.all()
		choice = choice.filter(choice_text__iexact=c)
		if choice.exists() == True:
			return choice.count()
		else:
			return 0

class Search(models.Model):
	search_text = models.CharField(max_length=80)
	pub_date = models.DateTimeField('date searched')

	def __str__(self):
		return self.search_text

	def search_date(q):
		return q.pub_date.strftime("%m/%d/%Y")

	def repeated_search(n):
		s = Search.objects.all()
		x = []
		for row in s:
			x.append(row.search_text[0:])
		return [item for item, count in collections.Counter(x).items() if count > n]

	def most_common(searcher):
		s = Search.objects.values(searcher)
		l = [keys for keys in s]
		results = list((object['search_text'] for object in l))
		c = Counter(results).most_common(2)
		return " : ".join( repr(e) for e in c )
