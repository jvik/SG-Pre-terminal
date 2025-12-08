# Epic Technical Specification: Project Foundation & User Authentication

Date: 2025-11-30
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

## Overview

This epic lays the foundational groundwork for the Excelence application. It covers two critical areas: initializing the technical scaffolding using a full-stack starter template and implementing the complete user authentication and account management system. The primary goal is to establish a secure, stable, and scalable base upon which all subsequent features, such as financial management and data visualization, will be built. This epic directly addresses the core functional requirements for user registration (FR001) and login/logout (FR002), ensuring that users can securely create and access their accounts from the very beginning.

## Objectives and Scope

**In Scope:**

*   Initializing the project structure with separate `frontend` (SvelteKit) and `backend` (FastAPI) directories.
*   Setting up all initial dependencies, build tooling, and Docker configurations as provided by the starter template.
*   Implementing the backend API endpoints for user registration (`POST /api/v1/users`) and login (`POST /api/v1/auth/login`).
*   Creating the database schema for the `users` table, including secure password hashing.
*   Developing the frontend registration and login pages and forms.
*   Managing user authentication state on the frontend using Svelte's built-in stores and JWT tokens.
*   Implementing logout functionality to securely terminate user sessions.

**Out of Scope:**

*   Any financial management features (CRUD for transactions or categories).
*   The main user dashboard, data visualization, or charting.
*   Gamification features (goals, achievements).
*   Data export or import functionality.

## System Architecture Alignment

This epic directly implements the foundational components of the chosen architecture. The `cookiecutter` initialization (Story 1.1) establishes the prescribed monorepo structure, build tools (Docker, Vite), and technology stack (FastAPI, SvelteKit). The user authentication stories (1.2 and 1.3) will create the initial API endpoints (`/auth`, `/users`) and database models (`users`) as outlined in the architecture document. Frontend state management for authentication will utilize Svelte's built-in stores, aligning with the decision to keep the frontend lightweight and avoid external dependencies for state. The implementation will adhere to the specified JWT token-based authentication mechanism and the standardized JSend-style API responses.

## Detailed Design

### Services and Modules

| Service/Module | Responsibility | Inputs/Outputs | Owner |
| :--- | :--- | :--- | :--- |
| **Backend: `auth.py`** | Handles user login and JWT token generation. | **In:** User credentials. **Out:** JWT Token. | Backend |
| **Backend: `users.py`** | Handles new user registration. | **In:** New user data. **Out:** Created user object & JWT Token. | Backend |
| **Backend: `schemas/user.py`**| Defines Pydantic schemas for user creation and data validation. | N/A | Backend |
| **Backend: `models/user.py`**| Defines the `users` database table model. | N/A | Backend |
| **Frontend: `routes/login`** | Provides the user interface for logging in. | User interactions. | Frontend |
| **Frontend: `routes/register`**| Provides the user interface for new account registration. | User interactions. | Frontend |
| **Frontend: `stores/auth.ts`**| Svelte store to manage the user's authentication state and JWT token globally. | **In:** JWT Token. **Out:** User auth status. | Frontend |
| **Frontend: `services/api.ts`**| Central module for handling all communication with the backend API, including error handling. | API requests/responses. | Frontend |

### Data Models and Contracts

**`users` Table Schema**

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | Primary Key, Default: `gen_random_uuid()` | Unique identifier for the user. |
| `email` | `VARCHAR(255)` | Not Null, Unique | User's email address, used for login. |
| `hashed_password` | `VARCHAR(255)` | Not Null | User's password, stored securely after hashing. |
| `is_active` | `BOOLEAN` | Not Null, Default: `true` | Flag to activate or deactivate the user account. |
| `created_at` | `TIMESTAMPZ` | Not Null, Default: `now()` | Timestamp of when the user account was created. |

### APIs and Interfaces

**1. User Registration**
- **Endpoint:** `POST /api/v1/users`
- **Description:** Creates a new user account.
- **Request Body (`schemas.UserCreate`):**
  ```json
  {
    "email": "user@example.com",
    "password": "a_strong_password"
  }
  ```
- **Success Response (201 Created):**
  - **Body:** `{ "status": "success", "data": { ...user_object... } }`
  - **Headers:** Includes a JWT token for the new session.
- **Error Response (400 Bad Request):**
  - **Body:** `{ "status": "error", "message": "Email already registered" }`

**2. User Login**
- **Endpoint:** `POST /api/v1/auth/login`
- **Description:** Authenticates a user and returns a JWT token.
- **Request Body (OAuth2PasswordRequestForm):**
  ```x-www-form-urlencoded
  username=user@example.com&password=a_strong_password
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Error Response (401 Unauthorized):**
  - **Body:** `{ "status": "error", "message": "Incorrect email or password" }`

### Workflows and Sequencing

**1. New User Registration Flow:**
1.  User navigates to the `/register` page on the SvelteKit frontend.
2.  User fills out the registration form and clicks "Submit".
3.  The frontend `api.ts` service sends a `POST` request to `/api/v1/users` with the user's email and password.
4.  The FastAPI backend receives the request, validates the data using the `UserCreate` schema, hashes the password, and creates a new record in the `users` table.
5.  Upon successful creation, the backend generates a JWT token.
6.  The backend returns a `201 Created` response with the user data and the JWT token.
7.  The frontend `auth.ts` store saves the JWT token, updates the user's state to logged-in, and redirects the user to the main dashboard.

**2. User Login Flow:**
1.  User navigates to the `/login` page.
2.  User enters their email and password and clicks "Login".
3.  The frontend `api.ts` service sends a `POST` request to `/api/v1/auth/login`.
4.  The backend validates the credentials against the `users` table.
5.  If valid, it generates and returns a JWT token.
6.  The frontend `auth.ts` store saves the token, updates the state, and redirects to the dashboard.
7.  If invalid, an error is shown to the user.

## Non-Functional Requirements

### Performance

- **Requirement:** The application should be responsive and performant, with minimal loading times for core features (NFR003).
- **Targets:**
  - API response times for authentication endpoints should be < 200ms under normal load.
  - Frontend page loads for login and registration should be interactive in < 1 second.

### Security

- **Requirement:** The application must provide a secure environment for user's financial data (NFR002).
- **Implementation:**
  - **Authentication:** All access to user-specific data will be protected and require a valid JWT token sent in the `Authorization` header.
  - **Password Storage:** User passwords will be salted and hashed using a strong algorithm (e.g., bcrypt) before being stored in the database. Plaintext passwords will never be stored.
  - **Data Transmission:** All communication between the frontend and backend will be over HTTPS.

### Reliability/Availability

- **Requirement:** The application should be reliably available to users.
- **Implementation:** The chosen deployment strategy (Vercel for frontend, containerized service for backend, Supabase for DB) provides high availability and fault tolerance. The system is expected to meet standard web application uptime of >99.9%.

### Observability

- **Requirement:** The system should provide enough information to debug issues.
- **Implementation:**
  - **Logging:** The FastAPI backend will implement structured logging to capture key events, particularly for authentication successes and failures (without logging sensitive data).
  - **Metrics:** Basic application health metrics will be exposed if supported by the hosting platform (e.g., response counts, error rates).

## Dependencies and Integrations

- **Backend (Python/FastAPI):**
- - `uv`: The core web framework for building the API.
  - `fastapi`: The core web framework for building the API.
  - `uvicorn`: The ASGI server to run the FastAPI application. Should be run with UV. Should be executed with `uv run uvicorn main:app --reload`
  - `pydantic`: For data validation and settings management.
  - `python-dotenv`: For managing environment variables from `.env` files.
  - `passlib[bcrypt]`: For securely hashing and verifying passwords.
  - `python-jose[cryptography]`: For creating and verifying JWT tokens for authentication.
- **Frontend (TypeScript/SvelteKit):**
  - `@sveltejs/kit`: The full-stack Svelte framework for the frontend application.
  - `svelte`: The core Svelte compiler.
  - `vite`: The build tool and development server.
  - `tailwindcss`: The utility-first CSS framework for styling.
- **Integrations:**
  - **Database:** Supabase (PostgreSQL) as the hosted database provider.
  - **Deployment:** Vercel (Frontend), Fly.io or similar (Backend).
  - **Project Initialization:** The entire project structure will be created using the `cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql` template.

## Acceptance Criteria (Authoritative)

1.  **(From Story 1.1)** Given the project's approved tech stack (FastAPI, SvelteKit), when the `cookiecutter` command is executed with the specified template, then the project directory is created with separate `frontend` and `backend` folders.
2.  **(From Story 1.1)** And all initial dependencies for both frontend and backend are installed and ready.
3.  **(From Story 1.2)** Given a user is on the registration page, when they enter a valid email and a strong password and submit the form, then a new user record is created in the `users` database table.
4.  **(From Story 1.2)** And the user is automatically logged in and redirected to the main dashboard.
5.  **(From Story 1.2)** And the API returns a JWT token upon successful registration.
6.  **(From Story 1.3)** Given a registered user is on the login page, when they enter their correct credentials and submit the form, then the system validates their credentials and returns a JWT token.
7.  **(From Story 1.3)** And the user is redirected to the main dashboard.
8.  **(From Story 1.3)** When a logged-in user clicks the "Logout" button, then their session is terminated and they are redirected to the login page.

## Traceability Mapping

| AC ID | Spec Section(s) | Component(s)/API(s) | Test Idea |
| :--- | :--- | :--- | :--- |
| 1 | System Architecture Alignment, Dependencies | `cookiecutter` command | Execute the initialization command and verify the generated directory structure matches the architecture. |
| 2 | Dependencies | `package.json`, `pyproject.toml` | Run dependency installation commands (`npm install`, `pip install`) in their respective folders and ensure they complete without errors. |
| 3 | Data Models, APIs | `POST /api/v1/users`, `users` table | Send a valid registration request via an API client and query the database directly to confirm the new user record was created with a hashed password. |
| 4 | Workflows and Sequencing | Frontend `auth.ts` store | In an end-to-end test, simulate a user registration and assert that the browser's final URL is the dashboard page. |
| 5 | APIs and Interfaces | `POST /api/v1/users` | Inspect the network response after a successful registration to confirm a valid JWT token is returned. |
| 6 | APIs and Interfaces | `POST /api/v1/auth/login` | Send a valid login request with correct credentials and verify a JWT token is returned in the response. |
| 7 | Workflows and Sequencing | Frontend `auth.ts` store | In an end-to-end test, simulate a user login and assert that the browser's final URL is the dashboard page. |
| 8 | Workflows and Sequencing | Frontend `auth.ts`, Logout UI element | In an end-to-end test, log in, click the logout button, and assert that the session storage/token is cleared and the user is redirected to the login page. |

## Risks, Assumptions, Open Questions

- **Risk:** The chosen `cookiecutter` starter template may have outdated dependencies or undiscovered vulnerabilities.
  - **Mitigation:** After initialization, immediately run dependency audit tools (e.g., `npm audit`, `pip-audit`) and review the template's GitHub repository for recent issues before beginning development.
- **Assumption:** The `cookiecutter` template will function as documented and scaffold the project without requiring significant manual fixes or configuration.
- **Assumption:** The development environment has all prerequisite tools (Python, Node.js, Docker, cookiecutter) installed and correctly configured.
- **Question:** What are the specific password strength requirements (e.g., minimum length, character types, complexity)? This needs to be clarified before implementation to ensure both frontend and backend validation rules are consistent.

## Test Strategy Summary

Given that automated testing frameworks were not included in the initial setup, this epic will be validated through a combination of API-level and manual end-to-end testing.

- **API-Level Testing:** The backend endpoints (`/users`, `/auth/login`) will be tested directly using an API client (e.g., Postman, Insomnia). This will verify correct responses for valid data, error handling for invalid data (e.g., duplicate email), and proper JWT token issuance.
- **Manual End-to-End Testing:** The full user flows will be tested in a browser to ensure frontend and backend are integrated correctly. This includes:
  - **Happy Path:** Successfully registering a new user, logging out, and logging back in.
  - **Negative Path:** Attempting to register with an email that is already in use.
  - **Negative Path:** Attempting to log in with an incorrect password.
  - **Session Management:** Verifying that a logged-in user is redirected from the login page and that a logged-out user cannot access protected routes.
- **Coverage:** This strategy directly covers all acceptance criteria for the epic.
