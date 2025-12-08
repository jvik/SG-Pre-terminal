# Epic Technical Specification: Dashboard, Visualization & Data Export

Date: 2025-11-30
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

This epic focuses on transforming the raw financial data entered in Epic 2 into actionable insights for the user. It covers the development of the main dashboard, which will display a high-level summary of the user's financial status, a visual breakdown of expenses, and the functionality to export all transaction data. This is a critical step in fulfilling the project's core goal of simplifying financial management. The epic directly addresses functional requirements FR005 (Display Financial Status), FR006 (Visual Representation/Graphs), and FR007 (Export Data), making the application not just a data entry tool, but a useful instrument for financial analysis.

## Objectives and Scope

**In Scope:**

*   **Financial Summary:** A component on the dashboard that displays total income, total expenses, and the net balance.
*   **Data Visualization:** A simple pie or bar chart on the dashboard showing the proportion of expenses for each category.
*   **Data Export:** A button that allows users to download all their transaction data as a CSV file.
*   **Backend API:**
    *   An endpoint to provide the calculated financial summary data.
    *   An endpoint to provide aggregated data structured for the charting library.
    *   An endpoint to generate and return the CSV file.
*   **Frontend UI:**
    *   The main dashboard layout.
    *   Components to display the summary figures and the chart.
    *   The "Export to CSV" button and its associated functionality.

**Out of Scope:**

*   Advanced analytics or customizable dashboard widgets.
*   Multiple chart types or complex data filtering on the dashboard.
*   Exporting to formats other than CSV (e.g., Excel, PDF).
*   Any gamification features.

## System Architecture Alignment

This epic aligns perfectly with the architecture by introducing the dashboard-specific components and endpoints. The backend will gain new endpoints under `/api/v1/dashboard/` and `/api/v1/export/`, as planned in the project structure. The frontend will implement the dashboard view within the `frontend/src/routes` directory and will use the `svelty-chartjs` wrapper for `Chart.js`, as specified in the architectural decisions. Data for the dashboard will be fetched via the `api.ts` service and managed by Svelte stores, ensuring consistency with the established patterns. All backend endpoints will be protected and scoped to the authenticated user, maintaining the security and data isolation principles of the architecture.

## Detailed Design

### Services and Modules

| Service/Module | Responsibility | Inputs/Outputs | Owner |
| :--- | :--- | :--- | :--- |
| **Backend: `dashboard.py`** | Provides aggregated financial data for the dashboard. | **Out:** JSON objects for summary and chart data. | Backend |
| **Backend: `export.py`** | Generates and serves user data in CSV format. | **Out:** A `text/csv` file stream. | Backend |
| **Frontend: `routes/dashboard`** | The main dashboard page that composes the summary and visualization components. | User interactions. | Frontend |
| **Frontend: `components/.../FinancialSummary.svelte`**| A component to display the total income, expenses, and net balance. | **In:** Summary data object. | Frontend |
| **Frontend: `components/.../ExpenseChart.svelte`**| A component to render the expense breakdown chart using Chart.js. | **In:** Chart data array. | Frontend |

### Data Models and Contracts

No new database models are introduced in this epic. The API endpoints will return data in the following formats:

**Financial Summary Contract**
```json
{
  "total_income": 1500.00,
  "total_expenses": 450.50,
  "net_balance": 1049.50
}
```

**Chart Data Contract**
```json
[
  { "category_name": "Groceries", "total_amount": 250.00 },
  { "category_name": "Utilities", "total_amount": 100.50 },
  { "category_name": "Transport", "total_amount": 100.00 }
]
```

### APIs and Interfaces

**1. Get Financial Summary**
- **Endpoint:** `GET /api/v1/dashboard/summary`
- **Description:** Returns the user's total income, expenses, and net balance.
- **Success Response (200 OK):**
  - **Body:** `{ "status": "success", "data": { ...financial_summary_contract... } }`

**2. Get Chart Data**
- **Endpoint:** `GET /api/v1/dashboard/chart-data`
- **Description:** Returns the total expenses aggregated by category, for use in a chart.
- **Success Response (200 OK):**
  - **Body:** `{ "status": "success", "data": [ ...chart_data_contract_array... ] }`

**3. Export to CSV**
- **Endpoint:** `GET /api/v1/export/csv`
- **Description:** Generates and returns a CSV file of all the user's transactions.
- **Success Response (200 OK):**
  - **Body:** A `text/csv` file stream.
  - **Headers:** `Content-Disposition: attachment; filename="export.csv"`

### Workflows and Sequencing

**1. Dashboard Loading:**
1.  User logs in and is redirected to the main dashboard page.
2.  The dashboard page component (`routes/dashboard`) mounts.
3.  On mount, it makes two parallel API calls: one to `GET /api/v1/dashboard/summary` and one to `GET /api/v1/dashboard/chart-data`.
4.  The `FinancialSummary.svelte` component receives the summary data and displays the figures.
5.  The `ExpenseChart.svelte` component receives the chart data, formats it for Chart.js, and renders the chart.

**2. Data Export:**
1.  User is on the main dashboard.
2.  User clicks the "Export to CSV" button.
3.  The frontend initiates a download by linking to or navigating to `GET /api/v1/export/csv`.
4.  The backend queries all transactions for the user, formats them into a CSV string, and returns the response with the appropriate headers to trigger a browser download.

## Non-Functional Requirements

### Performance

- **Requirement:** The application should be responsive and performant, with minimal loading times for core features (NFR003).
- **Targets:**
  - The aggregation APIs (`/summary`, `/chart-data`) must respond in < 500ms for a user with up to 5000 transactions.
  - The CSV export process should initiate a download in < 2 seconds for the same data volume.
  - The dashboard UI should remain interactive while data is being fetched.

### Security

- **Requirement:** The application must provide a secure environment for user's financial data (NFR002).
- **Implementation:**
  - **Authorization:** All new endpoints (`/dashboard/*`, `/export/*`) must be protected and require a valid JWT token.
  - **Data Isolation:** All aggregation queries performed by the backend must be strictly filtered by the authenticated `user_id`. It must be impossible for one user's data to be included in another user's summary, chart, or export.

### Reliability/Availability

- **Requirement:** The application should be reliably available.
- **Implementation:** The existing high-availability architecture is sufficient. The new endpoints are read-only and do not introduce new reliability risks.

### Observability

- **Requirement:** The system should provide insight into the performance of data-intensive operations.
- **Implementation:**
  - **Logging:** The backend should log the execution time of the database queries for the summary, chart, and export endpoints to monitor for performance degradation as data volume grows.

## Dependencies and Integrations

- **Frontend (TypeScript/SvelteKit):**
  - **`chart.js`**: The core library for rendering charts.
  - **`svelty-chartjs`**: A Svelte wrapper to simplify the integration of Chart.js.
- **Backend (Python/FastAPI):**
  - No new dependencies are required for this epic. The standard library's `csv` module will be used for CSV generation.

## Acceptance Criteria (Authoritative)

1.  **(From Story 3.1)** Given a user is logged in and on the dashboard, when they view the page, then the dashboard displays the calculated total income, total expenses, and the net balance for all their transactions.
2.  **(From Story 3.1)** And these totals automatically update whenever a transaction is added, edited, or deleted.
3.  **(From Story 3.2)** Given a user is on the dashboard and has recorded expenses, when the dashboard loads, then a pie or bar chart is displayed, showing the proportion of spending for each category.
4.  **(From Story 3.2)** And hovering over a chart segment displays the category name and total amount.
5.  **(From Story 3.3)** Given a user is on their dashboard, when they click an "Export to CSV" button, then a `.csv` file is generated and downloaded by their browser.
6.  **(From Story 3.3)** And the file contains all their income and expense transactions, including columns for date, description, category, and amount.

## Traceability Mapping

| AC ID | Spec Section(s) | Component(s)/API(s) | Test Idea |
| :--- | :--- | :--- | :--- |
| 1 | Data Models, APIs, Workflows | `GET /api/v1/dashboard/summary`, `FinancialSummary.svelte` | Manually add several income/expense transactions. Verify the summary numbers on the dashboard match the expected calculated totals. |
| 2 | Workflows | `FinancialSummary.svelte` | After the dashboard is loaded, add a new transaction and verify the summary figures update automatically without a page reload. |
| 3 | Data Models, APIs, Workflows, Dependencies | `GET /api/v1/dashboard/chart-data`, `ExpenseChart.svelte` | Add expenses across several categories and verify the chart on the dashboard renders correctly, showing a segment for each category. |
| 4 | Workflows | `ExpenseChart.svelte` | Manually hover the mouse over each segment of the chart and confirm that a tooltip appears with the correct category name and total amount. |
| 5 | APIs, Workflows | `GET /api/v1/export/csv` | Click the "Export to CSV" button and confirm that the browser initiates a download for a file named `export.csv`. |
| 6 | APIs | `GET /api/v1/export/csv` | Open the downloaded CSV file and verify that its contents correctly match the transaction data, with all the specified columns present. |

## Risks, Assumptions, Open Questions

- **Risk:** The database queries for the dashboard aggregation and CSV export could become slow as a user's transaction history grows, leading to poor performance.
  - **Mitigation:** Ensure that the `user_id` columns in the `transactions` and `categories` tables are indexed in the database to optimize query performance. Monitor query times as per the Observability NFR.
- **Risk:** If a user has a large number of expense categories, the chart could become cluttered and unreadable.
  - **Mitigation:** For the MVP, this is an accepted risk. If it becomes an issue, a future iteration could group smaller categories into an "Other" slice.
- **Assumption:** The built-in `csv` module in Python is sufficient for the export functionality and no external libraries are needed.
- **Question:** What should the dashboard display (especially the chart) when a user has no transactions or no expenses?
  - **Decision:** The summary should display all zeros. The chart area should display a friendly message like "No expense data to display. Add a transaction to get started!"

## Test Strategy Summary

The test strategy will focus on the correctness of the data aggregations and the integrity of the exported file.

- **API-Level Testing:**
  - The `/summary` and `/chart-data` endpoints will be tested by populating the database with a known set of transactions and asserting that the API responses contain the exact calculated totals and aggregations.
  - The `/export/csv` endpoint will be tested to ensure it returns a `200 OK` status with the correct `Content-Type` and `Content-Disposition` headers.
  - **Security:** As with other epics, all tests must be run for multiple user accounts to verify that one user's dashboard and export never contain data from another user.
- **Manual End-to-End Testing:**
  - **Data Accuracy:** Manually perform calculations on a small set of transaction data and verify that the numbers shown in the `FinancialSummary` component and `ExpenseChart` tooltips are correct.
  - **Chart Interaction:** Verify that the chart renders correctly and that tooltips work as expected.
  - **Empty State:** Test the dashboard's appearance for a brand new user with no transactions.
  - **CSV Validation:** Click the "Export to CSV" button, open the downloaded file in a spreadsheet program, and confirm:
    1.  The header row is correct.
    2.  The number of data rows matches the number of transactions.
    3.  The data in the cells accurately reflects the transaction data.
    4.  Dates and amounts are formatted correctly.
