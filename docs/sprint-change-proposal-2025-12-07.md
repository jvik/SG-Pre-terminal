# Sprint Change Proposal: Quick Category Creation

**Date:** 2025-12-07
**Author:** Bob (Scrum Master)
**Status:** Draft

## 1. Issue Summary
*   **Trigger:** User identified a usability gap in the "Add Transaction" view (Story 2.2).
*   **Problem:** Users cannot create a new category directly while adding a transaction. If a category is missing, they must abort the flow, go to settings, create it, and restart.
*   **Impact:** Friction in the core loop of the application, potentially discouraging transaction logging.

## 2. Impact Analysis
*   **Epics:** Epic 2 (Core Financial Management) is affected.
*   **Stories:**
    *   **Story 2.2 (Record Income and Expenses):** Completed, but lacks this feature.
    *   **New Story 2.5 (Quick Category Creation):** Proposed to address this gap without modifying closed stories.
*   **Artifacts:**
    *   **PRD:** Update "User Journey: Adding a New Expense".
    *   **UX Design:** Update "Core Loop" to include creation step.

## 3. Recommended Approach
*   **Strategy:** **Direct Adjustment (Add New Story).**
*   **Rationale:** Adding a specific story for this improvement allows us to keep Story 2.2 closed/stable while iteratively improving the UX. It isolates the risk and makes the change trackable.

## 4. Detailed Change Proposals

### 4.1. New Story: Story 2.5
**Title:** Quick Category Creation
**Epic:** Epic 2
**Goal:** Allow users to create a new category directly from the "Add Transaction" modal.
**Acceptance Criteria:**
1.  **Given** the user is opening the category dropdown in the "Add Transaction" modal
2.  **When** they type a name that doesn't exist OR click a "Create New" button
3.  **Then** they are presented with a quick input to define the new category (Name + Emoji)
4.  **And** upon saving, the new category is automatically selected in the transaction form
5.  **And** the transaction form remains open with previous data preserved.

### 4.2. PRD Update
**Section:** User Journey: Adding a New Expense
**Change:**
*   *Old:* "Step 4: ...select a category..."
*   *New:* "Step 4: ...select a category (or create a new one on the fly)..."

### 4.3. UX Design Spec Update
**Section:** 6.2 Core Loop: Transaction Management
**Change:** Add note about "Quick Create" flow within the modal steps.

## 5. Implementation Handoff
*   **Scope:** **Minor/Moderate** (Frontend logic + API reuse).
*   **Route To:** Development Team (via standard sprint backlog).
