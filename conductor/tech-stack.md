# Tech Stack

## Core Technologies
- **Programming Language**: Python 3.12 (as detected in the current environment)
- **Framework**: Odoo (Version 17.0)
- **Database Backend**: PostgreSQL (Standard Odoo backend)

## Odoo Dependencies
- **`base`**: Core Odoo functionality.
- **`mail`**: Messaging, internal communications, and automated email notifications.
- **`hr`**: Human Resources integration for managing employee-asset relationships.

## Security Maintenance
- **Dependency Guard**: Critical libraries (cryptography, gevent, Jinja2, etc.) are actively updated to mitigate known vulnerabilities (RCE, DoS).

## Frontend & Templating
- **XML Views**: Standard Odoo XML-based view definitions (Form, List, Kanban).
- **QWeb Templates**: Standard Odoo QWeb engine for server-side rendering.
- **Standard UI Components**: Relying on Odoo's native JavaScript framework (OWL/Legacy as per Odoo 15).
