import atom
import gdata

DOUBAN_NAMESPACE = 'http://www.douban.com/xmlns/'

def _t(v):
    if v is not None:
        return str(v)

def _decode(v):
    if v is not None:
        if isinstance(v, unicode) == False:
            return v.decode('utf-8')
        return v

class Location(atom.AtomBase):
    _tag = 'location'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()

    def __init__(self, loc=None, **kwargs):
        atom.AtomBase.__init__(self, text=loc, **kwargs)


class Uid(atom.AtomBase):
    _tag = 'uid'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()

    def __init__(self, loc=None, **kwargs):
        atom.AtomBase.__init__(self, text=loc, **kwargs)

class Rating(atom.AtomBase):
    """As gdata.py has not defined this element, we do this here.

    Should be removed when gdata.py includes the definition.

    """
    _tag = 'rating'
    _namespace = gdata.GDATA_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['average'] = 'average'
    _attributes['min'] = 'min'
    _attributes['max'] = 'max'
    _attributes['numRaters'] = 'numRaters'
    _attributes['value'] = 'value'

    def __init__(self, value=None, average=None,
            min=1, max=5, numRaters=1, **kwargs):
        atom.AtomBase.__init__(self, **kwargs)
        self.value = _t(value)
        self.average = _t(average)
        self.min = _t(min)
        self.max = _t(max)
        self.numRaters = _t(numRaters)


class Attribute(atom.AtomBase):
    _tag = 'attribute'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['name'] = 'name'
    _attributes['index'] = 'index'
    _attributes['lang'] = 'lang'

    def __init__(self, name=None, value=None, index=None, lang=None, **kwargs):
        atom.AtomBase.__init__(self, text=value, **kwargs)
        self.name = name
        self.index = _t(index)
        self.lang = lang

class Entity(atom.AtomBase):
    _tag = 'entity'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['name'] = 'name'

    def __init__(self, name=None, value=None, **kwargs):
        atom.AtomBase.__init__(self, text=value, **kwargs)
        self.name = name

class Tag(atom.AtomBase):
    _tag = 'tag'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['count'] = 'count'
    _attributes['name'] = 'name'

    def __init__(self, name=None, count=None, **kwargs):
        atom.AtomBase.__init__(self, **kwargs)
        self.name = name
        self.count = _t(count)


class Status(atom.AtomBase):
    _tag = 'status'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()

    def __init__(self, status=None, **kwargs):
        atom.AtomBase.__init__(self, text=status, **kwargs)


class Count(atom.AtomBase):
    _tag = 'count'
    _namespace = DOUBAN_NAMESPACE

    def __init__(self, count=None, **kwargs):
        atom.AtomBase.__init__(self, text=count, **kwargs)

def CreateClassFromXMLString(target_class, xml_string):
    return atom.CreateClassFromXMLString(target_class,
            xml_string.decode('utf8', 'ignore'), 'utf8')

class PeopleEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}location' % (DOUBAN_NAMESPACE)] = ('location', Location)
    _children['{%s}uid' % (DOUBAN_NAMESPACE)] = ('uid', Uid)

    def __init__(self, location=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.location = location

def PeopleEntryFromString(xml_string):
    return CreateClassFromXMLString(PeopleEntry, xml_string)

class PeopleFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [PeopleEntry])

def PeopleFeedFromString(xml_string):
    return CreateClassFromXMLString(PeopleFeed, xml_string)


class SubjectEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])
    _children['{%s}tag' % (DOUBAN_NAMESPACE)] = ('tag', [Tag])

    def __init__(self, rating=None, attribute=None, tag=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.rating = rating
        self.attribute = attribute or []
        self.tag = tag or []

    def GetImageLink(self):
        for a_link in self.link:
            if a_link.rel == 'image':
                return a_link

    def GetCollectionLink(self):
        for a_link in self.link:
            if a_link.rel == 'collection':
                return a_link

class Subject(SubjectEntry):
    """In some places we use <db:subject> to represent a subject entry."""
    _tag = 'subject'
    _namespace = DOUBAN_NAMESPACE

class BookEntry(SubjectEntry):
    pass

def BookEntryFromString(xml_string):
    return CreateClassFromXMLString(BookEntry, xml_string)


class BookFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [BookEntry])

def BookFeedFromString(xml_string):
    return CreateClassFromXMLString(BookFeed, xml_string)


class MovieEntry(SubjectEntry):
    pass

def MovieEntryFromString(xml_string):
    return CreateClassFromXMLString(MovieEntry, xml_string)


class MovieFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [MovieEntry])

def MovieFeedFromString(xml_string):
    return CreateClassFromXMLString(MovieFeed, xml_string)


class MusicEntry(SubjectEntry):
    pass

def MusicEntryFromString(xml_string):
    return CreateClassFromXMLString(MusicEntry, xml_string)


class MusicFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [MusicEntry])

def MusicFeedFromString(xml_string):
    return CreateClassFromXMLString(MusicFeed, xml_string)

class BroadcastingEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])

    def __init__(self, attribute=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.attribute = attribute or []

def BroadcastingEntryFromString(xml_string):
    return CreateClassFromXMLString(BroadcastingEntry, xml_string)

class BroadcastingFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [BroadcastingEntry])

def BroadcastingFeedFromString(xml_string):
    return CreateClassFromXMLString(BroadcastingFeed, xml_string)

class NoteEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])

    def __init__(self, attribute=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.attribute = attribute or []


def NoteEntryFromString(xml_string):
    return CreateClassFromXMLString(NoteEntry, xml_string)


class NoteFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [NoteEntry])

def NoteFeedFromString(xml_string):
    return CreateClassFromXMLString(NoteFeed, xml_string)

class ReviewEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}subject' % (DOUBAN_NAMESPACE)] = ('subject', Subject)
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)

    def __init__(self, subject=None, rating=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.subject = subject
        self.rating = rating

def ReviewEntryFromString(xml_string):
    return CreateClassFromXMLString(ReviewEntry, xml_string)


class ReviewFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [ReviewEntry])

def ReviewFeedFromString(xml_string):
    return CreateClassFromXMLString(ReviewFeed, xml_string)


class CollectionEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}status' % (DOUBAN_NAMESPACE)] = ('status', Status)
    _children['{%s}subject' % (DOUBAN_NAMESPACE)] = ('subject', Subject)
    _children['{%s}tag' % (DOUBAN_NAMESPACE)] = ('tags', [Tag])
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)
    _children['{%s}attribute' % (gdata.GDATA_NAMESPACE)] = ('attribute', [Attribute])

    def __init__(self, status=None, subject=None, tag=None, rating=None, attribute=None,
            **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.status = status
        self.subject = subject
        self.tags = tag or []
        self.rating = rating
	self.attribute = attribute or []

def CollectionEntryFromString(xml_string):
    return CreateClassFromXMLString(CollectionEntry, xml_string)

class CollectionFeed(gdata.GDataFeed):
    _children = gdata.GDataFeed._children.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [CollectionEntry])

def CollectionFeedFromString(xml_string):
    return CreateClassFromXMLString(CollectionFeed, xml_string)


class TagEntry(gdata.GDataEntry):
    _children = gdata.GDataEntry._children.copy()
    _children['{%s}count' % (DOUBAN_NAMESPACE)] = ('count', Count)
    def __init__(self, count=None, **kwargs):

        gdata.GDataEntry.__init__(self, **kwargs)
        self.count = count

class TagFeed(gdata.GDataFeed):
    _children = gdata.GDataFeed._children.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [TagEntry])

def TagFeedFromString(xml_string):
    return CreateClassFromXMLString(TagFeed, xml_string)

class When(atom.AtomBase):

    _tag = 'when'
    _namespace = gdata.GDATA_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['startTime'] = 'start_time'
    _attributes['endTime'] = 'end_time'

    def __init__(self, start_time=None, end_time=None, extension_elements=None,
          extension_attributes=None, text=None):
        self.start_time = start_time
        self.end_time = end_time
        self.extension_elements = extension_elements or []
        self.extension_attributes = extension_attributes or {}
        self.text = text

class Where(atom.AtomBase):

    _tag = 'where'
    _namespace = gdata.GDATA_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['valueString'] = 'value_string'

    def __init__(self, value_string=None, extension_elements=None,
          extension_attributes=None, text=None):
        self.value_string = value_string
        self.extension_elements = extension_elements or []
        self.extension_attributes = extension_attributes or {}
        self.text = text

class EventEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])
    _children['{%s}where' % gdata.GDATA_NAMESPACE] = ('where', Where)
    _children['{%s}when' % gdata.GDATA_NAMESPACE] = ('when', When)

    def __init__(self, attribute=None, when=None, where=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.attribute = attribute or []
        self.when = when
        self.where = where

def EventEntryFromString(xml_string):
    return CreateClassFromXMLString(EventEntry, xml_string)

class EventFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [EventEntry])

def EventFeedFromString(xml_string):
    return CreateClassFromXMLString(EventFeed, xml_string)

class RecommendationEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])

    def __init__(self, attribute=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.attribute = attribute or []

def RecommendationEntryFromString(xml_string):
    return CreateClassFromXMLString(RecommendationEntry, xml_string)

class RecommendationFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [RecommendationEntry])

def RecommendationFeedFromString(xml_string):
    return CreateClassFromXMLString(RecommendationFeed, xml_string)

class RecommendationCommentEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()

    def __init__(self, attribute=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)

def RecommendationCommentEntryFromString(xml_string):
    return CreateClassFromXMLString(RecommendationCommentEntry, xml_string)

class RecommendationCommentFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [RecommendationEntry])

def RecommendationCommentFeedFromString(xml_string):
    return CreateClassFromXMLString(RecommendationCommentFeed, xml_string)

class DoumailEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])
    _children['{%s}entity' % (DOUBAN_NAMESPACE)] = ('entity', [Entity])

    def __init__(self, attribute=None, entity=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.attribute = attribute or []
        self.entity = entity or []

def DoumailEntryFromString(xml_string):
    return CreateClassFromXMLString(DoumailEntry, xml_string)

class DoumailFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [DoumailEntry])

def DoumailFeedFromString(xml_string):
    return CreateClassFromXMLString(DoumailFeed, xml_string)


