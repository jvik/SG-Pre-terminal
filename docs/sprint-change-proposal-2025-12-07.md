# Sprint Change Proposal: Fix Critical UI/UX Gaps

**Date:** 2025-12-07
**Author:** Product Manager
**Status:** Draft

## 1. Issue Summary
A review of the current application state revealed several critical gaps between the implemented UI and the UX specifications. Specifically, users cannot initiate registration from the landing page, the main navigation sidebar is missing, and the transaction entry flow lacks key usability features (category creation, working cancel button).

## 2. Impact Analysis
*   **Epic 1 (Foundation):** Registration flow is technically functional but visually inaccessible on the landing page.
*   **Epic 2 (Core Financials):** Transaction entry friction is high due to missing category creation and broken cancel functionality.
*   **Epic 3 (Dashboard):** Navigation is severely compromised without the sidebar, violating the core layout spec.

## 3. Recommended Approach
**Direct Adjustment:** We will modify the existing stories in the backlog to explicitly include these missing UI elements. A new story will be added to Epic 3 to specifically cover the Sidebar implementation, ensuring it is treated as a distinct, verifiable requirement.

## 4. Detailed Change Proposals

### Artifact: `docs/epics.md`

#### **Change 1: Update Story 1.2 (User Registration)**
*   **Reason:** Explicitly require the UI trigger for registration.
*   **Edit:**
    ```markdown
    **Acceptance Criteria:**
    ...
    **Given** a user is on the landing page
    **Then** a prominent "Register" or "Sign Up" button is visible.
    **When** they click the button, they are taken to the registration form.
    ...
    ```

#### **Change 2: Update Story 2.2 (Record Income/Expenses)**
*   **Reason:** Add category creation to flow and fix cancel button.
*   **Edit:**
    ```markdown
    **Acceptance Criteria:**
    ...
    **When** they open the "Add Transaction" form
    **Then** they see a button or link to "Create New Category" next to the category selector.
    **And** clicking "Cancel" immediately closes the form/modal without saving data.
    ...
    ```

#### **Change 3: Add New Story 3.4 (Global Navigation Sidebar)**
*   **Reason:** The sidebar is a complex, persistent component that was missed. It warrants its own story to ensure proper implementation.
*   **Addition:**
    ```markdown
    ### Story 3.4: Implement Global Navigation Sidebar

    As a user,
    I want a persistent sidebar on all application pages,
    So that I can easily navigate between the Dashboard, Spreadsheet, and Settings.

    **Acceptance Criteria:**
    **Given** a logged-in user
    **Then** a fixed sidebar (approx. 256px wide) is visible on the left side of the screen.
    **And** it contains links to: Dashboard, Spreadsheet/Transactions, and Settings.
    **And** the current page is visually highlighted in the sidebar.
    **And** on mobile screens, the sidebar collapses into a hamburger menu.
    ```

### Artifact: `docs/ux-design-specification.md`
*   **Status:** No changes needed. The specification already correctly describes these requirements (Sidebar, Layout). The implementation simply failed to match it.

## 5. Implementation Handoff
*   **Scope:** **Minor/Moderate**. These are standard UI implementations.
*   **Route To:** Development Team.
*   **Action:** Update `epics.md` and generate/update implementation plans for the affected stories.

---
**Approval Required:** Do you approve these changes?