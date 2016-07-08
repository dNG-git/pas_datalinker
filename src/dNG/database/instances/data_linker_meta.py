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

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BOOLEAN, BIGINT, SMALLINT, VARCHAR

from dNG.database.types.date_time import DateTime

from .abstract import Abstract

class DataLinkerMeta(Abstract):
#
	"""
SQLAlchemy database instance for the metadata of a DataLinker entry.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_datalinker_meta".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_schema_version = 1
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), ForeignKey("{0}_datalinker.id".format(Abstract.get_table_prefix())), primary_key = True)
	"""
datalinker_meta.id
	"""
	sub_entries = Column(BIGINT, server_default = "0", nullable = False)
	"""
datalinker_meta.sub_entries
	"""
	sub_entries_type = Column(SMALLINT, server_default = "0", nullable = False)
	"""
datalinker_meta.sub_entries_type
	"""
	time_sortable = Column(DateTime, default = 0, index = True, nullable = False)
	"""
datalinker_meta.time_sortable
	"""
	symbol = Column(VARCHAR(255), server_default = "", nullable = False)
	"""
datalinker_meta.symbol
	"""
	title = Column(VARCHAR(255), server_default = "", index = True, nullable = False)
	"""
datalinker_meta.title
	"""
	tag = Column(VARCHAR(255), server_default = "", index = True, nullable = False)
	"""
datalinker_meta.tag
	"""
	views_count = Column(BOOLEAN, server_default = "0", nullable = False)
	"""
datalinker_meta.views_count
	"""
	views = Column(BIGINT, server_default = "0", index = True, nullable = False)
	"""
datalinker_meta.views
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(DataLinkerMeta)

:since: v0.2.00
		"""

		Abstract.__init__(self, *args, **kwargs)
		if (self.sub_entries is None): self.sub_entries = 0
		if (self.views is None): self.views = 0
	#
#

##j## EOF