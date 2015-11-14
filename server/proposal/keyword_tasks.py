import redis

from cornerwise import celery_app

from . import idf, keywords
from .models import Attribute

celery_app.task(name="proposal.build_counts")
def build_counts(handles=[]):
    attrs = Attribute.objects.filter(handle__in=handles)
    r = redis.StrictRedis()

    for att in attrs:
        att_keywords = keywords.keywords(text)
        idf.add_document(r, att_keywords, att.pk)

celery_app.task(name="proposal.analyze_text")
def analyze_text(doc):
    pass

# For testing:
def add_full_text(r, doc):
    terms = keywords.keywords(doc.get_text())
    idf.add_document(r, terms, doc.pk)

def add_full_docs(docs):
    r = redis.StrictRedis()
    for doc in docs:
        if doc.fulltext:
            add_full_text(r, doc)

def top_terms(doc):
    r = redis.StrictRedis()
    terms = keywords.keywords(doc.get_text())
    return idf.sorted_terms(r, terms)