from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
# Create your models here.

class Topic(models.Model):
	topicId = models.AutoField(primary_key=True)
	topicName = models.CharField(max_length=200)
	def __str__(self):
		return self.topicName

class Tutorial(models.Model):
	topicId = models.ForeignKey('Topic',db_column='topicId')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=255, blank=True)
	complexity = models.CharField(max_length = 50)
	authorId = models.IntegerField()
	rating = models.IntegerField( null = True )
	content = models.TextField(default="write your content here")
	createdDate = models.DateTimeField(default=timezone.now)
	publishedDate = models.DateTimeField(blank=True, null=True)
	tags = TaggableManager()
	def __str__(self):
		return self.tags.all()

	def save(self, **kwargs):
		if self.title and not self.slug:
			self.slug = slugify(self.title)
		super(Tutorial, self).save(**kwargs)

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)
	
class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

