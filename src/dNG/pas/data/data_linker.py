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

			if ("subs" in kwargs or "objects" in kwargs or "time_sortable" in kwargs or "symbol" in kwargs or "title" in kwargs or "datasubs_type" in kwargs or "datasubs_hide" in kwargs or "datasubs_new" in kwargs or "views_count" in kwargs or "views" in kwargs):
			#
				if (self.local.db_instance.rel_meta == None):
				#
					self.local.db_instance.rel_meta = _DbDataLinkerMeta()
					self.local.db_instance.rel_meta.id = self.local.db_instance.id_object
					db_meta_instance = self.local.db_instance.rel_meta
				#
				else: db_meta_instance = self.local.db_instance.rel_meta

				if ("subs" in kwargs):
				#
					if (kwargs['subs'] == "++"): db_meta_instance.subs = db_meta_instance.subs + 1
					elif (kwargs['subs'] == "--"):
					#
						if (db_meta_instance.subs > 0): db_meta_instance.subs = db_meta_instance.subs - 1
					#
					else: db_meta_instance.subs = kwargs['subs']
				#

				if ("objects" in kwargs):
				#
					if (kwargs['objects'] == "++"): db_meta_instance.objects = db_meta_instance.objects + 1
					elif (kwargs['objects'] == "--"):
					#
						if (db_meta_instance.objects > 0): db_meta_instance.objects = db_meta_instance.objects - 1
					#
					else: db_meta_instance.objects = kwargs['objects']
				#

				if ("time_sortable" in kwargs): db_meta_instance.time_sortable = int(kwargs['time_sortable'])
				if ("symbol" in kwargs): db_meta_instance.symbol = Binary.utf8(kwargs['symbol'])
				if ("title" in kwargs): db_meta_instance.title = Binary.utf8(kwargs['title'])
				if ("hashtag" in kwargs and "id_main" in kwargs and kwargs['hashtag'] != None and len(kwargs['hashtag']) > 0): db_meta_instance.hashtag = Binary.utf8(kwargs['hashtag'])
				if ("datasubs_type" in kwargs): db_meta_instance.datasubs_type = kwargs['datasubs_type']
				if ("datasubs_hide" in kwargs): db_meta_instance.datasubs_hide = kwargs['datasubs_hide']
				if ("datasubs_new" in kwargs): db_meta_instance.datasubs_new = kwargs['datasubs_new']
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

			if (db_meta_instance != None and db_meta_instance.hashtag != None):
			#
				if (
					self._database.query(sql_count(_DbDataLinker.id)).join(_DbDataLinkerMeta).filter(
						_DbDataLinker.id_main == self.local.db_instance.id_main, _DbDataLinkerMeta.hashtag == db_meta_instance.hashtag
					).scalar() > 0
				): raise ValueException("Hashtag can't be used twice in the same context")
			#
		#
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

	@staticmethod
	def load_hashtag(hashtag, id_main):
	#
		with Connection.get_instance() as database: db_instance = database.query(_DbDataLinker).join(_DbDataLinkerMeta).filter(_DbDataLinkerMeta.hashtag == hashtag, _DbDataLinker.id_main == id_main).first()
		if (db_instance == None): raise ValueException("DataLinker hashtag '{0}' not found".format(hashtag))
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