# pylint: disable=unused-argument,invalid-name,line-too-long


from typing import Generator

from sqlalchemy import text as sql_text
from sqlalchemy.sql.elements import TextClause

# https://github.com/olirice/alembic_utils/blob/d5d69519159fdabb2cac7cc10f748415f9fe6537/src/alembic_utils/pg_extension.py#L31

class PGExtension:
    """A PostgreSQL Extension compatible with `alembic revision --autogenerate`

    **Parameters:**

    * **schema** - *str*: A SQL schema name
    * **signature** - *str*: A PostgreSQL extension's name
    """

    # type_ = "extension"
    operation_name = 'create_extension'
    requires_connection = True

    def __init__(self, schema: str, signature: str, version: str = None, if_not_exists=True, cascade=False):
        self.schema: str = schema
        self.signature: str = signature
        # Include schema in definition since extensions can only exist once per
        # database and we want to detect schema changes and emit alter schema
        self.definition: str = f"{self.__class__.__name__}: {self.schema} {self.signature}"
        self.version: str = version
        self.if_not_exists = if_not_exists
        self.cascade = cascade

    def to_sql_statement_create(self) -> TextClause:
        """Generates a SQL "create extension" statement"""
        return sql_text(f'CREATE EXTENSION "{self.signature}" WITH SCHEMA {self.schema};')

    def to_sql_statement_drop(self, cascade=False) -> TextClause:
        """Generates a SQL "drop extension" statement"""
        cascade = "CASCADE" if cascade else ""
        return sql_text(f'DROP EXTENSION "{self.signature}" {cascade}')

    def to_sql_statement_create_or_replace(self) -> Generator[TextClause, None, None]:
        """Generates SQL equivalent to "create or replace" statement"""
        raise NotImplementedError()

    @property
    def identity(self) -> str:
        """A string that consistently and globally identifies an extension"""
        # Extensions may only be installed once per db, schema is not a
        # component of identity
        return f"{self.__class__.__name__}: {self.signature}"

    def render_self_for_migration(self, omit_definition=False) -> str:
        """Render a string that is valid python code to reconstruct self in a migration"""
        var_name = self.to_variable_name()
        class_name = self.__class__.__name__

        return f"""{var_name} = {class_name}(
    schema="{self.schema}",
    signature="{self.signature}"
)\n"""

    @classmethod
    def from_database(cls, sess, schema):
        """Get a list of all extensions defined in the db"""
        sql = sql_text(
            f"""
        select
            np.nspname schema_name,
            ext.extname extension_name
        from
            pg_extension ext
            join pg_namespace np
                on ext.extnamespace = np.oid
        where
            np.nspname not in ('pg_catalog')
            and np.nspname like :schema;
        """
        )
        rows = sess.execute(sql, {"schema": schema}).fetchall()
        db_exts = [cls(x[0], x[1]) for x in rows]
        return db_exts

    @classmethod
    def create_extension(cls, signature: str, schema: str = None, version=None, if_not_exists=True, cascade=False):
        """
        Creates a custom operation to create a PostgreSQL extension.

        Args:
            signature (str): The name of the extension.
            schema (str, optional): The schema where the extension should be created. Defaults to None.
            version (str, optional): The version of the extension. Defaults to None.
            if_not_exists (bool, optional): Whether to create the extension only if it does not exist. Defaults to True.
            cascade (bool, optional): Whether to cascade the extension creation to dependent objects. Defaults to False.

        Returns:
            OpMessage: A custom operation instance.
        """
        return cls(signature, schema, version, if_not_exists, cascade)

    def _execute(self, connection):
        """Executes the operation using the database connection."""
        sql = f"CREATE EXTENSION"
        if self.if_not_exists:
            sql += " IF NOT EXISTS"
        sql += f" {self.signature}"
        if self.schema:
            sql += f" SCHEMA {self.schema}"
        if self.version:
            sql += f" VERSION {self.version}"
        if self.cascade:
            sql += " CASCADE"
        
        with connection.begin():
            connection.execute(sql)
