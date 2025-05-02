# pylint: disable=unused-argument,invalid-name,line-too-long

from alembic.operations import MigrateOperation, Operations


# https://github.com/olirice/alembic_utils/blob/d5d69519159fdabb2cac7cc10f748415f9fe6537/src/alembic_utils/pg_extension.py#L31


class PgExtensionOp(MigrateOperation):
    """Base PgExtensionOp for Create and Drop statements.
    """

    def __init__(self, signature: str, schema: str, version: str = None, if_not_exists=True, cascade=False):
        self.signature: str = signature
        self.schema: str = schema
        self.version: str = version
        self.if_not_exists = if_not_exists
        self.cascade = cascade

class PgCreateExtensionOp(PgExtensionOp):
    """A PostgreSQL Extension compatible with `alembic revision --autogenerate`

    **Parameters:**

    * **schema** - *str*: A SQL schema name
    * **signature** - *str*: A PostgreSQL extension's name
    """

    operation_name = 'create_extension'

    @classmethod
    def create_extension(
            cls,
            operations: Operations,
            signature: str,
            schema: str = None,
            version=None,
            if_not_exists=True,
            cascade=False,
        ):
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
        op = cls(signature, schema, version, if_not_exists, cascade)
        return operations.invoke(op)

    def to_sql_statement_create(self) -> str:
        """Generates a SQL "create extension" statement"""
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
        
        return sql

class PgDropExtensionOp(PgExtensionOp):
    """A PostgreSQL Extension compatible with `alembic revision --autogenerate`

    **Parameters:**

    * **schema** - *str*: A SQL schema name
    * **signature** - *str*: A PostgreSQL extension's name
    """

    operation_name = 'drop_extension'

    @classmethod
    def drop_extension(
            cls,
            operations: Operations,
            signature: str,
            schema: str = None,
            version=None,
            if_not_exists=True,
            cascade=False,
        ):
        """
        Creates a custom operation to drop a PostgreSQL extension.

        Args:
            signature (str): The name of the extension.
            schema (str, optional): The schema where the extension should be created. Defaults to None.
            version (str, optional): The version of the extension. Defaults to None.
            if_not_exists (bool, optional): Whether to create the extension only if it does not exist. Defaults to True.
            cascade (bool, optional): Whether to cascade the extension creation to dependent objects. Defaults to False.

        Returns:
            OpMessage: A custom operation instance.
        """
        op = cls(signature, schema, version, if_not_exists, cascade)
        return operations.invoke(op)
    
    def to_sql_statement_drop(self) -> str:
        """Generates a SQL "drop extension" statement"""
        cascade = "CASCADE" if self.cascade else ""
        
        return f'DROP EXTENSION "{self.signature}" {cascade}'


def create_extension(operations: Operations, operation: PgCreateExtensionOp):
    operations.execute(operation.to_sql_statement_create())

def drop_extension(operations: Operations, operation: PgDropExtensionOp):
    operations.execute(operation.to_sql_statement_drop())


_operations_registered = False


def register_operations():
    global _operations_registered

    if not _operations_registered:
        Operations.register_operation(PgCreateExtensionOp.operation_name)(PgCreateExtensionOp)
        Operations.implementation_for(PgCreateExtensionOp)(create_extension)
        Operations.register_operation(PgDropExtensionOp.operation_name)(PgDropExtensionOp)
        Operations.implementation_for(PgDropExtensionOp)(drop_extension)
        _operations_registered = True
