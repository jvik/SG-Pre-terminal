# Story 3.4: Implement Global Navigation Sidebar

Status: review

## Story

As a user,
I want a persistent sidebar on all application pages,
So that I can easily navigate between the Dashboard, Spreadsheet, and Settings.

## Acceptance Criteria

1.  **Given** a logged-in user, **when** they view any page, **then** a fixed sidebar is visible on the left side of the screen.
2.  **And** it contains links to: Dashboard, Spreadsheet/Transactions, and Settings.
3.  **And** the current page is visually highlighted in the sidebar.
4.  **When** viewing on a mobile screen, **then** the sidebar collapses into a hamburger menu.

## Tasks / Subtasks

-   [x] **Create Sidebar Component** (AC: #1, #2, #3)
    -   [x] Create `frontend/src/lib/components/layout/Sidebar.svelte`.
    -   [x] Implement navigation links using SvelteKit's `$page` store to determine active state.
    -   [x] Apply Tailwind CSS classes for fixed positioning, width (`w-64`), and styling.
    -   [x] **Testing**: Create component test `frontend/src/lib/components/layout/Sidebar.test.ts` to verify links and active class application.
-   [x] **Implement Responsive Behavior** (AC: #4)
    -   [x] Add state for sidebar visibility (open/closed) on mobile.
    -   [x] Create a "Hamburger" toggle button visible only on mobile breakpoints.
    -   [x] Implement transition/animation for sidebar sliding in/out on mobile.
    -   [x] **Testing**: Verify toggle functionality and visibility classes at different viewports.
-   [x] **Integrate into Global Layout** (AC: #1)
    -   [x] Modify `frontend/src/routes/+layout.svelte` to include the `<Sidebar />` component.
    -   [x] Adjust the main content area with a left margin (`ml-64` on desktop) to prevent overlap.
    -   [x] Ensure the layout is responsive (no margin on mobile).

## Dev Notes

-   **Architecture**: This story implements the Global Navigation Sidebar as a core layout component. It must be integrated into the root `+layout.svelte` to persist across all routes.
-   **State Management**: Use SvelteKit's `$page` store (from `$app/stores`) to access `url.pathname` for highlighting the active link.
-   **Styling**: Use Tailwind CSS utility classes.
    -   Desktop: `fixed`, `h-full`, `w-64`, `border-r`.
    -   Mobile: `fixed`, `z-50`, `transform` (for sliding).
    -   Content Area: Needs dynamic padding/margin based on screen size.

### Project Structure Notes

-   **New Component**: `frontend/src/lib/components/layout/Sidebar.svelte`
-   **Modified File**: `frontend/src/routes/+layout.svelte`

### Learnings from Previous Story

**From Story 3.3 (Status: done)**

-   **Frontend/Backend Separation**: Story 3.3 confirmed the pattern of separate concerns. This story is purely frontend but relies on the project structure established.
-   **Review Items**: No blocking review items from 3.3 affect the sidebar, but maintaining high code quality and component testing (as seen in 3.3) is required.

### References

-   [Source: docs/epics.md#story-3-4-implement-global-navigation-sidebar]
-   [Source: docs/architecture.md#project-structure-and-boundaries]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/3-4-implement-global-navigation-sidebar.context.xml

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

- Implemented `Sidebar` component with Svelte 5 runes (`$state`, `$derived`, `$effect`).
- Added responsive hamburger menu logic directly within `Sidebar.svelte` for encapsulation.
- Integrated Sidebar into `+layout.svelte`, using `md:ml-64` to offset content on desktop and conditional rendering based on authentication.
- Added comprehensive tests in `Sidebar.test.ts` covering rendering, active link highlighting, and mobile toggle behavior.

### File List

- excelence/frontend/src/lib/components/layout/Sidebar.svelte
- excelence/frontend/src/lib/components/layout/Sidebar.test.ts
- excelence/frontend/src/routes/+layout.svelte