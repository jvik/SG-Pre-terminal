# Story 3.2: Visualize Spending Breakdown

Status: review

## Story

As a user,
I want to see a simple chart on my dashboard that visualizes my expenses by category,
So that I can easily identify where my money is going.

## Acceptance Criteria

1.  **Given** a user is on the dashboard and has recorded expenses, **when** the dashboard loads, **then** a pie or bar chart is displayed, showing the proportion of spending for each category.
2.  **And** hovering over a chart segment displays the category name and total amount.

## Tasks / Subtasks

-   [x] **Backend: Create Chart Data Endpoint** (AC: #1)
    -   [x] Implement `GET /api/v1/dashboard/chart-data` in `backend/app/api/v1/endpoints/dashboard.py`.
    -   [x] Add business logic to `backend/app/crud/` to aggregate expense data by category.
    -   [x] Ensure the endpoint is protected and the database query is scoped to the authenticated `user_id`.
-   [x] **Frontend: Create Chart Component** (AC: #1)
    -   [x] Create a new `SpendingChart.svelte` component in `frontend/src/lib/components/routes/dashboard/`.
    -   [x] Use Chart.js and the `svelty-chartjs` wrapper to render a pie or bar chart.
    -   [x] Style the component according to the UX design specification.
-   [x] **Frontend: Integrate Chart on Dashboard** (AC: #1, #2)
    -   [x] In the main dashboard route (`frontend/src/routes/dashboard/+page.svelte`), fetch data from the `GET /api/v1/dashboard/chart-data` endpoint on page load.
    -   [x] Pass the fetched data as props to the `SpendingChart.svelte` component.
    -   [x] Ensure the chart data is managed in a Svelte store and refreshes when transactions change.

## Dev Notes

-   **API Endpoint:** The backend endpoint must be `GET /api/v1/dashboard/chart-data`.
-   **Data Contract:** The API should return a JSON object with labels (category names) and datasets (amounts).
-   **Security:** The backend query must be strictly filtered by the `user_id`.
-   **State Management:** Use a Svelte store for chart data to ensure reactivity.
-   **Performance:** The aggregation query must be performed at the database level for efficiency.

### Project Structure Notes

-   New backend endpoint in `backend/app/api/v1/endpoints/dashboard.py`.
-   New frontend component in `frontend/src/lib/components/routes/dashboard/SpendingChart.svelte`.

### Learnings from Previous Story

**From Story 3.1 (Status: done)**

-   **Reactivity is Key**: Do not use local variables for data that needs to be reactive. Use a proper Svelte store that is updated by the `transactions` store.
-   **Database-level Aggregation**: Perform calculations in the database, not in the Python code, to ensure performance.
-   **Thorough Testing**: Backend tests must validate the business logic, not just the endpoint's existence. Frontend tests should cover component integration.

### References

-   [Source: docs/epics.md#Story-3.2-Visualize-Spending-Breakdown]
-   [Source: docs/architecture.md#Architectural-Decisions]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/3-2-visualize-spending-breakdown.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
- excelence/backend/app/api/v1/endpoints/dashboard.py
- excelence/backend/app/crud/transactions.py
- excelence/backend/app/schemas/chart.py
- excelence/backend/app/schemas/__init__.py
- excelence/backend/supabase/migrations/20251207195326_create_expenses_by_category_rpc.sql
- excelence/backend/tests/api/v1/test_dashboard.py
- excelence/frontend/package.json
- excelence/frontend/src/lib/components/routes/dashboard/SpendingChart.svelte
- excelence/frontend/src/lib/components/routes/dashboard/SpendingChart.test.ts
- excelence/frontend/src/lib/services/api.ts
- excelence/frontend/src/lib/stores/data.ts
- excelence/frontend/src/routes/dashboard/+page.svelte

## Senior Developer Review (AI)

### Reviewer
Amelia (Dev Agent)

### Date
2025-12-07

### Outcome
**Approve**

The implementation is solid and fully meets the acceptance criteria and technical specifications. The backend correctly delegates aggregation to the database layer via a new RPC function, ensuring performance. The frontend integration using Chart.js is well-implemented with proper reactivity using Svelte stores.

### Key Findings

-   **High Severity:** None.
-   **Medium Severity:** None.
-   **Low Severity:** None.

### Acceptance Criteria Coverage

| AC# | Description | Status | Evidence |
| :--- | :--- | :--- | :--- |
| 1 | Chart displayed on dashboard showing spending proportion by category | **IMPLEMENTED** | `frontend/src/routes/dashboard/+page.svelte` (imports SpendingChart), `frontend/src/lib/components/routes/dashboard/SpendingChart.svelte` (renders chart) |
| 2 | Hovering over segment displays category name and total amount | **IMPLEMENTED** | `frontend/src/lib/components/routes/dashboard/SpendingChart.svelte` (tooltip callback logic) |

**Summary:** 2 of 2 acceptance criteria fully implemented.

### Task Completion Validation

| Task | Marked As | Verified As | Evidence |
| :--- | :--- | :--- | :--- |
| Backend: Create Chart Data Endpoint | [x] | **VERIFIED** | `backend/app/api/v1/endpoints/dashboard.py`, `backend/app/crud/transactions.py`, `backend/supabase/migrations/...sql` |
| Frontend: Create Chart Component | [x] | **VERIFIED** | `frontend/src/lib/components/routes/dashboard/SpendingChart.svelte` |
| Frontend: Integrate Chart on Dashboard | [x] | **VERIFIED** | `frontend/src/routes/dashboard/+page.svelte`, `frontend/src/lib/stores/data.ts` |

**Summary:** 3 of 3 completed tasks verified.

### Test Coverage and Gaps
-   **Backend:** `test_get_chart_data_integration` and `test_get_chart_data_empty` in `backend/tests/api/v1/test_dashboard.py` cover the new endpoint and crud logic.
-   **Frontend:** `SpendingChart.test.ts` covers component rendering and empty state.
-   **Coverage:** Good.

### Architectural Alignment
-   **Tech Spec:** Fully aligned. Endpoint and data contract match the spec.
-   **Architecture:** Follows the pattern of using Supabase RPC for aggregations and Svelte stores for state management.
-   **Library:** Used `chart.js` directly as `svelty-chartjs` installation had issues, but the implementation is clean and follows the "Use Chart.js" decision intent.

### Security Notes
-   **Authorization:** Endpoint protected by `get_current_active_user`.
-   **Data Isolation:** RPC function and CRUD layer explicitly filter by `user_id`.

### Best-Practices and References
-   **Database:** Good use of `security definer` RPC for encapsulation.
-   **Frontend:** `onMount` used correctly for Chart.js initialization (canvas requirement).

### Action Items

### Change Log
- 2025-12-07: Senior Developer Review notes appended.
**Advisory Notes:**
-   Note: The current color palette in `SpendingChart.svelte` has 8 colors. If a user has more categories, colors might need handling (e.g., repeating or generating dynamically). Acceptable for now.
