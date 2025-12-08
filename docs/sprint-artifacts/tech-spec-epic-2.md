# Epic Technical Specification: Core Financial Management

Date: 2025-11-30
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This epic delivers the central, most critical functionality of the Excelence application: the ability for users to manage their finances. It encompasses the complete CRUD (Create, Read, Update, Delete) operations for both financial transactions (income and expenses) and the custom categories they belong to. By the end of this epic, users will be able to accurately record their financial activities, organize them meaningfully, and correct any mistakes. This directly addresses the core functional requirements FR003 (CRUD for Transactions) and FR004 (CRUD for Categories), transforming the application from a basic login system into a functional budgeting tool.

## Objectives and Scope

**In Scope:**

*   **Category Management:** Full CRUD functionality for user-defined categories (Create, View, Update, Delete).
*   **Transaction Management:** Full CRUD functionality for income and expense transactions.
*   **Backend API:** Creation of all necessary endpoints under `/api/v1/categories` and `/api/v1/transactions` to support these operations.
*   **Database Schema:** Implementation of the `categories` and `transactions` tables in the database, including the relationship between them.
*   **Frontend UI:**
    *   A dedicated settings page for managing categories.
    *   A modal form on the main dashboard for adding/editing transactions.
    *   A list or table view to display all past transactions.
*   **Real-time Updates:** Ensuring the UI immediately reflects any changes made to transactions or categories.

**Out of Scope:**

*   Dashboard summaries or calculations (e.g., total income/expenses). This is handled in Epic 3.
*   Visualizations or charts of financial data. This is handled in Epic 3.
*   Data export functionality. This is handled in Epic 3.
*   Any gamification features.

## System Architecture Alignment

This epic builds directly upon the foundation established in Epic 1 and adheres to the defined architecture. It will introduce new API endpoints (`/transactions`, `/categories`) and corresponding database models (`transactions`, `categories`) as anticipated in the project structure. The implementation will follow the established API naming conventions (plural nouns, kebab-case) and database naming conventions (plural, snake_case). The frontend will leverage the existing `api.ts` service for communication and Svelte's reactive stores to manage and display the lists of transactions and categories, ensuring a consistent state management approach. All new database tables will be related to the `users` table to ensure data ownership and security.

## Detailed Design

### Services and Modules

| Service/Module | Responsibility | Inputs/Outputs | Owner |
| :--- | :--- | :--- | :--- |
| **Backend: `transactions.py`** | Handles all CRUD operations for financial transactions. | **In:** Transaction data. **Out:** Transaction objects. | Backend |
| **Backend: `categories.py`** | Handles all CRUD operations for user-defined categories. | **In:** Category data. **Out:** Category objects. | Backend |
| **Backend: `schemas/`** | Defines Pydantic schemas for `Transaction` and `Category` data validation. | N/A | Backend |
| **Backend: `models/`** | Defines the `transactions` and `categories` database table models. | N/A | Backend |
| **Frontend: `routes/settings/categories`**| Provides the UI for managing categories. | User interactions. | Frontend |
| **Frontend: `components/.../TransactionForm.svelte`**| A reusable modal form component for creating and editing transactions. | **In:** Optional transaction data. **Out:** Form submission event. | Frontend |
| **Frontend: `components/.../TransactionList.svelte`**| A component to display a list of transactions. | **In:** Array of transaction objects. | Frontend |
| **Frontend: `stores/data.ts`**| Svelte store to manage and cache lists of transactions and categories. | API data. | Frontend |

### Data Models and Contracts

**`categories` Table Schema**

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | Primary Key | Unique identifier for the category. |
| `name` | `VARCHAR(255)` | Not Null | The name of the category (e.g., "Groceries", "Salary"). |
| `user_id` | `UUID` | Not Null, Foreign Key -> `users.id` | Links the category to the user who created it. |

**`transactions` Table Schema**

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | Primary Key | Unique identifier for the transaction. |
| `amount` | `DECIMAL(10, 2)` | Not Null | The monetary value of the transaction. |
| `type` | `VARCHAR(7)` | Not Null, Check: `income` or `expense` | The type of transaction. |
| `date` | `DATE` | Not Null | The date the transaction occurred. |
| `description`| `TEXT` | Nullable | An optional description for the transaction. |
| `user_id` | `UUID` | Not Null, Foreign Key -> `users.id` | Links the transaction to the user. |
| `category_id`| `UUID` | Not Null, Foreign Key -> `categories.id` | Links the transaction to a category. |

### APIs and Interfaces

**Categories API (`/api/v1/categories`)**
- `GET /`: Lists all categories for the authenticated user.
- `POST /`: Creates a new category.
- `PUT /{category_id}`: Updates an existing category's name.
- `DELETE /{category_id}`: Deletes a category.

**Transactions API (`/api/v1/transactions`)**
- `GET /`: Lists all transactions for the authenticated user, with optional filtering.
- `POST /`: Creates a new income or expense transaction.
- `PUT /{transaction_id}`: Updates an existing transaction.
- `DELETE /{transaction_id}`: Deletes a transaction.

### Workflows and Sequencing

**1. User Manages Categories:**
1.  User navigates to the `/settings/categories` page.
2.  The frontend calls `GET /api/v1/categories` to fetch and display the user's current categories.
3.  **Create:** User submits a new category name. Frontend sends a `POST` request. The list refreshes.
4.  **Update:** User edits a category name. Frontend sends a `PUT` request. The list refreshes.
5.  **Delete:** User deletes a category. Frontend sends a `DELETE` request after a confirmation prompt. The list refreshes.

**2. User Records a New Transaction:**
1.  On the main dashboard, the user clicks the "Add Transaction" button.
2.  The `TransactionForm.svelte` modal appears. The category dropdown is populated by data from `GET /api/v1/categories`.
3.  User fills in the amount, type, date, and selects a category, then clicks "Save".
4.  The frontend sends a `POST` request to `/api/v1/transactions`.
5.  Upon success, the modal closes, and the transaction list on the dashboard immediately updates to show the new entry.

## Non-Functional Requirements

### Performance

- **Requirement:** The application must be intuitive and easy to use for non-technical users (NFR001) and feel responsive (NFR003).
- **Targets:**
  - All CRUD API responses for transactions and categories should be < 300ms.
  - Fetching and displaying the initial list of transactions should be interactive in < 1.5 seconds for up to 1000 transactions.
  - UI updates after creating, editing, or deleting an item should feel instantaneous (< 100ms).

### Security

- **Requirement:** The application must provide a secure environment for user's financial data (NFR002).
- **Implementation:**
  - **Authorization:** All API endpoints for this epic (`/api/v1/transactions` and `/api/v1/categories`) MUST be protected and require a valid JWT token.
  - **Data Isolation:** All database queries for CRUD operations MUST be scoped to the authenticated `user_id`. A user must be strictly prevented from accessing or modifying another user's financial data. This is a critical security requirement.

### Reliability/Availability

- **Requirement:** The application should be reliably available to users.
- **Implementation:** The architecture's deployment strategy (Vercel, containerized backend, Supabase) continues to support high availability. Database transactions should be used for operations that modify multiple records to ensure data integrity.

### Observability

- **Requirement:** The system should provide enough information to debug issues.
- **Implementation:**
  - **Logging:** The backend will log the creation, update, and deletion of transactions and categories, including the `user_id` and object IDs, to provide an audit trail. Sensitive data like transaction amounts will not be logged.

## Dependencies and Integrations

No new external libraries or integrations are required for this epic. The implementation will rely on the existing technology stack established in Epic 1:

- **Backend:** FastAPI will be used to build the new CRUD endpoints.
- **Frontend:** SvelteKit and Svelte stores will be used to build the UI components and manage state.
- **Database:** The new `transactions` and `categories` tables will be created in the existing Supabase (PostgreSQL) database.

## Acceptance Criteria (Authoritative)

1.  **(From Story 2.1)** Given a user is on the category management page, when they create a new category with a unique name, then the new category is saved to the database and appears in their list of categories.
2.  **(From Story 2.1)** When they edit an existing category's name, then the change is reflected in the database and the UI.
3.  **(From Story 2.1)** When they delete a category, then it is removed from the database and the UI.
4.  **(From Story 2.2)** Given a user is on the main dashboard, when they open the "Add Transaction" form and enter an amount, select a category, and a date for an income or expense, then a new record is created in the `transactions` table in the database.
5.  **(From Story 2.2)** And the main dashboard immediately updates to reflect the new entry.
6.  **(From Story 2.3)** Given a user is viewing their transaction history, when they select a specific transaction to edit, then a form appears pre-filled with the transaction's details.
7.  **(From Story 2.3)** When the user modifies and saves the changes, then the transaction is updated in the database and the list is refreshed.
8.  **(From Story 2.4)** Given a user is viewing their transaction history, when they select an option to delete a specific transaction and confirm the action, then the transaction is permanently removed from the database.
9.  **(From Story 2.4)** And the transaction list and dashboard summary update to reflect the removal.

## Traceability Mapping

| AC ID | Spec Section(s) | Component(s)/API(s) | Test Idea |
| :--- | :--- | :--- | :--- |
| 1 | Data Models, APIs, Workflows | `POST /api/v1/categories`, `routes/settings/categories` | Manually create a new category on the settings page and verify it appears in the list and in the database. |
| 2 | APIs, Workflows | `PUT /api/v1/categories/{id}` | Manually edit a category's name and verify the UI and database are updated. |
| 3 | APIs, Workflows | `DELETE /api/v1/categories/{id}` | Manually delete a category and verify it is removed from the UI and database. |
| 4 | Data Models, APIs, Workflows | `POST /api/v1/transactions`, `TransactionForm.svelte` | Using the UI, create a new expense and verify the record is correctly saved in the `transactions` table. |
| 5 | Workflows | `TransactionList.svelte`, `stores/data.ts` | After creating a transaction, verify it immediately appears in the transaction list on the dashboard. |
| 6 | Workflows | `TransactionForm.svelte` | Click the "edit" button on a transaction and verify the form opens with the correct data pre-filled. |
| 7 | APIs, Workflows | `PUT /api/v1/transactions/{id}` | Edit a transaction's amount via the UI and verify the change is reflected in the list and the database. |
| 8 | APIs, Workflows | `DELETE /api/v1/transactions/{id}` | Delete a transaction and verify via the database that the record is gone. |
| 9 | Workflows | `TransactionList.svelte` | After deleting a transaction, confirm it is immediately removed from the UI list. |

## Risks, Assumptions, Open Questions

- **Risk:** Deleting a category that is currently associated with one or more transactions could lead to orphaned records or database constraint violations.
  - **Mitigation:** The backend `DELETE /api/v1/categories/{id}` endpoint must include logic to handle this. The chosen strategy will be to block the deletion and return an error message if the category is in use.
- **Assumption:** The performance of fetching all transactions will be acceptable for the MVP. Pagination will be considered for a future iteration if performance degrades with a large number of entries.
- **Question:** Should there be a default set of categories created for a new user (e.g., "Food", "Transport", "Housing")? For the MVP, we will assume no, and users start with a blank slate to create their own.

## Test Strategy Summary

The validation for this epic will expand upon the strategy from Epic 1, continuing with API-level and manual testing. The primary focus is ensuring the correctness of all CRUD operations and, most critically, the strict enforcement of data isolation between users.

- **API-Level Testing:**
  - All four CRUD endpoints for both `/categories` and `/transactions` will be tested for correct behavior on success and failure.
  - **Critical Security Test:** A dedicated test suite will be run using two different user accounts (User A and User B). The tests will confirm that User A can *only* interact with their own data. Every attempt by User B to access or modify User A's data via any endpoint must result in a `403 Forbidden` or `404 Not Found` error.
- **Manual End-to-End Testing:**
  - **Category Flow:** A user can successfully create, rename, and delete categories via the settings page.
  - **Transaction Flow:** A user can successfully create, edit, and delete both income and expense transactions from the dashboard.
  - **Integration Flow:** A user can create a new category and then immediately use it in a new transaction.
  - **Error Handling:** Test the UI's response to API errors, such as trying to create a category with a name that already exists.
  - **Data Integrity:** Confirm that attempting to delete a category that is in use presents the user with a clear error message and does not delete the category.
