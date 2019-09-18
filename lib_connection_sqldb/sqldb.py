"""Relational database utilities to be used in every fx project"""

import logging
from . import config
from .exceptions import QueryEmptyResult
from lib_formatter_logger import log
from sqlalchemy import text
from sqlalchemy.event import listen, remove
from sqlalchemy.engine import create_engine, url


class MySQL(object):

    def __init__(self, conn=config.MYSQL_DATABASE_CONN):
        """Constructor method

        Keyword Arguments:
            conn {dict} -- A dict containing the database connection info (default: {config.MYSQL_DATABASE_CONN})
        """

        self.conn = conn
        self.logger = log.getLogger()
        _url = str(url.URL(**conn)) + "?charset=utf8"
        self.engine = create_engine(url.URL(**conn))
        self.query = None
        if self.logger.isEnabledFor(logging.DEBUG):
            listen(self.engine, "do_execute", self.__receive_do_execute)


    def __prepare_query(self, query, params):
        """Internal function to construct a TextClause clause, representing a textual SQL string directly.

        Arguments:
            query {str} -- The query
            params {dict} -- The params to be passed to the query

        Returns:
            [sqlalchemy.sql.expression.TextClause] -- A TextClause clause
        """
        try:
            q = text(query)
            if params:
                q = q.bindparams(**params)
        except:
            with self.logger.extra(query=query):
                self.logger.exception("Failed to prepare query with params {}".format(params))
            raise

        return q

    def execute(self, query, params, get_results=True, check_for_empty_result=True):
        """Execute the query

        Arguments:
            query {str} -- The query
            params {dict} -- The params to be passed to the query

        Keyword Arguments:
            get_results {bool} -- Hold result into 'results' attribute? (default: {True})
            check_for_empty_result {bool} -- Check for an empty result? If True, and the result is empty,
                                             a QueryEmptyResult exception will be raised (default: {True})
        """

        with self.engine.connect() as connection:
            try:
                f_query = self.__prepare_query(query, params)
                self._result = connection.execute(f_query)
            except:
                self.logger.exception("Failed to execute query")
                raise

            if get_results:
                self.__get_results(check_for_empty_result=check_for_empty_result)

    def open_session(self):
        """open the session

        Return Transaction and connectio:
            
        Example: Use
        trans,conn = openSession()

        try
            ALL inserts select all what u want do early trans.commit
            sessionExecute(X,connection)
            sessionExecute(Y,connection)
            sessionExecute(z,connection)
            trans.commit() #  transaction is committed here
        except:            
            trans.rollback() # this rolls back the transaction unconditionally
            raise


        """
        connection = self.engine.connect()
        trans = connection.begin() # open a transaction
        
        return trans, connection

    def session_execute(self, query, params, connection, get_results=True, check_for_empty_result=True):
        """Execute the query

        Arguments:
            query {str} -- The query
            params {dict} -- The params to be passed to the query

        Keyword Arguments:
            get_results {bool} -- Hold result into 'results' attribute? (default: {True})
            check_for_empty_result {bool} -- Check for an empty result? If True, and the result is empty,
                                             a QueryEmptyResult exception will be raised (default: {True})

        Connection:
            Connection for make cascade methods

        conn = .sessionExecute() when pass connection get same trasaction with someone raise a rollback all connection rollback

        """
        
        try:
            trans = connection.begin()
            f_query = self.__prepare_query(query, params)
            self._result = connection.execute(f_query)
            trans.commit() # transaction is not committed yet
        except:
            self.logger.exception("Failed to execute query")
            trans.rollback() # this rolls back the transaction unconditionally
            raise

        if get_results:
            self.__get_results(check_for_empty_result=check_for_empty_result)

        return connection

    def __get_results(self, check_for_empty_result):
        """Internal function to get and optionally check an empty query result
        
        Arguments:
            check_for_empty_result {bool} -- Check for an empty result?
        
        Raises:
            QueryEmptyResult -- If check_for_empty_result == True and the result is empty
        """

        self.result = []
        for row in self._result:
            row_dict = dict(row)
            self.result.append(row_dict.copy())

        if check_for_empty_result:
            if not self.result:
                with self.logger.extra(query=self.query):
                    self.logger.exception("Query returned an empty result")
                    raise QueryEmptyResult()


    def __receive_do_execute(self, cursor, statement, parameters, context):
        """Internal function used to put debug information about the executed query into logs. It must have
        the same signature of sqlalchemy.engine.default.DefaultDialect.do_execute class.
        Details:

        http://docs.sqlalchemy.org/en/latest/core/internals.html#sqlalchemy.engine.default.DefaultDialect.do_execute
        https://stackoverflow.com/a/37845168
        """

        try:
            self.query = cursor.mogrify(statement, parameters)
        except:
            pass
            
        return False
