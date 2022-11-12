"""
Copyright 2020 SCOUT
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations
from . import *
from bs4 import BeautifulSoup
import structlog
logger = structlog.getLogger()
# Types
T = TypeVar("T")


class Description(NamedTuple):
    """
    :param [name]: Column name
    :param [type_code]: The column data type
    """

    name: str
    type_code: str


from sys import path
from pathlib import Path

path.append(str(Path(__file__).parent)[2:])
clr.AddReference("Microsoft.AnalysisServices.AdomdClient")
from Microsoft.AnalysisServices.AdomdClient import AdomdConnection, AdomdCommand  # type: ignore

from ._type_code import adomd_type_map, convert


class Cursor:
    def __init__(self, connection: AdomdConnection):
        self._conn = connection
        self._description: List[Description] = []

    def close(self) -> None:
        """
        Closes the cursor
        """
        if self.is_closed:
            return
        self._reader.Close()

    def executeXML(self, query: str) -> BeautifulSoup:
        """
        Executes a query against the data source
        :params [query]: The query to be executed
        """
        logger.debug("executeXML query")
        self._cmd = AdomdCommand(query, self._conn)
        self._reader = self._cmd.ExecuteXmlReader()
        logger.debug("reading query")
        lines = [self._reader.ReadOuterXml()]
        while lines[-1] != "":
            lines.append(self._reader.ReadOuterXml())
        return BeautifulSoup("".join(lines), "xml")

    def executeXMLNonQuery(self, query: str, transaction: bool=True) -> None:
        logger.debug("executeXMLNonQuery")
        transaction = self._conn.BeginTransaction()
        self._cmd = AdomdCommand(query, self._conn)
        self._reader = self._cmd.ExecuteXmlReader()
        transaction.Commit()

    def execute(self, query: str) -> Cursor:
        """
        Executes a query against the data source
        :params [query]: The query to be executed
        """
        logger.debug("execute query")
        self._cmd = AdomdCommand(query, self._conn)
        self._reader = self._cmd.ExecuteReader()
        self._field_count = self._reader.FieldCount

        logger.debug("reading query")
        for i in range(self._field_count):
            self._description.append(
                Description(
                    self._reader.GetName(i),
                    adomd_type_map[self._reader.GetFieldType(i).ToString()].type_name,
                )
            )
        return self

    def executeNonQuery(self, command: str) -> Cursor:
        """
        Executes a Analysis Services Command against the database

        :params [command]: The command to be executed
        """
        self._cmd = AdomdCommand(command, self._conn)
        self._reader = self._cmd.ExecuteNonQuery()

        return self

    def fetchone(self) -> Iterator[Tuple[T, ...]]:
        """
        Fetches the current line from the last executed query
        """
        while self._reader.Read():
            yield tuple(
                convert(
                    self._reader.GetFieldType(i).ToString(),
                    self._reader[i],
                    adomd_type_map,
                )
                for i in range(self._field_count)
            )

    def fetchmany(self, size=1) -> List[Tuple[T, ...]]:
        """
        Fetches one or more lines from the last executed query
        :params [size]: The number of rows to fetch.
                        If the size parameter exceeds the number of rows returned from the last executed query then fetchmany will return all rows from that query.
        """
        l: List[Tuple[T, ...]] = []
        try:
            for i in range(size):
                l.append(next(self.fetchone()))
        except StopIteration:
            pass
        return l

    def fetchall(self) -> List[Tuple[T, ...]]:
        """
        Fetches all the rows from the last executed query
        """
        # mypy issues with list comprehension :-(
        return [i for i in self.fetchone()]  # type: ignore

    @property
    def is_closed(self) -> bool:
        try:
            state = self._reader.IsClosed
        except AttributeError:
            return True
        return state

    @property
    def description(self) -> List[Description]:
        return self._description

    def __enter__(self) -> Cursor:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


class Pyadomd:
    def __init__(self, conn_str: str):
        self.conn = AdomdConnection()
        self.conn.ConnectionString = conn_str

    def close(self) -> None:
        """
        Closes the connection
        """
        self.conn.Close()

    def open(self) -> None:
        """
        Opens the connection
        """
        self.conn.Open()

    def cursor(self) -> Cursor:
        """
        Creates a cursor object
        """
        c = Cursor(self.conn)
        return c

    @property
    def state(self) -> int:
        """
        1 = Open
        0 = Closed
        """
        return self.conn.State

    def __enter__(self) -> Pyadomd:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
