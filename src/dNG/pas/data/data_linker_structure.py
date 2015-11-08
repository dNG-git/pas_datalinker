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

from copy import copy

from dNG.pas.runtime.value_exception import ValueException

class DataLinkerStructure(object):
#
	"""
The "DataLinkerStructure" represents a hierarchical structure of DataLinker
entries.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(DataLinkerStructure)

:param db_instance: Encapsulated SQLAlchemy database instance

:since: v0.1.00
		"""

		self.structure_ids = { }
		"""
Hierarchical structure of IDs and their children
		"""
		self.structure = None
		"""
Hierarchical structure of IDs and their children
		"""
		self.entry_ids = [ ]
		"""
List holding the entry IDs
		"""
		self.entries = [ ]
		"""
List holding the entries
		"""
	#

	def add(self, entry):
	#
		"""
Add the given entry to this structure.

:param entry: DataLinker entry

:since: v0.1.00
		"""

		if (not entry.is_data_attribute_none("id", "id_main")):
		#
			entry_id = entry.get_id()

			self.entry_ids.append(entry_id)
			self.entries.append(entry)

			self.structure = None
		#
	#

	def _analyze_entries(self):
	#
		"""
Analyzes all entries to build the hierarchical structure.

:since: v0.1.00
		"""

		self.structure = { }
		self.structure_ids = { }
		structure_entries = { }
		structure_main_id = None
		unmatched_entries = { }

		for entry in self.entries:
		#
			entry_data = entry.get_data_attributes("id", "id_parent", "id_main")
			if (structure_main_id is None): structure_main_id = entry_data['id_main']

			entry_id = entry_data['id']
			entry_parent_id = entry_data['id_parent']

			if (entry_id == structure_main_id):
			#
				structure_entry = { "entry": entry,
				                    "entry_id": entry_id,
				                    "children": [ ]
				                  }

				self.structure = structure_entry
				structure_entries[entry_id] = structure_entry
			#
			elif (entry_parent_id in structure_entries):
			#
				structure_entry = { "entry": entry,
				                    "entry_id": entry_id,
				                    "children": [ ]
				                  }

				structure_entries[entry_parent_id]['children'].append(structure_entry)
				structure_entries[entry_id] = structure_entry

				if (entry_id in unmatched_entries):
				#
					structure_entry['children'] = unmatched_entries[entry_id]
					del(unmatched_entries[entry_id])
				#
			#
			else:
			#
				structure_entry = { "entry": entry,
				                    "entry_id": entry_id,
				                    "entry_parent_id": entry_parent_id,
				                    "children": [ ]
				                  }

				unmatched_entries[entry_id] = structure_entry

				if (entry_parent_id in unmatched_entries):
				#
					unmatched_entries[entry_parent_id]['children'].append(structure_entry)
				#
			#
		#

		for unmatched_id in unmatched_entries:
		#
			unmatched_entry = unmatched_entries[unmatched_id]

			if (unmatched_entry['entry_parent_id'] in structure_entries):
			#
				structure_entries[unmatched_entry['entry_parent_id']]['children'].append(unmatched_entry)
				structure_entries[unmatched_entry['entry_id']] = unmatched_entry
			#
		#

		self._analyze_entries_walker(self.structure, [ ])
	#

	def _analyze_entries_walker(self, structure_dict, structure_ids):
	#
		"""
Analyzes all hierarchical structure to build the flat, reversed ID list.

:since: v0.1.00
		"""

		if (len(structure_dict) > 0):
		#
			ids = (structure_ids.copy() if (hasattr(structure_ids, "copy")) else copy(structure_ids))
			ids.append(structure_dict['entry_id'])

			self.structure_ids[structure_dict['entry_id']] = ids
			for structure_child in structure_dict['children']: self._analyze_entries_walker(structure_child, ids)
		#
	#

	def get_structure(self, _id):
	#
		"""
Returns a hierarchical dict containing the matched entry and a list of
children dictionaries.

:return: (dict) Hierarchical dict
:since:  v0.1.00
		"""

		_return = { }

		if (self.structure is None): self._analyze_entries()
		if (_id not in self.entry_ids): raise ValueException("Given ID is not a child of this structure")

		structure_ids = self.structure_ids.get(_id)
		if (structure_ids is None): raise ValueException("Given ID is not a valid structure entry")

		structure_ptr = self.structure

		for structure_id in structure_ids:
		#
			if (structure_ptr['entry_id'] == structure_id): continue
			else:
			#
				is_child_found = False

				for structure_child in structure_ptr['children']:
				#
					if (structure_child['entry_id'] == structure_id):
					#
						is_child_found = True
						structure_ptr = structure_child
						break
					#
				#

				if (not is_child_found): raise ValueException("Given ID is not a valid structure entry")
			#
		#

		_return = structure_ptr
		return _return
	#

	def get_structure_list(self, _id):
	#
		"""
Returns a list of the matched entry and its children entries.

:return: (list) List of entries
:since:  v0.1.00
		"""

		return self._get_structure_list_walker(self.get_structure(_id))
	#

	def _get_structure_list_walker(self, structure_dict):
	#
		"""
Returns a flat list for the hierarchical dict entry and its children.

:return: (list) List of entries
:since:  v0.1.00
		"""

		_return = [ ]

		if (len(structure_dict) > 0):
		#
			_return.append(structure_dict['entry'])
			for structure_child in structure_dict['children']: _return += self._get_structure_list_walker(structure_child)
		#

		return _return
	#
#

##j## EOF