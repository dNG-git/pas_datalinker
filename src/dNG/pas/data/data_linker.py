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

from dNG.pas.database.instance import Instance
from dNG.pas.database.instances.data_linker import DataLinker as DataLinkerInstance
from dNG.pas.database.instances.data_linker_meta import DataLinkerMeta as DataLinkerMetaInstance
from .binary import Binary
from .traced_exception import TracedException

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

	def data_get(self, *args):
	#
		"""
Return the requested attributes.

:return: (dict) Values for the requested attributes
:since:  v0.1.00
		"""

		_return = { }

		with self:
		#
			for attribute in args:
			#
				if (attribute == "title" and self.local.db_instance.title_alt != ""): _return['title'] = self.local.db_instance.title_alt
				elif (attribute == "title_orig" and self.local.db_instance.rel_meta != None): _return['title_orig'] = self.local.db_instance.rel_meta.title
				elif (hasattr(self.local.db_instance, attribute)): _return[attribute] = getattr(self.local.db_instance, attribute)
				elif (self.local.db_instance.rel_meta != None and hasattr(self.local.db_instance.rel_meta, attribute)): _return[attribute] = getattr(self.local.db_instance.rel_meta, attribute)
				else: _return[attribute] = None
			#
		#

		return _return
	#

	def data_set(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		if (self.local.db_instance == None): self.local.db_instance = DataLinkerInstance()

		with self:
		#
			if (self.id == None): self.id = self.local.db_instance.id

			if ("id_object" in kwargs): self.local.db_instance.id_object = kwargs['id_object']
			if ("id_parent" in kwargs): self.local.db_instance.id_parent = kwargs['id_parent']
			if ("id_main" in kwargs): self.local.db_instance.id_main = Binary.utf8(kwargs['id_main'])
			if ("id_site" in kwargs): self.local.db_instance.id_site = Binary.utf8(kwargs['id_site'])
			if ("type" in kwargs): self.local.db_instance.type = kwargs['type']
			if ("position" in kwargs): self.local.db_instance.position = kwargs['position']
			if ("title_alt" in kwargs): self.local.db_instance.title_alt = Binary.utf8(kwargs['title_alt'])

			if ("subs" in kwargs or "objects" in kwargs or "sorting_date" in kwargs or "symbol" in kwargs or "title" in kwargs or "datasubs_type" in kwargs or "datasubs_hide" in kwargs or "datasubs_new" in kwargs or "views_count" in kwargs or "views" in kwargs):
			#
				if (self.local.db_instance.rel_meta == None):
				#
					self.local.db_instance.rel_meta = DataLinkerMetaInstance()
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

				if ("sorting_date" in kwargs): db_meta_instance.sorting_date = kwargs['sorting_date']
				if ("symbol" in kwargs): db_meta_instance.symbol = Binary.utf8(kwargs['symbol'])
				if ("title" in kwargs): db_meta_instance.title = Binary.utf8(kwargs['title'])
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
					self._database.query(sql_count(DataLinkerInstance.id)).filter(DataLinkerInstance.id_parent == db_meta_id).scalar() < 2
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

	def load_parent(self):
	#
		"""
Load the parent instance.

:return: (object) Parent DataLinker instance
:since:  v0.1.00
		"""

		with self: _return = (None if (self.local.db_instance.rel_parent == None) else DataLinker(self.local.db_instance.rel_parent))
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

		with self.synchronized:
		#
			if (self.local.db_instance == None):
			#
				if (self.db_id == None): raise TracedException("Database instance is not reloadable.")
				else: self.local.db_instance = self._database.query(DataLinkerInstance).filter(DataLinkerInstance.id == self.db_id).first()
			#
			else: Instance._reload(self)
		#
	#
#

##j## EOF