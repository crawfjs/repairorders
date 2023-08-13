#### Overview

This projects reads individual repair order events stored as XML within a folder on a filesystem and coerces the data into a normalized structure within a generated database. Each "run" of the project is assigned a unique identifier and the identifier is used for both logging as well as the generated database.

#### Setup

- If you are using a virutal environment, run it prior to setup.
- Run `pip install -r requirements.txt`

#### Running

The project includes a Makefile, so you can type `make` within the root of the project and have the options displayed.

- `make docs`: Generates documentation for the project and serves it on http://localhost:1234"
- `make run`: Runs the project against the data folder included in the project. To run against another folder, just update the _.env_ file.
- `make test`: Runs the unit tests within the project. All generated data will automatically be cleaned up, but is safe to run repeatedly.

#### Logging

Logging within the system is abstracted via the repair orders logging service. Currently, it using the python Logger, however it is configurable via audit_logging_config.ini.
The root logger is also configured there, but our special RepairOrders logger can configured to store in a separate file, to stdout, or both. Each run generates a unique "run key", so that each run may be audited.
