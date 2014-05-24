# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.database.instances.DataLinkerMeta
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

from sqlalchemy import BOOLEAN, BIGINT, Column, SMALLINT, VARCHAR

from dNG.pas.database.types.date_time import DateTime
from .abstract import Abstract

class DataLinkerMeta(Abstract):
#
	"""
SQLAlchemy database instance for the metadata of a DataLinker entry.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_datalinker_meta".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""

	id = Column(VARCHAR(32), primary_key = True)
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

:since: v0.1.00
		"""

		Abstract.__init__(self, *args, **kwargs)

		if (self.sub_entries == None): self.sub_entries = 0
	#
#

##j## EOF