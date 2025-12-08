# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-30
**Project Level:** 
**Target Scale:** 

---

## Overview

This document provides the complete epic and story breakdown for ibe160, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

Here is the proposed epic structure. Each epic is designed to deliver incremental user value.

*   **Epic 1: Project Foundation & User Authentication:** Establishes the project's technical foundation and implements the core user account and authentication features.
*   **Epic 2: Core Financial Management:** Delivers the primary CRUD (Create, Read, Update, Delete) functionality for managing income, expenses, and categories.
*   **Epic 3: Dashboard, Visualization & Data Export:** Focuses on providing users with insights into their financial status through a dashboard, charts, and the ability to export their data.

---

## Functional Requirements Inventory

This inventory lists all functional requirements (FRs) from the PRD to ensure complete coverage in the epics and stories below.

*   **FR001:** Users must be able to register for a new account.
*   **FR002:** Users must be able to log in and log out of their account.
*   **FR003:** The system must allow users to create, read, update, and delete income and expense entries.
*   **FR004:** The system must allow users to create, read, update, and delete custom categories for income and expenses.
*   **FR005:** The system must automatically calculate and display the user's current financial status (e.g., total income, total expenses, net balance).
*   **FR006:** The system must provide a visual representation of income and expenses using simple graphs (e.g., bar or pie charts).
*   **FR007:** Users must be able to export their budget data to a CSV or Excel file.
*   **FR008:** The application must provide a full-featured view on desktop browsers.

---

## FR Coverage Map

This map shows which Functional Requirements (FRs) are addressed by each epic. Note that FR008 is a cross-cutting concern that applies to all epics.

*   **Epic 1: Project Foundation & User Authentication**
    *   Covers: **FR001, FR002**
*   **Epic 2: Core Financial Management**
    *   Covers: **FR003, FR004**
*   **Epic 3: Dashboard, Visualization & Data Export**
    *   Covers: **FR005, FR006, FR007**

---

## Epic 1: Project Foundation & User Authentication

**Goal:** Establish the project's technical foundation, implement user authentication, and deliver the core functionalities for account management. This epic ensures a secure and stable base for all future features.

### Story 1.1: Initialize Project Structure

As a developer,
I want to initialize the codebase using the full-stack starter template,
So that we have a consistent and pre-configured foundation for development.

**Acceptance Criteria:**

**Given** the project's approved tech stack (FastAPI, SvelteKit)
**When** the `cookiecutter` command is executed with the specified template
**Then** the project directory is created with separate `frontend` and `backend` folders
**And** all initial dependencies for both frontend and backend are installed and ready.

**Prerequisites:** None

**Technical Notes:** As per the architecture document, use the `cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql` command. This sets up the monorepo structure, Docker configuration, and initial JWT authentication boilerplate.

### Story 1.2: Implement User Registration

As a new user,
I want to register for an account using my email and a password,
So that I can access the application and manage my finances securely.

**Acceptance Criteria:**

**Given** a user is on the registration page
**When** they enter a valid email and a strong password and submit the form
**Then** a new user record is created in the `users` database table
**And** the user is automatically logged in and redirected to the main dashboard.
**And** the API returns a JWT token upon successful registration.

**Prerequisites:** Story 1.1

**Technical Notes:** This involves creating a `POST /api/v1/users` endpoint in the FastAPI backend. The endpoint should validate the incoming data using Pydantic schemas and hash the password before storing it. The frontend will have a registration form that calls this endpoint.

### Story 1.3: Implement User Login and Logout

As a registered user,
I want to log in with my email and password and be able to log out,
So that I can securely access my financial data and end my session.

**Acceptance Criteria:**

**Given** a registered user is on the login page
**When** they enter their correct credentials and submit the form
**Then** the system validates their credentials and returns a JWT token
**And** the user is redirected to the main dashboard.
**When** a logged-in user clicks the "Logout" button
**Then** their session is terminated and they are redirected to the login page.

**Prerequisites:** Story 1.2

**Technical Notes:** The backend will have a `POST /api/v1/auth/login` endpoint as defined in the architecture. The frontend will use Svelte's built-in stores to manage the user's authentication state and the JWT token. The logout functionality will clear the token from the store and local storage.

---

## Epic 2: Core Financial Management

**Goal:** Deliver the primary CRUD (Create, Read, Update, Delete) functionality for managing income, expenses, and the categories they belong to. This epic empowers users to take control of their financial data.

### Story 2.1: Create and Manage Categories

As a user,
I want to create, view, update, and delete custom categories,
So that I can organize my financial entries in a way that is meaningful to me.

**Acceptance Criteria:**

**Given** a user is on the category management page
**When** they create a new category with a unique name
**Then** the new category is saved to the database and appears in their list of categories.
**When** they edit an existing category's name
**Then** the change is reflected in the database and the UI.
**When** they delete a category
**Then** it is removed from the database and the UI.

**Prerequisites:** Story 1.3

**Technical Notes:** This requires a new set of CRUD endpoints in the backend under `/api/v1/categories`. The frontend will have a dedicated settings page for category management, likely in `frontend/src/routes/settings/categories`.

### Story 2.2: Record Income and Expenses

As a user,
I want to add new income and expense entries,
So that I can keep an accurate record of my finances.

**Acceptance Criteria:**

**Given** a user is on the main dashboard
**When** they open the "Add Transaction" form and enter an amount, select a category, and a date for an income or expense
**Then** a new record is created in the `transactions` table in the database.
**And** the main dashboard immediately updates to reflect the new entry.

**Prerequisites:** Story 2.1

**Technical Notes:** This will be the primary user interaction. A `POST /api/v1/transactions` endpoint is needed. The frontend will feature a prominent "Add" button that opens a modal form, as described in the PRD's user journey.

### Story 2.3: View and Update Transactions

As a user,
I want to view a list of my past transactions and be able to edit them,
So that I can review my financial history and correct any mistakes.

**Acceptance Criteria:**

**Given** a user is viewing their transaction history
**When** they select a specific transaction to edit
**Then** a form appears pre-filled with the transaction's details.
**When** the user modifies and saves the changes
**Then** the transaction is updated in the database and the list is refreshed.

**Prerequisites:** Story 2.2

**Technical Notes:** The backend needs `GET /api/v1/transactions` to list transactions and `PUT /api/v1/transactions/{transaction_id}` to update a specific one. The frontend will display these in a table or list format.

### Story 2.4: Delete Transactions

As a user,
I want to be able to delete a transaction,
So that I can remove accidental or incorrect entries.

**Acceptance Criteria:**

**Given** a user is viewing their transaction history
**When** they select an option to delete a specific transaction and confirm the action
**Then** the transaction is permanently removed from the database.
**And** the transaction list and dashboard summary update to reflect the removal.

**Prerequisites:** Story 2.3

**Technical Notes:** Requires a `DELETE /api/v1/transactions/{transaction_id}` endpoint. The UI should include a confirmation step (e.g., a modal dialog) to prevent accidental deletions.

### Story 2.5: Quick Category Creation

As a user,
I want to create a new category directly from the "Add Transaction" screen,
So that I don't have to interrupt my workflow if I realize a category is missing.

**Acceptance Criteria:**

**Given** a user is adding a new transaction
**When** they open the category selection dropdown
**Then** they see an option to "Create New Category".
**When** they select this option
**Then** a secondary input or modal appears to enter the new category details (name/icon).
**When** they save the new category
**Then** it is immediately selected in the transaction form, and the form remains open with previous data preserved.

**Prerequisites:** Story 2.2

**Technical Notes:** This is a frontend-heavy story. It requires reusing the category creation logic (or component) within the `TransactionForm`. The backend `POST /categories` endpoint already exists and should be reused. Ensure the state of the transaction form is not lost during this side-task.

---

## Epic 3: Dashboard, Visualization & Data Export

**Goal:** To provide users with a clear, visual summary of their financial situation and allow them to export their data for external use, turning raw data into actionable insights.

### Story 3.1: Display Financial Summary

As a user,
I want to see a real-time summary of my total income, expenses, and net balance on the dashboard,
So that I can quickly understand my current financial standing.

**Acceptance Criteria:**

**Given** a user is logged in and on the dashboard
**When** they view the page
**Then** the dashboard displays the calculated total income, total expenses, and the net balance for all their transactions.
**And** these totals automatically update whenever a transaction is added, edited, or deleted.

**Prerequisites:** Story 2.2

**Technical Notes:** The backend needs an endpoint like `GET /api/v1/dashboard/summary` to provide these calculated figures. The SvelteKit frontend will call this on dashboard load and refresh the data in its store after any transaction change.

### Story 3.2: Visualize Spending Breakdown

As a user,
I want to see a simple chart on my dashboard that visualizes my expenses by category,
So that I can easily identify where my money is going.

**Acceptance Criteria:**

**Given** a user is on the dashboard and has recorded expenses
**When** the dashboard loads
**Then** a pie or bar chart is displayed, showing the proportion of spending for each category.
**And** hovering over a chart segment displays the category name and total amount.

**Prerequisites:** Story 2.2

**Technical Notes:** Per the architecture, this will use Chart.js with the `svelty-chartjs` wrapper. A backend endpoint, `GET /api/v1/dashboard/chart-data`, will provide the aggregated data needed to render the chart.

### Story 3.3: Export Budget Data

As a user,
I want to export my transaction data to a CSV file,
So that I can perform my own analysis or keep a local backup.

**Acceptance Criteria:**

**Given** a user is on their dashboard
**When** they click an "Export to CSV" button
**Then** a `.csv` file is generated and downloaded by their browser.
**And** the file contains all their income and expense transactions, including columns for date, description, category, and amount.

**Prerequisites:** Story 2.3

**Technical Notes:** A backend endpoint, `GET /api/v1/export/csv`, will be created. This endpoint will query the user's transactions, format them into a CSV string, and return it with the appropriate headers for file download.

### Story 3.4: Implement Global Navigation Sidebar

As a user,
I want a persistent sidebar on all application pages,
So that I can easily navigate between the Dashboard, Spreadsheet, and Settings.

**Acceptance Criteria:**

**Given** a logged-in user
**When** they view any page
**Then** a fixed sidebar is visible on the left side of the screen.
**And** it contains links to: Dashboard, Spreadsheet/Transactions, and Settings.
**And** the current page is visually highlighted in the sidebar.
**When** viewing on a mobile screen
**Then** the sidebar collapses into a hamburger menu.

**Prerequisites:** Story 3.1

**Technical Notes:** This is a global layout change. Use SvelteKit's layout system (`+layout.svelte`) to ensure the sidebar persists. Responsive design is required using Tailwind CSS.

---

## FR Coverage Matrix

This matrix confirms that all functional requirements from the PRD have been mapped to at least one story.

| FR ID | Requirement Description | Epic(s) | Story(ies) |
|---|---|---|---|
| FR001 | User Registration | 1 | 1.2 |
| FR002 | User Login/Logout | 1 | 1.3 |
| FR003 | CRUD for Transactions | 2 | 2.2, 2.3, 2.4 |
| FR004 | CRUD for Categories | 2 | 2.1 |
| FR005 | Display Financial Status | 3 | 3.1 |
| FR006 | Visual Representation/Graphs | 3 | 3.2 |
| FR007 | Export Data | 3 | 3.3 |
| FR008 | Desktop-First Experience | 1, 2, 3 | All |

---

## Summary

This document provides a complete, story-by-story breakdown of the work required to deliver the Excelence MVP. The project is structured into three value-driven epics, ensuring that each phase of development delivers tangible functionality. All requirements from the PRD, UX, and Architecture documents have been incorporated. The project is now ready for implementation.

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

_This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical decisions._
