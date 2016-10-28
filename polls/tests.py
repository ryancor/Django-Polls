import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question, Search


class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), True)

	def test_was_published_recently_with_future_question(self):
		time = timezone.now() - datetime.timedelta(days=1)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def count_total_votes(self):
		question = Question.objects.all()
		for x in question:
			self.assertIs(x.total_votes() >= 1)

	def create_question(question_text, days):
		time = timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text=question_text, pub_date=time)

	def most_recent_questions(question_text, days):
		time = timezone.now() + datetime.timedelta(days=days)
		q = Question.objects.create(question_text=question_text, pub_date=time)
		q_time = q.latest_questions(48)
		return self.assertIs(q_time, True)


class QuestionViewTests(TestCase):

	# No polls available
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['questioned'], [])

	# '/' gets a 302
	def test_route_404(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)

	def text_index_view_with_past_questions(self):
		create_question(question_text="Past question.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['<Question: Past question.'])


class SearchMethodTests(TestCase):

	# Search gets received on BE
	def test_search_saves(self):
		search_text = 'sports'
		time = timezone.now() + datetime.timedelta(days=1)
		Search.objects.create(search_text=search_text, pub_date=time)
		return Search.objects.filter(search_text__iexact=search_text)

	def repeated_search_counts(self):
		s = Search.objects.all()
		results = []
		for row in s:
			results.append(row.search_text)
		len(Search.repeated_search(1)) < len(results)
