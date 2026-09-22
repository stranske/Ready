fix(dashboard): close DB connection on missing table and query errors (#1697)

Closes #1697. Adds parameterized connection-close regression coverage for load_delta() missing-table and exception paths.
