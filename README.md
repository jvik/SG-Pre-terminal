# Excelence - Personal Budget Management

A modern full-stack budget management application built with FastAPI and SvelteKit.

## 🌐 Production Environment

**Live Application**: [https://excelence.bitbu.no](https://excelence.bitbu.no)

The application is deployed using:
- **Frontend**: Vercel (SvelteKit)
- **Backend**: Render (FastAPI)
- **Database**: Supabase (PostgreSQL)

### Features
- User authentication (register/login)
- Transaction management (income & expenses)
- Category management
- Financial dashboard with visualizations
- Budget data export (CSV/JSON)
- Real-time budget tracking

## 🚀 Local Development

### Prerequisites

- **Python 3.11+** with [uv](https://github.com/astral-sh/uv) installed
- **Node.js 18+** with npm
- **Just** command runner (optional but recommended)
- **Supabase account** for database

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/IBE160/SG-Pre-terminal.git
   cd SG-Pre-terminal
   ```

2. **Configure Backend**
   
   Create `excelence/backend/.env`:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-service-role-key
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   CORS_ORIGINS=http://localhost:5173
   ```
   
   Get Supabase credentials from: Supabase Dashboard → Settings → API

3. **Configure Frontend**
   
   Create `excelence/frontend/.env`:
   ```env
   PUBLIC_API_URL=http://localhost:8000
   ```

### Installation

#### Using Just (Recommended)

```bash
# Install all dependencies
just install

# Start both frontend and backend
just dev
```

#### Manual Installation

**Backend:**
```bash
cd excelence/backend
uv venv
uv pip install -e ".[dev]"
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd excelence/frontend
npm install
npm run dev
```

### Available Commands (with Just)

```bash
just dev              # Start both frontend and backend
just dev-backend      # Start backend only (port 8000)
just dev-frontend     # Start frontend only (port 5173)
just test             # Run all tests
just test-backend     # Run backend tests
just test-frontend    # Run frontend tests
just lint             # Lint all code
just format           # Format all code
just clean            # Clean build artifacts
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
excelence/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── crud/     # Database operations
│   │   ├── models/   # Data models
│   │   └── schemas/  # Pydantic schemas
│   ├── tests/        # Backend tests
│   └── main.py       # Application entry point
│
└── frontend/         # SvelteKit frontend
    ├── src/
    │   ├── lib/      # Components & services
    │   └── routes/   # Page routes
    └── static/       # Static assets
```

## 🔧 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database & authentication
- **Pydantic** - Data validation
- **Python-Jose** - JWT token handling
- **uvicorn** - ASGI server

### Frontend
- **SvelteKit** - Frontend framework
- **TailwindCSS** - Styling
- **Chart.js** - Data visualization
- **TypeScript** - Type safety

## 📚 Documentation

- [Deployment Guide](./DEPLOYMENT.md) - How to deploy to production
- [Product Requirements](./docs/PRD.md) - Product specifications
- [Technical Architecture](./docs/architecture.md) - System design
- [Sprint Artifacts](./docs/sprint-artifacts/) - Development progress

## 🧪 Testing

Run the test suites:

```bash
# All tests
just test

# Backend only
just test-backend

# Frontend only
just test-frontend
```

## 🤝 Contributing

This is a student project for IBE160 - Programming with AI at Western Norway University of Applied Sciences.

## 📝 License

This project is part of academic coursework.

## 🆘 Troubleshooting

### Backend won't start
- Verify `.env` file exists with correct Supabase credentials
- Check Python version: `python --version` (requires 3.11+)
- Install uv: `pip install uv`

### Frontend won't start
- Check Node version: `node --version` (requires 18+)
- Clear node_modules: `rm -rf node_modules && npm install`

### CORS errors
- Ensure `CORS_ORIGINS` in backend `.env` includes your frontend URL
- Check `PUBLIC_API_URL` in frontend `.env` points to backend

### Database connection issues
- Verify Supabase credentials are correct
- Check if you're using `service_role` key (not `anon` key)
- Ensure database tables are created in Supabase

For deployment issues, see [DEPLOYMENT.md](./DEPLOYMENT.md).
