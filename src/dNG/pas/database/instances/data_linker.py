# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.database.instances.DataLinker
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

from sqlalchemy import BIGINT, Column, ForeignKey, INT, VARCHAR
from sqlalchemy.orm import backref, foreign, relationship, remote
from uuid import uuid4 as uuid

from .abstract import Abstract
from .data_linker_meta import DataLinkerMeta

class DataLinker(Abstract):
#
	"""
SQLAlchemy database instance for DataLinker.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_datalinker".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.pas.data.DataLinker"
	"""
Encapsulating SQLAlchemy database instance class name
	"""

	id = Column(VARCHAR(32), primary_key = True)
	"""
datalinker.id
	"""
	id_object = Column(VARCHAR(32), index = True, nullable = False)
	"""
datalinker.id_object
	"""
	id_parent = Column(VARCHAR(32), ForeignKey(id), index = True)
	"""
datalinker.id_parent
	"""
	id_main = Column(VARCHAR(32), index = True)
	"""
datalinker.id_main
	"""
	id_site = Column(VARCHAR(20), index = True)
	"""
datalinker.id_site
	"""
	linkertype = Column(VARCHAR(100), index = True, nullable = False)
	"""
datalinker.linkertype
	"""
	type = Column(INT, server_default = "1", nullable = False)
	"""
datalinker.type
	"""
	position = Column(BIGINT, server_default = "0", nullable = False)
	"""
datalinker.position
	"""
	title_alt = Column(VARCHAR(255), server_default = "", index = True, nullable = False)
	"""
datalinker.title_alt
	"""

	__mapper_args__ = { "polymorphic_identity": "DataLinker", "polymorphic_on": linkertype }
	"""
sqlalchemy.org: Other options are passed to mapper() using the
                __mapper_args__ class variable.
	"""

	rel_children = relationship("DataLinker", backref = backref("rel_parent", remote_side = [ id ]), lazy = "dynamic")
	"""
Relation to DataLinker children (backref is set as "rel_parent")
	"""
	rel_main = relationship("DataLinker", primaryjoin = (foreign(id_main) == remote(id)), uselist = False)
	"""
Relation to DataLinker children (backref is set as "rel_parent")
	"""
	rel_meta = relationship(DataLinkerMeta, backref = "rel_linker", lazy = "joined", primaryjoin = (foreign(id_object) == remote(DataLinkerMeta.id)), uselist = False)
	"""
Relation to DataLinkerMeta (backref is set as "rel_linker")
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(DataLinker)

:since: v0.1.00
		"""

		Abstract.__init__(self, *args, **kwargs)

		if (self.id == None): self.id = uuid().hex
		if (self.id_object == None): self.id_object = self.id
	#
#

##j## EOF