# -*- coding: utf-8 -*-

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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from sqlalchemy.orm import backref, foreign, relationship, remote
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BIGINT, VARCHAR
from uuid import uuid4 as uuid

from dNG.database.autoloading_polymorphic_map import AutoloadingPolymorphicMap

from .abstract import Abstract
from .data_linker_meta import DataLinkerMeta

class DataLinker(Abstract):
    """
SQLAlchemy database instance for DataLinker.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    # pylint: disable=invalid-name

    __tablename__ = "{0}_datalinker".format(Abstract.get_table_prefix())
    """
SQLAlchemy table name
    """
    db_instance_class = "dNG.data.DataLinker"
    """
Encapsulating SQLAlchemy database instance class name
    """
    db_schema_version = 1
    """
Database schema version
    """

    id = Column(VARCHAR(32), primary_key = True)
    """
datalinker.id
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
    identity = Column(VARCHAR(100), index = True, nullable = False)
    """
datalinker.identity
    """
    position = Column(BIGINT, server_default = "0", nullable = False)
    """
datalinker.position
    """

    __mapper_args__ = { "polymorphic_identity": "DataLinker",
                        "_polymorphic_map": AutoloadingPolymorphicMap(),
                        "polymorphic_on": identity
                      }
    """
sqlalchemy.org: Other options are passed to mapper() using the
__mapper_args__ class variable.
    """

    rel_children = relationship("DataLinker", backref = backref("rel_parent", remote_side = [ id ]), lazy = "dynamic")
    """
Relation to DataLinker children (backref is set as "rel_parent")
    """
    rel_main = relationship("DataLinker", post_update = True, primaryjoin = (foreign(id_main) == remote(id)), uselist = False)
    """
Relation to DataLinker main entry
    """
    rel_meta = relationship(DataLinkerMeta, lazy = "joined", uselist = False)
    """
Relation to DataLinkerMeta (backref is set as "rel_linker")
    """

    def __init__(self, *args, **kwargs):
        """
Constructor __init__(DataLinker)

:since: v0.2.00
        """

        Abstract.__init__(self, *args, **kwargs)

        if (self.id is None): self.id = uuid().hex
        if (self.position is None): self.position = 0
    #

    @staticmethod
    def _get_db_column(cls, attribute):
        """
Returns the SQLAlchemy column for the requested attribute of the given
class.

:param cls: Python class
:param attribute: Requested attribute

:return: (object) SQLAlchemy column
:since:  v0.2.00
        """

        return (DataLinker.id
                if (attribute == "id") else
                Abstract._get_db_column(cls, attribute)
               )
    #

    @staticmethod
    def _get_unknown_db_column(cls, attribute):
        """
Returns the SQLAlchemy column for the requested attribute not defined for
the given entity class.

:param cls: Python class
:param attribute: Requested attribute

:return: (object) SQLAlchemy column
:since:  v0.2.00
        """

        return (getattr(DataLinkerMeta, attribute)
                if (hasattr(DataLinkerMeta, attribute)) else
                Abstract._get_unknown_db_column(cls, attribute)
               )
    #
#
