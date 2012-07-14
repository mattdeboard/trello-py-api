"""
A Trello API client focused on the concept of "resources". Heavily
influenced by "django-tastypie" https://github.com/toastdriven/django-tastypie
by Daniel Lindsley and contributors.

Please review the full Trello API documentation at:
https://trello.com/docs/index.html

"""
import json
import requests

try:
    from secrets import *
except ImportError:
    import sys
    print >> sys.stderr, ("You must create a `secrets' module that contains "
                          "the `TRELLO_API_KEY' and `TRELLO_TOKEN' constants.")


class TrelloResourceOptions(object):
    """
    A configuration class for ``TrelloResource``.
    
    """
    resource_uri_stub = None
    subresources = None
    parent_resources = None
    can_filter = None

    def __new__(cls, meta=None):
        overrides = {}
        
        if meta:
            for override_name in dir(meta):
                if not override_name.startswith('_'):
                    overrides[override_name] = getattr(meta, override_name)

        return object.__new__(type('TrelloResourceOptions', (cls,), overrides))
    
    
class DeclarativeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(DeclarativeMetaclass, cls).__new__(cls, name, bases,
                                                             attrs)
        opts = getattr(new_class, 'Meta', None)
        new_class._meta = TrelloResourceOptions(opts)
        return new_class

        
class TrelloResource(object):
    """
    This is the base class used to create subclasses for representing
    various Trello resources. This includes but is not limited to:

        - Boards
        - Cards
        - Lists
        - Members

    etc.

    """
    __metaclass__ = DeclarativeMetaclass

    def __init__(self, protocol='https', api_domain='api.trello.com',
                 api_version='1'):
        self.auth_string = '?key={key}&token={token}'.format(key=TRELLO_API_KEY,
                                                             token=TRELLO_TOKEN)
        self.api_url = '{protocol}://{domain}/{ver}/'.format(protocol=protocol,
                                                             domain=api_domain,
                                                             ver=api_version)

    def get_subresources(self, resource_id, resources=None):
        results = {}
        if not resources:
            resources = []
        else:
            resources = list(resources)
            
        r_set = set(resources)
        sr_set = set(self._meta.subresources)
        
        if r_set.intersection(sr_set) != r_set:
            raise AttributeError(
                "%s is not a valid subresource." % r_set.difference(sr_set)
            )

        kwargs = {
            'url': self.api_url,
            'stub': self._meta.resource_uri_stub,
            'auth': self.auth_string,
            'id': resource_id
        }
        
        for resource in resources:
            kwargs['subresource'] = resource
            request_url = '{url}{stub}/{id}/{subresource}{auth}'.format(**kwargs)
            resp = requests.get(request_url)

            if resp.status_code != 200:
                raise AttributeError

            results[resource] = self._subresource_urls(resource, resp.content)

        return results

    def filter_subresource(self, resource_id, subresource, filters=None):
        """
        Retrieve the URL for the set of instances of 'subresource' that
        match the criteria set forth in 'filters'.

        """
        if subresource not in self._meta.subresources:
            raise AttributeError("You must provide a valid subresource to "
                                 "filter.")

        if isinstance(filters, (list, tuple, set)):
            filters = ','.join(filters)
            
        resource_uri = self._resource_instance_uri(resource_id)
        request_url = u'{url}{auth}&filter={filters}'.format(
            url=resource_uri,
            filters=filters,
            auth=self.auth_string
        )
        resp = requests.get(request_url)

        if resp.status_code != 200:
            raise AttributeError

        return {subresource: self._subresource_urls(subresource, resp.content)}

    def _resource_instance_uri(self, resource_id):
        return u'{url}{stub}/{id}/'.format(url=self.api_url,
                                           stub=self._meta.resource_uri_stub,
                                           id=resource_id)

    def _subresource_urls(self, resource, response):
        kwargs = {'url': self.api_url, 'stub': resource,
                  'auth': self.auth_string}
        response = json.loads(response)

        try:
            ids = [result.get('id') for result in response if result.get('id')]
        except AttributeError:
            if response.get('id'):
                ids = [response.get('id')]
            else:
                raise StopIteration

        for _id in ids:
            kwargs['id'] = _id
            discovered_url = '{url}{stub}/{id}{auth}'.format(**kwargs)
            yield discovered_url
 

class Board(TrelloResource):
   
    class Meta:
        resource_uri_stub = 'boards'
        subresources = [
            'actions',
            'cards',
            'checklists',
            'lists',
            'members',
            'membersInvited'
        ]
        parent_resources = [
            'organization'
        ]
        can_filter = [
            'cards',
            'lists',
            'members'
        ]
            

