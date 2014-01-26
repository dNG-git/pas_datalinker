# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.DataLinker
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;datalinker

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
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasDataLinkerVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from sqlalchemy.sql.functions import count as sql_count

from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.instances.data_linker import DataLinker as _DbDataLinker
from dNG.pas.database.instances.data_linker_meta import DataLinkerMeta as _DbDataLinkerMeta
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .binary import Binary

class DataLinker(Instance):
#
	"""
This class provides an hierarchical abstraction layer called DataLinker.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(DataLinker)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.1.00
		"""

		Instance.__init__(self, db_instance)

		self.db_id = None
		"""
Database ID used for reloading
		"""

		if (db_instance != None):
		#
			with self: self.db_id = self.local.db_instance.id
		#
	#

	def _data_get(self, attribute):
	#
		"""
Return the data for the requested attribute.

:param attribute: Requested attribute

:return: (dict) Value for the requested attribute; None if undefined
:since:  v0.1.00
		"""

		if (attribute == "title" and self.local.db_instance.title_alt != ""): _return = self.local.db_instance.title_alt
		elif (attribute == "title_orig" and self.local.db_instance.rel_meta != None): _return = self.local.db_instance.rel_meta.title
		else: _return = Instance._data_get(self, attribute)

		return _return
	#

	def _data_get_unknown(self, attribute):
	#
		"""
Return the data for the requested attribute not defined for this instance.

:param attribute: Requested attribute

:return: (dict) Value for the requested attribute; None if undefined
:since:  v0.1.00
		"""

		return (getattr(self.local.db_instance.rel_meta, attribute) if (self.local.db_instance.rel_meta != None and hasattr(self.local.db_instance.rel_meta, attribute)) else Instance._data_get_unknown(self, attribute))
	#

	def data_set(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		if (self.local.db_instance == None): self.local.db_instance = _DbDataLinker()

		with self:
		#
			if (self.db_id == None): self.db_id = self.local.db_instance.id

			if ("id_object" in kwargs): self.local.db_instance.id_object = kwargs['id_object']
			if ("id_parent" in kwargs): self.local.db_instance.id_parent = kwargs['id_parent']
			if ("id_main" in kwargs): self.local.db_instance.id_main = Binary.utf8(kwargs['id_main'])
			if ("id_site" in kwargs): self.local.db_instance.id_site = Binary.utf8(kwargs['id_site'])
			if ("type" in kwargs): self.local.db_instance.type = kwargs['type']
			if ("position" in kwargs): self.local.db_instance.position = kwargs['position']
			if ("title_alt" in kwargs): self.local.db_instance.title_alt = Binary.utf8(kwargs['title_alt'])

			if ("objects" in kwargs or "objects_sub_type" in kwargs or "time_sortable" in kwargs or "symbol" in kwargs or "title" in kwargs or "tag" in kwargs or "views_count" in kwargs or "views" in kwargs):
			#
				if (self.local.db_instance.rel_meta == None):
				#
					self.local.db_instance.rel_meta = _DbDataLinkerMeta()
					self.local.db_instance.rel_meta.id = self.local.db_instance.id_object
					db_meta_instance = self.local.db_instance.rel_meta
				#
				else: db_meta_instance = self.local.db_instance.rel_meta

				if ("objects" in kwargs):
				#
					if (kwargs['objects'] == "++"): db_meta_instance.objects = db_meta_instance.objects + 1
					elif (kwargs['objects'] == "--"):
					#
						if (db_meta_instance.objects > 0): db_meta_instance.objects = db_meta_instance.objects - 1
					#
					else: db_meta_instance.objects = kwargs['objects']
				#

				if ("objects_sub_type" in kwargs): db_meta_instance.objects_sub_type = kwargs['objects_sub_type']
				if ("time_sortable" in kwargs): db_meta_instance.time_sortable = int(kwargs['time_sortable'])
				if ("symbol" in kwargs): db_meta_instance.symbol = Binary.utf8(kwargs['symbol'])
				if ("title" in kwargs): db_meta_instance.title = Binary.utf8(kwargs['title'])

				if ("tag" in kwargs and kwargs['tag'] != None and len(kwargs['tag']) > 0):
				#
					tag = Binary.utf8(kwargs['tag'])
					if (db_meta_instance.tag != None and db_meta_instance.tag != tag): self._validate_unique_tag(tag)
					db_meta_instance.tag = tag
				#

				if ("views_count" in kwargs): db_meta_instance.views_count = kwargs['views_count']
				if ("views" in kwargs): db_meta_instance.views = kwargs['views']
			#
		#
	#

	def delete(self):
	#
		"""
Deletes this entry from the database.

:return: (bool) True on success
:since:  v0.1.00
		"""

		_return = False

		with self:
		#
			self._database.begin()

			try:
			#
				db_meta_id = self.local.db_instance.id_object
				db_meta_instance = self.local.db_instance.rel_meta

				if (self.local.db_instance.rel_parent != None): DataLinker(self.local.db_instance.rel_parent).object_remove(self)

				_return = Instance.delete(self)

				if (
					_return and
					db_meta_instance != None and
					db_meta_instance.objects < 1 and
					self._database.query(sql_count(_DbDataLinker.id)).filter(_DbDataLinker.id_parent == db_meta_id).scalar() < 2
				): self._database.delete(db_meta_instance)

				if (_return): self._database.commit()
				else: self._database.rollback()
			#
			except Exception:
			#
				self._database.rollback()
				raise
			#
		#

		return _return
	#

	get_id = Instance._wrap_getter("id")
	"""
Returns the ID of this instance.

:return: (str) DataLinker ID; None if undefined
:since:  v0.1.00
	"""

	get_linkertype = Instance._wrap_getter("linkertype")
	"""
Returns the type of this instance.

:return: (str) DataLinker ID; None if undefined
:since:  v0.1.00
	"""

	def get_objects(self, offset = 0, limit = -1):
	#
		"""
Returns the children objects of this instance.

:return: (list) DataLinker children instances
:since:  v0.1.00
		"""

		with self:
		#
			db_query = self.local.db_instance.rel_children
			if (offset > 0): db_query = db_query.offset(offset)
			if (limit > 0): db_query = db_query.limit(limit)

			return DataLinker.buffered_iterator(_DbDataLinker, self._database.execute(db_query), DataLinker)
		#
	#

	get_objects_count = Instance._wrap_getter("objects")
	"""
Returns the number of objects of this instance.

:return: (str) DataLinker ID; None if undefined
:since:  v0.1.00
	"""

	def _insert(self):
	#
		"""
Insert the instance into the database.

:since: v0.1.00
		"""

		with self:
		#
			Instance._insert(self)
			db_meta_instance = self.local.db_instance.rel_meta

			if (db_meta_instance != None and db_meta_instance.tag != None):
			#
				with self._database.no_autoflush: self._validate_unique_tag(tag)
			#
		#
	#

	def is_reloadable(self):
	#
		"""
Returns true if the instance can be reloaded automatically in another
thread.

:return: (bool) True if reloadable
:since:  v0.1.00
		"""

		_return = True

		if (self.db_id == None):
		#
			# Value could be set in another thread so check again
			with self.lock: _return = (self.db_id != None)
		#

		return _return
	#

	def load_parent(self):
	#
		"""
Load the parent instance.

:return: (object) Parent DataLinker instance
:since:  v0.1.00
		"""

		with self:
		#
			_return = (None if (self.local.db_instance.rel_parent == None) else DataLinker(self.local.db_instance.rel_parent))
			if (_return == None and self.local.db_instance.rel_main != None): _return = DataLinker(self.local.db_instance.rel_main)
		#

		return _return
	#

	def object_add(self, child):
	#
		"""
Add the given child.

:param child: DataLinker instance

:since: v0.1.00
		"""

		if (isinstance(child, DataLinker)):
		#
			with self:
			#
				child_data = child.data_get("id")

				if (child_data['id'] != self.local.db_instance.id):
				#
					self.local.db_instance.rel_children.append(child._get_db_instance())
					child.data_set(id_main = self.local.db_instance.id_main)

					self.data_set(objects = "++")
				#
			#
		#
	#

	def object_remove(self, child):
	#
		"""
Remove the given child.

:param child: DataLinker instance

:since: v0.1.00
		"""

		if (isinstance(child, DataLinker)):
		#
			with self:
			#
				self.local.db_instance.rel_children.remove(child._get_db_instance())
				child.data_set(id_main = None)

				self.data_set(objects = "--")
			#
		#
	#

	def _reload(self):
	#
		"""
Implementation of the reloading SQLalchemy database instance logic.

:since: v0.1.00
		"""

		with self.lock:
		#
			if (self.local.db_instance == None):
			#
				if (self.db_id == None): raise IOException("Database instance is not reloadable.")
				else: self.local.db_instance = self._database.query(_DbDataLinker).filter(_DbDataLinker.id == self.db_id).first()
			#
			else: Instance._reload(self)
		#
	#

	def _validate_unique_tag(self, tag):
	#
		"""
Validates the given tag to be unique in the current main context.

:param tag: Tag to be checked

:since: v0.1.00
		"""

		if (
			self._database.query(sql_count(_DbDataLinker.id)).join(_DbDataLinkerMeta, (_DbDataLinker.id_object == _DbDataLinkerMeta.id)).filter(
				_DbDataLinker.id_main == self.local.db_instance.id_main, _DbDataLinkerMeta.tag == tag
			).scalar() > 0
		): raise ValueException("Tag can't be used twice in the same context")
	#

	@staticmethod
	def load_tag(tag, id_main):
	#
		with Connection.get_instance() as database: db_instance = database.query(_DbDataLinker).join(_DbDataLinkerMeta).filter(_DbDataLinkerMeta.tag == tag, _DbDataLinker.id_main == id_main).first()
		if (db_instance == None): raise ValueException("DataLinker tag '{0}' not found".format(tag))
		return DataLinker(db_instance)
	#

	@staticmethod
	def load_id(_id):
	#
		with Connection.get_instance() as database: db_instance = database.query(_DbDataLinker).filter(_DbDataLinker.id == _id).first()
		if (db_instance == None): raise ValueException("DataLinker ID '{0}' is invalid".format(_id))
		return DataLinker(db_instance)
	#
#

##j## EOF