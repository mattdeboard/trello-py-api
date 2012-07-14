=============
trello-py-api
=============

trello-py-api is a client for Trello_\'s REST API. There are already a couple [1]_  [2]_ of working Python API clients for Trello, so why another?

The main reason is that I wanted to explore writing a REST API client without the concepts of ``Client`` objects or ``Connection`` instances. Those don't really fit how I think of REST APIs anymore. I'm just trying to figure out what a ``Resource``\-oriented REST API client would look like, and how it would behave. If a RESTful web service/REST API "is a collection of resources" [3]_, maybe the client should match that metaphor.

It doesn't seem like there's a consensus on what REST API clients should look like. That being said my brain did start churning when I read Google's `Client Design document <http://code.google.com/p/google-api-python-client/wiki/ClientDesignDocument>`_. They use a ``Resource`` class as the center of gravity for their API client framework. At this point I'm dropping in some of the concepts of `django-tastypie <https://github.com/toastdriven/django-tastypie/>`_ (mostly metaprogramming wrt ``Options`` metaclasses for ``Resource`` classes) and seeing how that shakes out.

I'd be interested in hearing feedback. 

.. _Trello: http://trello.com
.. [1] `py-trello <https://github.com/sarumont/py-trello>`_
.. [2] `trollop <https://bitbucket.org/btubbs/trollop>`_
.. [3] `Wikipedia entry on REST <http://en.wikipedia.org/wiki/REST#RESTful_web_services>`_

    
       
