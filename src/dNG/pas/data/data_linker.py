# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;datalinker

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from sqlalchemy.sql.expression import func as sql
from sqlalchemy.sql.expression import or_
from sqlalchemy.sql.functions import count as sql_count
from weakref import WeakValueDictionary

from dNG.pas.data.settings import Settings
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.database.sort_definition import SortDefinition
from dNG.pas.database.instance_iterator import InstanceIterator
from dNG.pas.database.instances.data_linker import DataLinker as _DbDataLinker
from dNG.pas.database.instances.data_linker_meta import DataLinkerMeta as _DbDataLinkerMeta
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .binary import Binary
from .data_linker_structure import DataLinkerStructure

class DataLinker(Instance):
#
	"""
This class provides an hierarchical abstraction layer called DataLinker.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=maybe-no-member

	_DB_INSTANCE_CLASS = _DbDataLinker
	"""
SQLAlchemy database instance class to initialize for new instances.
	"""
	SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT = 1
	"""
Sub entries are defined to represent "additional content"
	"""

	_structure_instance_cache = WeakValueDictionary()
	"""
Structure instance cache
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(DataLinker)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.1.00
		"""

		Instance.__init__(self, db_instance)

		self.db_id = (None if (db_instance is None) else self.get_id())
		"""
Database ID used for reloading
		"""
		self.structure_instance = None
		"""
Structure instance for the main ID of this entry
		"""
	#

	def add_entry(self, child):
	#
		"""
Add the given child.

:param child: DataLinker instance

:since: v0.1.00
		"""

		# pylint: disable=protected-access

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.add_entry()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		if (isinstance(child, DataLinker)):
		#
			with self:
			#
				child_id = child.get_id()

				if (child_id != self.local.db_instance.id):
				#
					self.local.db_instance.rel_children.append(child._get_db_instance())
					child.set_data_attributes(id_main = self.local.db_instance.id_main)

					self.set_data_attributes(sub_entries = "++")
				#
			#
		#
	#

	def _analyze_structure(self, cache_id):
	#
		"""
Analyzes the entry structure based on the main ID of this instance.

:param cache_id: ID used for building the structure SQLAlchemy query and
                 cache its result.

:since: v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._analyze_structure()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		structure_instance = DataLinker._structure_instance_cache.get(cache_id)

		if (structure_instance is None):
		#
			structure_instance = DataLinkerStructure()

			with self:
			#
				db_query = self.local.connection.query(_DbDataLinker)
				db_query = self._apply_structure_join_condition(db_query, cache_id)
				db_query = self._apply_structure_where_condition(db_query, cache_id)

				if (self._db_sort_definition is None): db_query = self._apply_structure_order_by_condition(db_query, cache_id)
				else: db_query = self._db_sort_definition.apply(db_query)

				for entry in DataLinker.iterator(_DbDataLinker, self.local.connection.execute(db_query)): structure_instance.add(entry)
			#

			DataLinker._structure_instance_cache[cache_id] = structure_instance
		#

		self.structure_instance = structure_instance
	#

	def _apply_structure_join_condition(self, db_query, cache_id):
	#
		"""
Returns the modified SQLAlchemy database query with the "join" condition
applied.

:param cache_id: ID used for building the structure SQLAlchemy query.

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._apply_structure_join_condition()- (#echo(__LINE__)#)", self, context = "pas_datalinker")
		return db_query.outerjoin(_DbDataLinkerMeta, _DbDataLinker.id == _DbDataLinkerMeta.id)
	#

	def _apply_structure_order_by_condition(self, db_query, cache_id):
	#
		"""
Returns the modified SQLAlchemy database query with the "order by" condition
applied.

:param cache_id: ID used for building the structure SQLAlchemy query.

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._apply_structure_order_by_condition()- (#echo(__LINE__)#)", self, context = "pas_datalinker")
		return self._apply_db_sort_definition(db_query, "DataLinker")
	#

	def _apply_structure_where_condition(self, db_query, cache_id):
	#
		"""
Returns the modified SQLAlchemy database query with the "where" condition
applied.

:param cache_id: ID used for building the structure SQLAlchemy query.

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._apply_structure_where_condition()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		db_query = db_query.filter(_DbDataLinker.id_main == self.local.db_instance.id_main,
		                           _DbDataLinker.identity == self.local.db_instance.identity
		                          )

		return DataLinker._db_apply_id_site_condition(db_query)
	#

	def _apply_sub_entries_join_condition(self, db_query, context = None):
	#
		"""
Returns the modified SQLAlchemy database query with the "join" condition
applied.

:param context: Sub entries request context

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._apply_sub_entries_condition()- (#echo(__LINE__)#)", self, context = "pas_datalinker")
		return db_query.outerjoin(_DbDataLinkerMeta, _DbDataLinker.id == _DbDataLinkerMeta.id)
	#

	def _apply_sub_entries_order_by_condition(self, db_query, context = None):
	#
		"""
Returns the modified SQLAlchemy database query with the "order by" condition
applied.

:param context: Sub entries request context

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._apply_sub_entries_order_by_condition()- (#echo(__LINE__)#)", self, context = "pas_datalinker")
		return self._apply_db_sort_definition(db_query, context)
	#

	def delete(self):
	#
		"""
Deletes this entry from the database.

:since: v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.delete()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		with self:
		#
			if (self.local.db_instance.rel_parent is not None): DataLinker(self.local.db_instance.rel_parent).remove_entry(self)
			if (self.local.db_instance.rel_meta is not None): self.local.connection.delete(self.local.db_instance.rel_meta)

			Instance.delete(self)
		#
	#

	def _ensure_non_expired_db_instance(self):
	#
		"""
Ensures that the encapsulated database instance does not contain expired
attributes.

:since: v0.1.02
		"""
	#

	get_id = Instance._wrap_getter("id")
	"""
Returns the ID of this instance.

:return: (str) DataLinker ID; None if undefined
:since:  v0.1.00
	"""

	get_identity = Instance._wrap_getter("identity")
	"""
Returns the identity of this DataLinker instance.

:return: (str) DataLinker ID; None if undefined
:since:  v0.1.00
	"""

	def _get_default_sort_definition(self, context = None):
	#
		"""
Returns the default sort definition list.

:param context: Sort definition context

:return: (object) Sort definition
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._get_default_sort_definition({1})- (#echo(__LINE__)#)", self, context, context = "pas_datalinker")

		return SortDefinition([ ( "position", SortDefinition.ASCENDING ),
		                        ( "title", SortDefinition.ASCENDING ),
		                        ( "id", SortDefinition.ASCENDING )
		                      ]
		                      if (context == "DataLinker") else
		                      [ ( "position", SortDefinition.ASCENDING ),
		                        ( "time_sortable", SortDefinition.DESCENDING ),
		                        ( "title", SortDefinition.ASCENDING )
		                      ]
		                     )
	#

	def get_sub_entries(self, offset = 0, limit = -1, identity = None, exclude_identity = None):
	#
		"""
Returns the child entries of this instance.

:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit
:param identity: DataLinker children should only be of the given identity
:param exclude_identity: DataLinker children should not be of the given identity

:return: (list) DataLinker children instances
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_sub_entries({1:d}, {2:d})- (#echo(__LINE__)#)", self, offset, limit, context = "pas_datalinker")

		if (identity is not None and exclude_identity is not None): raise ValueException("Defining both an identity and to exclude an identity is not supported")

		with self:
		#
			db_class = _DbDataLinker
			db_query = self.local.db_instance.rel_children

			if (isinstance(identity, _DbDataLinker)):
			#
				db_class = identity._DB_INSTANCE_CLASS
				identity = identity.__name__
			#

			if (identity is not None):
			#
				if (self.local.db_instance.identity == identity): db_class = DataLinker.get_db_class(self.__class__)
				db_query = db_query.filter(db_class.identity == identity)
			#

			if (isinstance(exclude_identity, _DbDataLinker)): exclude_identity = exclude_identity.__name__
			if (exclude_identity is not None): db_query = db_query.filter(db_class.identity != exclude_identity)

			db_query = DataLinker._db_apply_id_site_condition(db_query)

			db_query = self._apply_sub_entries_join_condition(db_query, identity)
			db_query = self._apply_sub_entries_order_by_condition(db_query, identity)
			if (offset > 0): db_query = db_query.offset(offset)
			if (limit > 0): db_query = db_query.limit(limit)

			return DataLinker.iterator(db_class, self.local.connection.execute(db_query))
		#
	#

	def get_sub_entries_count(self, identity = None, exclude_identity = None):
	#
		"""
Returns the number of child entries of this instance.

:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit
:param identity: Count only DataLinker children of the given identity
:param exclude_identity: Count only DataLinker children not be of the given identity

:return: (int) Number of child entries
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_sub_entries_count()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		if (identity is None and exclude_identity is None): _return = self.get_data_attributes("sub_entries")['sub_entries']
		elif (identity is not None and exclude_identity is not None): raise ValueException("Defining both an identity and to exclude an identity is not supported")
		else:
		#
			with self:
			#
				db_query = self.local.db_instance.rel_children.with_entities(sql.count(_DbDataLinker.id))

				if (identity is not None): db_query = db_query.filter(_DbDataLinker.identity == identity)
				elif (exclude_identity is not None): db_query = db_query.filter(_DbDataLinker.identity != exclude_identity)

				db_query = DataLinker._db_apply_id_site_condition(db_query)

				_return = db_query.scalar()
			#
		#

		return _return
	#

	def _get_unknown_data_attribute(self, attribute):
	#
		"""
Returns the data for the requested attribute not defined for this instance.

:param attribute: Requested attribute

:return: (dict) Value for the requested attribute; None if undefined
:since:  v0.1.00
		"""

		return (getattr(self.local.db_instance.rel_meta, attribute) if (self.local.db_instance.rel_meta is not None and hasattr(self.local.db_instance.rel_meta, attribute)) else Instance._get_unknown_data_attribute(self, attribute))
	#

	def is_main_entry(self):
	#
		"""
Returns true if this is the main entry of the current context.

:return: (bool) True if main entry
:since:  v0.1.00
		"""

		with self: return (self.local.db_instance.id == self.local.db_instance.id_main)
	#

	def is_reloadable(self):
	#
		"""
Returns true if the instance can be reloaded automatically in another
thread.

:return: (bool) True if reloadable
:since:  v0.1.00
		"""

		return (self.db_id is not None)
	#

	def is_tag_unique(self, tag):
	#
		"""
Returns true if the given tag is unique in the current main context.

:return: (bool) True if the Tag to be checked
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.is_tag_unique()- (#echo(__LINE__)#)", self, context = "pas_datalinker")
		_return = True

		with self:
		#
			try: self._validate_unique_tag(tag)
			except ValueException: _return = False
		#

		return _return
	#

	def load_main(self):
	#
		"""
Load the main instance. Please note that it could be the same DataLinker
instance as the current one.

:return: (object) Main DataLinker instance; None if no main entry exists
:since:  v0.1.00
		"""

		_return = None

		with self:
		#
			if (self.local.db_instance.rel_main is not None):
			#
				_return = (self
				           if (self.local.db_instance.id == self.local.db_instance.id_main) else
				           DataLinker(self.local.db_instance.rel_main)
				          )
			#
		#

		return _return
	#

	def load_parent(self):
	#
		"""
Load the parent instance.

:return: (object) Parent DataLinker instance; None if no parent exists
:since:  v0.1.00
		"""

		with self:
		#
			_return = (None
			           if (self.local.db_instance.rel_parent is None
			               or self.local.db_instance.id == self.local.db_instance.id_parent
			              ) else
			           DataLinker(self.local.db_instance.rel_parent)
			          )

			if (_return is None
			    and self.local.db_instance.rel_main is not None
			    and self.local.db_instance.id != self.local.db_instance.id_main
			   ): _return = DataLinker(self.local.db_instance.rel_main)
		#

		return _return
	#

	def _reload(self):
	#
		"""
Implementation of the reloading SQLAlchemy database instance logic.

:since: v0.1.00
		"""

		if (self.local.db_instance is None):
		#
			if (self.db_id is None): raise IOException("Database instance is not reloadable.")
			else: self.local.db_instance = Instance.get_db_class_query(self.__class__).filter(_DbDataLinker.id == self.db_id).first()
		#
		else: Instance._reload(self)
	#

	def remove_entry(self, child):
	#
		"""
Remove the given child.

:param child: DataLinker instance

:since: v0.1.00
		"""

		# pylint: disable=protected-access

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.remove_entry()- (#echo(__LINE__)#)", self, context = "pas_datalinker")

		if (isinstance(child, DataLinker)):
		#
			with self:
			#
				self.local.db_instance.rel_children.remove(child._get_db_instance())
				child.set_data_attributes(id_main = None)

				self.set_data_attributes(sub_entries = "--")
			#
		#
	#

	def set_as_main_entry(self):
	#
		"""
Sets this entry to be main entry of the current context.

:since: v0.1.00
		"""

		with self: self.local.db_instance.id_main = self.local.db_instance.id
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		with self, self.local.connection.no_autoflush:
		#
			if (self.db_id is None): self.db_id = self.local.db_instance.id

			if ("id_parent" in kwargs): self.local.db_instance.id_parent = kwargs['id_parent']
			if ("id_main" in kwargs): self.local.db_instance.id_main = kwargs['id_main']
			if ("id_site" in kwargs): self.local.db_instance.id_site = Binary.utf8(kwargs['id_site'])
			if ("position" in kwargs): self.local.db_instance.position = kwargs['position']

			if ("sub_entries" in kwargs or "sub_entries_type" in kwargs or "time_sortable" in kwargs or "symbol" in kwargs or "title" in kwargs or "tag" in kwargs or "views_count" in kwargs or "views" in kwargs):
			#
				if (self.local.db_instance.rel_meta is None):
				#
					self.local.db_instance.rel_meta = _DbDataLinkerMeta()
					db_meta_instance = self.local.db_instance.rel_meta
				#
				else: db_meta_instance = self.local.db_instance.rel_meta

				if ("sub_entries" in kwargs):
				#
					if (kwargs['sub_entries'] == "++"): db_meta_instance.sub_entries = db_meta_instance.sub_entries + 1
					elif (kwargs['sub_entries'] == "--"):
					#
						if (db_meta_instance.sub_entries > 0): db_meta_instance.sub_entries = db_meta_instance.sub_entries - 1
					#
					else: db_meta_instance.sub_entries = kwargs['sub_entries']
				#

				if ("sub_entries_type" in kwargs): db_meta_instance.sub_entries_type = kwargs['sub_entries_type']
				if ("time_sortable" in kwargs): db_meta_instance.time_sortable = int(kwargs['time_sortable'])
				if ("symbol" in kwargs): db_meta_instance.symbol = Binary.utf8(kwargs['symbol'])
				if ("title" in kwargs): db_meta_instance.title = Binary.utf8(kwargs['title'])

				if ("tag" in kwargs and kwargs['tag'] is not None and len(kwargs['tag']) > 0):
				#
					tag = Binary.utf8(kwargs['tag'])
					if (tag is not None and db_meta_instance.tag != tag): self._validate_unique_tag(tag)
					db_meta_instance.tag = tag
				#

				if ("views_count" in kwargs): db_meta_instance.views_count = kwargs['views_count']
				if ("views" in kwargs): db_meta_instance.views = kwargs['views']
			#
		#
	#

	def _validate_unique_tag(self, tag):
	#
		"""
Validates the given tag to be unique in the current main context.

:param tag: Tag to be checked

:since: v0.1.00
		"""

		if (self.local.connection.query(sql_count(_DbDataLinker.id))
		    .join(_DbDataLinkerMeta, (_DbDataLinker.id == _DbDataLinkerMeta.id))
		    .filter(_DbDataLinker.id_main == self.local.db_instance.id_main, _DbDataLinkerMeta.tag == tag)
		    .scalar() > 0
		   ): raise ValueException("Tag can't be used twice in the same context")
	#

	@staticmethod
	def _db_apply_id_site_condition(db_query):
	#
		"""
Returns the modified SQLAlchemy database query with the "where" condition
for the site ID applied.

:return: (object) SQLAlchemy database query
:since:  v0.1.00
		"""

		id_site = Settings.get("pas_global_datalinker_site_id")
		if (id_site is not None): db_query = db_query.filter(or_(_DbDataLinker.id_site is None, _DbDataLinker.id_site == id_site))

		return db_query
	#

	@classmethod
	def get_entries_count_with_condition(cls, condition_definition):
	#
		"""
Returns the count of database entries based on the given condition
definition.

:param cls: Python class
:param condition_definition: ConditionDefinition instance

:return: (int) Number of DataLinker entries
:since:  v0.1.00
		"""

		db_class = DataLinker.get_db_class(cls)
		if (db_class is None): db_class = _DbDataLinker

		return DataLinker._get_entries_count_with_condition(db_class, condition_definition)
	#

	@staticmethod
	def _get_entries_count_with_condition(entity, condition_definition):
	#
		"""
Returns the count of cls entries based on the given condition definition.

:param entity: SQLAlchemy database entity
:param condition_definition: ConditionDefinition instance

:return: (int) Number of DataLinker entries
:since:  v0.1.00
		"""

		with Connection.get_instance() as connection:
		#
			db_query = connection.query(sql_count(entity.id))
			db_query = db_query.outerjoin(_DbDataLinkerMeta, _DbDataLinker.id == _DbDataLinkerMeta.id)

			db_query = DataLinker._db_apply_id_site_condition(db_query)
			db_query = condition_definition.apply(entity, db_query)

			return db_query.scalar()
		#
	#

	@classmethod
	def load_entries_list_with_condition(cls, condition_definition, offset = 0, limit = -1, sort_definition = None):
	#
		"""
Loads a list of database instances based on the given condition definition.

:param cls: Python class
:param condition_definition: ConditionDefinition instance
:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit
:param sort_definition: SortDefinition instance

:return: (list) List of DataLinker instances on success
:since:  v0.1.00
		"""

		db_class = DataLinker.get_db_class(cls)
		if (db_class is None): db_class = _DbDataLinker

		return DataLinker._load_entries_list_with_condition(db_class, condition_definition, offset, limit, sort_definition)
	#

	@classmethod
	def _load_entries_list_with_condition(cls, entity, condition_definition, offset = 0, limit = -1, sort_definition = None):
	#
		"""
Loads a list of cls instances based on the given condition definition.

:param cls: Python class
:param entity: SQLAlchemy database entity
:param condition_definition: ConditionDefinition instance
:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit
:param sort_definition: SortDefinition instance

:return: (list) List of DataLinker instances on success
:since:  v0.1.00
		"""

		with Connection.get_instance() as connection:
		#
			db_query = connection.query(entity)
			db_query = db_query.outerjoin(_DbDataLinkerMeta, _DbDataLinker.id == _DbDataLinkerMeta.id)

			db_query = DataLinker._db_apply_id_site_condition(db_query)
			db_query = condition_definition.apply(entity, db_query)

			if (sort_definition is None):
			#
				sort_definition = SortDefinition([ ( "position", SortDefinition.ASCENDING ),
				                                   ( "title", SortDefinition.ASCENDING ),
				                                   ( "id", SortDefinition.ASCENDING )
				                                 ])
			#

			db_query = sort_definition.apply(entity, db_query)
			if (offset > 0): db_query = db_query.offset(offset)
			if (limit > 0): db_query = db_query.limit(limit)

			return InstanceIterator(entity, connection.execute(db_query), instance_class = cls)
		#
	#

	@classmethod
	def load_id(cls, _id):
	#
		"""
Load DataLinker instance by ID.

:param cls: Expected encapsulating database instance class
:param _id: DataLinker ID

:return: (object) DataLinker instance on success
:since:  v0.1.00
		"""

		if (_id is None): raise NothingMatchedException("DataLinker ID is invalid")

		with Connection.get_instance():
		#
			db_query = Instance.get_db_class_query(cls)
			db_query = DataLinker._db_apply_id_site_condition(db_query)
			db_instance = db_query.get(_id)

			if (db_instance is None): raise NothingMatchedException("DataLinker ID '{0}' is invalid".format(_id))
			Instance._ensure_db_class(cls, db_instance)

			return DataLinker(db_instance)
		#
	#

	@classmethod
	def load_tag(cls, tag, id_main):
	#
		"""
Load DataLinker instance by tag.

:param cls: Expected encapsulating database instance class
:param tag: DataLinker tag
:param id_main: DataLinker main ID where the unique tag is looked up

:return: (object) DataLinker instance on success
:since:  v0.1.00
		"""

		if (tag is None): raise NothingMatchedException("DataLinker tag is invalid")

		with Connection.get_instance():
		#
			db_query = (Instance.get_db_class_query(cls)
			            .join(_DbDataLinkerMeta, (_DbDataLinker.id == _DbDataLinkerMeta.id))
			           )

			db_query = DataLinker._db_apply_id_site_condition(db_query)

			db_instance = (db_query.filter(_DbDataLinkerMeta.tag == tag, _DbDataLinker.id_main == id_main)
			               .first()
			              )

			if (db_instance is None): raise NothingMatchedException("DataLinker tag '{0}' not found".format(tag))
			Instance._ensure_db_class(cls, db_instance)

			return DataLinker(db_instance)
		#
	#
#

##j## EOF