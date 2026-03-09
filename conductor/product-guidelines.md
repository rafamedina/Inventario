# Product Guidelines

## Prose Style

- **User-friendly & Descriptive:** The documentation should be clear and accessible to all organizational roles, avoiding overly technical jargon where possible.
- **Language:** Spanish is the preferred language for all project-related documentation and user-facing guidelines to maintain consistency with the existing repository.

## UI/UX Principles

- **Strict Odoo HIG:** All user interface elements must strictly adhere to the Odoo Human Interface Guidelines (HIG) for Odoo 18. This ensures a seamless and familiar experience for users already accustomed to the Odoo ecosystem.
- **Consistency:** Use standard Odoo views (tree, form, search) and components to maintain a unified look and feel.

## Communication & Feedback

- **Odoo Standard Notifications:** Utilize the built-in Odoo notification system (sticky and non-sticky) to inform users of successful actions or minor warnings.
- **Detailed Backend Logging:** For critical asset updates (creation, deletion, or major field changes), implement robust backend logging to provide a clear audit trail for administrative review.

## Architecture & Code

- **Modular Structure:** Maintain the Odoo-standard directory structure (models, views, security, data) for clarity and ease of maintenance.
- **Dependency Management:** Explicitly declare all module dependencies in the `__manifest__.py` file.
