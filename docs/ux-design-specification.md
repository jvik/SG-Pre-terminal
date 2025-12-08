# UX Design Specification: Excelence

This document outlines the collaborative UX and UI design decisions for **Excelence**, a personal finance web application. It is based on the initial visual direction created with Google Stitch and refined through a collaborative process to ensure it is user-centric, consistent, and implementation-ready.

## 1. Collaborative Process and Key Decisions

This specification is the result of a collaborative design process. After a review of the two distinct visual themes in the initial mockups, the following key decisions were made **with the user**:

*   **Design Direction:** From the options presented in `ux-design-directions.html`, the user selected **Option A: Professional & Data-Driven**. This clean, modern, and data-rich direction found in the main dashboard mockups (the "FinFlow" theme) will be used for the entire application, including modals.
*   **Brand Name:** The application will be consistently referred to as **Excelence**. All UI elements will be updated to reflect this.
*   **Design System:** We will use **Tailwind CSS** as the foundational design system, which aligns with the class-based approach in the Stitch files.

## 2. Design System Foundation

*   **Chosen System:** Tailwind CSS
*   **Version:** v3
*   **Rationale:** The existing designs are built with Tailwind CSS, making it the natural choice. It provides a robust, utility-first framework for building a consistent and responsive UI efficiently. This choice was affirmed as part of our collaborative review.

## 3. Core Experience Definition

*   **Defining Experience:** Excelence provides a **gamified and encouraging approach to personal finance**, making budgeting feel less like a chore and more like a rewarding journey towards financial wellness.
*   **Core Principles:**
    *   **Clarity:** Present financial data in a way that is easy to understand at a glance.
    *   **Encouragement:** Use positive reinforcement and gamification to motivate users.
    *   **Efficiency:** Enable users to perform core tasks like adding transactions with minimal effort.
    *   **Control:** Give users the tools to customize categories and set personal goals.

## 4. Visual Foundation (Based on User-Selected Option A)

This section standardizes the visual elements for the entire application.

### 4.1. Color System

The primary color palette is professional and calming, using a dependable blue as the primary actor, with an energetic orange as a secondary accent for gamified elements.

| Role                  | Light Theme                               | Dark Theme                                | Usage                                                              |
| --------------------- | ----------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------ |
| **Primary**           | `#4A90E2` (Blue)                           | `#4A90E2` (Blue)                           | CTAs, interactive elements, highlights, navigation.                |
| **Secondary**         | `#F5A623` (Orange)                         | `#F5A623` (Orange)                         | Gamification elements (streaks, achievements), highlights.         |
| **Background**        | `#F4F7FA` (Off-white)                      | `#1A202C` (Dark Slate)                     | Main application background.                                       |
| **Surface/Card**      | `#FFFFFF` (White)                         | `#2D3748` (Dark Gray)                      | Card backgrounds, sidebars, modals.                                |
| **Text Primary**      | `#4A4A4A` (Dark Gray)                      | `#E2E8F0` (Light Gray)                     | Headings, primary body text.                                       |
| **Text Secondary**    | `#A0AEC0` (Medium Gray)                    | `#718096` (Light Gray)                     | Sub-headings, labels, secondary information.                       |
| **Border**            | `#E2E8F0` (Light Gray)                     | `#4A5568` (Medium Gray)                    | Borders, dividers.                                                 |
| **Semantic: Success** | `#34D399` (Green)                          | `#34D399` (Green)                          | Positive feedback, income visualization.                           |
| **Semantic: Warning** | `#FBBF24` (Yellow)                         | `#FBBF24` (Yellow)                         | Non-critical alerts.                                               |
| **Semantic: Error**   | `#F87171` (Red)                            | `#F87171` (Red)                            | Errors, negative feedback, expense visualization.                  |

### 4.2. Typography

*   **Font Family:** "Inter", sans-serif. Chosen for its clean readability, which is ideal for data-heavy interfaces.
*   **Type Scale:**
    *   **h1 (Page Title):** 3xl (30px), font-black
    *   **h2 (Section Title):** xl (20px), font-bold
    *   **h3 (Card Title):** lg (18px), font-bold
    *   **Body:** base (16px), font-normal
    *   **Small/Sub-text:** sm (14px), font-normal

### 4.3. Spacing & Layout

*   **Base Unit:** 4px. Spacing is based on a 4px grid system (e.g., `p-4` = 16px, `gap-6` = 24px).
*   **Layout:** The main application uses a two-column layout with a fixed sidebar (256px width) and a main content area.
*   **Border Radius:**
    *   **Default:** `0.5rem` (e.g., for buttons, inputs)
    *   **Large:** `1rem` (e.g., for cards, modals)

## 5. Design Direction

*   **Chosen Direction:** Clean & Focused (User-selected Option A).
*   **Description:** The UI is clean, with a strong visual hierarchy. It uses cards to group related information, ample white space to reduce cognitive load, and a clear color system to guide the user's attention. The focus is on data visualization and quick access to core actions.
*   **Rationale:** This direction was chosen by the user because it feels professional, trustworthy, and easy to navigate. It allows the financial data to be the hero, which is the primary goal of the application.

## 6. User Journey Flows

This section details the primary user journeys, derived from the Stitch mockups.

### 6.1. Onboarding (New User Registration & Login)

**Goal:** A new user creates an account and logs in for the first time.

**Steps:**
1.  User lands on the **Login/Registration** page.
2.  User selects the "Sign Up" tab.
3.  User fills in their email, a password, and confirms the password.
4.  User clicks "Create My Account".
5.  *Alternate Path:* User clicks "Continue with Google" for OAuth registration.
6.  Upon successful registration, the user is automatically logged in and redirected to the **Main Dashboard**.
7.  A "Welcome" modal may appear, prompting them to add their first transaction or set a goal.

```mermaid
graph TD
    A[/"Landing Page (Login/Registration)"] --> B{Select Auth Type};
    B --> C["Sign Up Tab"];
    B --> D["Log In Tab"];
    C --> E["Fill Email/Password"];
    C --> F["Continue with Google"];
    E --> G["Click 'Create My Account'"];
    F --> G;
    D --> H["Fill Email/Password"];
    H --> I["Click 'Log In'"];
    G --> J[/"Main Dashboard"];
    I --> J;
```

### 6.2. Core Loop: Transaction Management

**Goal:** An existing user logs in, adds a new expense, and views it in the spreadsheet.

**Steps:**
1.  User logs in and lands on the **Main Dashboard**.
2.  User clicks the "Add Expense" button.
3.  **An "Add Transaction" modal appears (similar to the "Create Category" modal).**
4.  **User enters the amount, selects a category (or clicks "Create New" to add one instantly), adds a description, and confirms the date.**
5.  **User clicks "Save Transaction".**
6.  The modal closes, and the dashboard widgets (e.g., Total Expenses, Spending Breakdown) update in real-time.
7.  User navigates to the **Spreadsheet** page via the sidebar.
8.  The new transaction is visible at the top of the transaction list.
9.  User can hover over the transaction row to reveal "Edit" and "Delete" actions.

```mermaid
graph TD
    A[/"Main Dashboard"] --> B["Click 'Add Expense'"];
    B --> C["Add Transaction Modal Opens"];
    C --> D["Fill Details (Amount, Category, etc.)"];
    D --> E["Click 'Save Transaction'"];
    E --> F["Dashboard Widgets Update"];
    F --> G["Navigate to Spreadsheet Page"];
    G --> H["View New Transaction in List"];
```

### 6.3. Goal & Category Management

**Goal:** A user creates a new savings goal and a new expense category.

**Steps (Create Goal):**
1.  From the **Main Dashboard**, the user navigates to a "Goals" section (or a CTA).
2.  The user clicks "Create New Goal".
3.  The **Create a New Goal** modal appears.
4.  User fills in the goal name, target amount, and target date.
5.  User clicks "Set My Goal".
6.  The new goal appears in the "Your Goals" widget on the dashboard.

**Steps (Create Category):**
1.  From the **Spreadsheet** or **Settings** page, the user clicks "Manage Categories".
2.  The user clicks "Create New Category".
3.  The **Create a New Category** modal appears.
4.  User fills in the category name and an optional emoji.
5.  User clicks "Create Category".
6.  The new category is now available in the category selection dropdown when adding a new transaction.

### 6.4. Profile & Settings Management

**Goal:** A user updates their profile information and application preferences.

**Steps:**
1.  User clicks on "Settings" in the sidebar navigation.
2.  User is taken to the **Settings** page.
3.  User can update their Full Name and Email in the "Profile" section.
4.  User can change their preferred currency in the "Preferences" section.
5.  User can toggle email notifications on or off.
6.  User can switch between Light, Dark, and System themes.
7.  User clicks "Save Changes" to apply all updates.

```mermaid
graph TD
    A[/"Any Page"] --> B["Click 'Settings' in Sidebar"];
    B --> C[/"Settings Page"];
    C --> D["Update Profile Info"];
    C --> E["Change Preferences (Currency, Theme)"];
    D --> F["Click 'Save Changes'"];
    E --> F;
```

## 7. Component Library

This library is derived from a detailed analysis of the `docs/UI_stitch_design/stitch_excelence/` mockups.

### 7.1. Global Components

*   **Sidebar Navigation:**
    *   **Purpose:** Primary navigation for the application.
    *   **Content:** App logo/name, user profile summary, navigation links (Dashboard, Spreadsheet, Achievements, Settings), Game Mode toggle, Help Center link.
    *   **States:**
        *   **Active Link:** `bg-primary/20`, `text-primary`
        *   **Hover:** `bg-primary/10`
    *   **Variants:** The sidebar is fixed on desktop views.

*   **Modals:**
    *   **Purpose:** Used for focused tasks like creating goals or categories without leaving the current page.
    *   **Content:** Contains a form with a clear title, icon, input fields, and a primary action button.
    *   **Behavior:** Appears centered over the page content with a backdrop blur. Can be dismissed via an "X" icon in the top-right corner.
    *   **Variants:** `create_goal`, `create_category`. Note the distinct color scheme (`primary: #13ec80`) used in the modal mockups.

### 7.2. Form Elements

*   **Text Input with Icon:**
    *   **Purpose:** Standard user input for text, email, password, and numbers.
    *   **Content:** A label, an input field, and a leading Material Symbols icon.
    *   **States:**
        *   **Default:** `border-border-light`
        *   **Focus:** `ring-2`, `ring-primary/50`
    *   **Variants:** Email, Password, Text, Date.

*   **Toggle Switch:**
    *   **Purpose:** To turn settings on or off (e.g., Game Mode, Email Notifications).
    *   **States:** On, Off.

### 7.3. Buttons

*   **Primary Action Button:**
    *   **Purpose:** For the main call-to-action in a view or modal.
    *   **Style:** Solid background color (`bg-primary`), white or dark text.
    *   **Examples:** "Add Expense", "Create Category", "Save Changes".

*   **Secondary Action Button:**
    *   **Purpose:** For secondary calls-to-action.
    *   **Style:** Bordered (`border`), transparent or light background.
    *   **Examples:** "Add Income", "Change Avatar".

*   **Tertiary/Link Button:**
    *   **Purpose:** For less prominent actions or links.
    *   **Style:** No border or background (ghost/link style).
    *   **Examples:** "View All".

*   **OAuth Button:**
    *   **Purpose:** For social sign-in.
    *   **Style:** Bordered, with provider logo (e.g., Google).

### 7.4. Data Display

*   **Dashboard Stat Card:**
    *   **Purpose:** To display a single, key financial metric on the dashboard.
    *   **Content:** Title (e.g., "Total Income"), the metric value, and a percentage change comparison.
    *   **Style:** Rounded corners (`rounded-xl`), `shadow-sm`.

*   **Spending Breakdown Chart (Donut Chart):**
    *   **Purpose:** To visualize expense distribution by category.
    *   **Content:** A multi-colored donut chart, a central label showing the total, and a legend listing categories with their percentage and absolute values.

*   **Goal Progress Bar:**
    *   **Purpose:** To show progress towards a financial goal.
    *   **Content:** A label with the goal name, a progress bar, and text showing the current/total amount and time remaining.

*   **Transaction Table/Spreadsheet:**
    *   **Purpose:** To display a detailed list of all income and expense transactions.
    *   **Content:** Columns for Amount, Category, Description, and Date. Rows are color-coded for income (green) and expense (red).
    *   **Behavior:** On hover, action buttons (Edit, Delete) appear for each row.

*   **Achievement Card:**
    *   **Purpose:** To display a gamification badge.
    *   **Variants:**
        *   **Unlocked:** Full color, prominent icon, border-glow effect.
        *   **Locked:** Grayscale/desaturated, progress bar if applicable.
        *   **Hidden:** Represented as a placeholder.

## 8. UX Pattern Consistency Rules

These rules are established from the common patterns observed across all provided mockups.

*   **Forms and Modals:**
    *   **Structure:** All forms within modals follow a consistent structure: Icon + Title, descriptive subtext, labeled input fields, and a full-width primary action button at the bottom.
    *   **Feedback:** The `Create Goal` and `Create Category` modals include a progress bar that is full, indicating the form is complete and ready to be submitted. This pattern should be used for all multi-step or validation-ready forms.
    *   **Dismissal:** All modals must be dismissible via a dedicated "close" icon in the top-right corner.

*   **Button Hierarchy:**
    *   **Primary:** A solid background button is always the primary affirmative action (e.g., "Save", "Create", "Add"). On the dashboard, "Add Expense" is primary over "Add Income".
    *   **Secondary:** A bordered button is used for secondary actions (e.g., "Add Income", "Change Avatar").
    *   **Destructive:** Destructive actions, like "Delete" in the spreadsheet, should use a red icon/text on hover.

*   **Navigation:**
    *   **Primary Navigation:** The main sidebar is the single source for navigating between the application's top-level pages (Dashboard, Spreadsheet, etc.).
    *   **Active State:** The current page must be clearly indicated in the sidebar with a background and text color change.

*   **Feedback and Status:**
    *   **Income/Expense:** Financial values should be consistently colored: Green for income (positive) and Red for expenses (negative). This applies to the spreadsheet and transaction lists.
    *   **Achievements:** Unlocked achievements are visually distinct and celebrated (e.g., with a glowing border), while locked achievements are subdued to encourage completion.

*   **Empty States:**
    *   **Guidance:** While not explicitly shown in the mockups, empty states (e.g., no transactions, no goals) should provide a helpful message and a clear call-to-action to guide the user's next step (e.g., "Add your first transaction!").

## 9. Responsive Design

*   **Breakpoints:** The design uses standard Tailwind CSS breakpoints (sm, md, lg, xl).
*   **Strategy:** On smaller screens, the sidebar navigation will collapse into a hamburger menu. Multi-column layouts will stack vertically.
*   **Adaptation Patterns:**
    *   **Dashboard Stat Cards:** The 4-column grid of stat cards will stack vertically on mobile.
    *   **Main Content Layout:** The two-column (sidebar + content) layout will become a single column, with the sidebar hidden behind a hamburger menu icon.
    *   **Spreadsheet/Table:** The transaction table may require horizontal scrolling on small screens to remain usable.

## 10. Accessibility

*   **Target:** The application will target WCAG 2.1 AA compliance.
*   **Strategy:**
    *   **Color Contrast:** All text/background color combinations must meet the minimum contrast ratio of 4.5:1. This will be verified with automated tools.
    *   **Keyboard Navigation:** All interactive elements (buttons, links, form fields, toggles) must be reachable and operable via the `Tab` key. The focus order must be logical.
    *   **Focus Indicators:** A clear and visible focus state (e.g., the `focus:ring-2` class seen in the mockups) must be present on all interactive elements.
    *   **Semantic HTML:** Use appropriate HTML elements (`<nav>`, `<main>`, `<button>`, `<label>`, etc.) to define the structure and purpose of content.
    *   **ARIA Roles:** For custom components, use appropriate ARIA roles. For example:
        *   **Modals:** Use `role="dialog"`, `aria-modal="true"`, and manage focus trapping.
        *   **Sidebar:** Use `<nav>` with an appropriate `aria-label` (e.g., "Main Navigation").
    *   **Form Accessibility:** All form inputs must have an associated `<label>` element for screen readers.
    *   **Alt Text:** All meaningful images (like user avatars) must have descriptive alt text. Decorative icons should have an empty `alt` attribute.
    *   **Testing Strategy:** Accessibility will be checked at two stages:
        *   **Automated:** Use browser extensions (like Axe DevTools) during development to catch common issues.
        *   **Manual:** Perform keyboard-only navigation checks and screen reader (e.g., NVDA, VoiceOver) walkthroughs for critical user journeys before release.
