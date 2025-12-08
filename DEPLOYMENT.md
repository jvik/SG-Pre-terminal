# Deployment Guide - Excelence

Dette dokumentet beskriver hvordan du deployer Excelence frontend og backend når du ikke eier GitHub-organisasjonen.

## Oversikt

- **Frontend**: SvelteKit → Vercel (gratis)
- **Backend**: FastAPI → Render (gratis tier)
- **Database**: Supabase (allerede konfigurert)
- **Auto-sync**: GitHub Actions synkroniserer fork automatisk

## Steg 1: Fork repoet

1. Gå til https://github.com/IBE160/SG-Pre-terminal
2. Klikk "Fork" øverst til høyre
3. Velg din personlige GitHub-konto som eier
4. Klikk "Create fork"

Din fork vil nå være på: `https://github.com/DIN_BRUKER/SG-Pre-terminal`

## Steg 2: Auto-sync er allerede konfigurert

Filen `.github/workflows/sync-fork.yml` er allerede i repoet og vil:
- Synkronisere med upstream (IBE160/SG-Pre-terminal) hver 6. time
- Kunne kjøres manuelt fra GitHub Actions UI
- Automatisk pushe endringer til din fork

**Første gang**: Workflow aktiveres automatisk når du forker. Sjekk under "Actions" i din fork.

## Steg 3: Deploy Frontend til Vercel

### 3.1 Opprett Vercel-konto
1. Gå til https://vercel.com
2. Logg inn med GitHub-kontoen din

### 3.2 Koble til fork
1. Klikk "Add New" → "Project"
2. Velg din fork: `DIN_BRUKER/SG-Pre-terminal`
3. Klikk "Import"

### 3.3 Konfigurer prosjektet
- **Framework Preset**: SvelteKit
- **Root Directory**: `excelence/frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.svelte-kit/vercel/output` (automatisk)
- **Install Command**: `npm install`

### 3.4 Legg til environment variables

**VIKTIG**: Du må først deploye backend (se Steg 4) før du setter denne verdien!

Klikk "Environment Variables" og legg til:

```env
PUBLIC_API_URL=https://excelence-backend.onrender.com
```

(Erstatt med din faktiske Render backend URL)

**Merk**: Supabase håndteres av backend, så du trenger ikke Supabase-variabler her.

### 3.5 Deploy
1. Klikk "Deploy"
2. Vent ~2 minutter
3. Frontend er nå live på `https://din-app.vercel.app`

## Steg 4: Deploy Backend til Render

### 4.1 Opprett Render-konto
1. Gå til https://render.com
2. Logg inn med GitHub-kontoen din

### 4.2 Koble til fork
1. Klikk "New" → "Blueprint"
2. Velg din fork: `DIN_BRUKER/SG-Pre-terminal`
3. Render vil automatisk finne `render.yaml`

### 4.3 Konfigurer environment variables

Render vil be om disse verdiene (definert i `render.yaml`):

```env
SUPABASE_URL=https://din-supabase-url.supabase.co
SUPABASE_KEY=din-service-role-key
CORS_ORIGINS=https://din-app.vercel.app
```

**Viktig**: 
- Bruk **service_role** key fra Supabase (ikke anon key!)
- Hent fra: Supabase dashboard → Settings → API → `service_role` secret
- `CORS_ORIGINS` må matche din Vercel URL nøyaktig (får du etter Vercel deployment)

### 4.4 Deploy
1. Klikk "Apply"
2. Vent ~5 minutter (første bygg tar litt tid)
3. Backend er nå live på `https://excelence-backend.onrender.com`

## Steg 5: Oppdater CORS og API URL

### 5.1 Oppdater backend CORS

Backend CORS er allerede konfigurert via `CORS_ORIGINS` som du satte i steg 4.3.

**Hvis du trenger å endre det senere:**

1. Gå til Render dashboard → din service → Environment
2. Rediger `CORS_ORIGINS` til å matche din Vercel URL
3. Render vil auto-redeploy

### 5.2 Oppdater frontend API URL

Nå som backend er deployet, få backend URL fra Render og legg til i Vercel:

1. Kopier backend URL fra Render (f.eks. `https://excelence-backend.onrender.com`)
2. Gå til Vercel → Settings → Environment Variables
3. Legg til:

```env
PUBLIC_API_URL=https://excelence-backend.onrender.com
```

4. Velg Production, Preview, Development
5. Save
6. Redeploy frontend (Deployments → tre prikker → Redeploy)

## Steg 6: Test deployment

1. Gå til din Vercel URL: `https://din-app.vercel.app`
2. Test registrering av ny bruker
3. Test innlogging
4. Sjekk at API-kall fungerer

## Automatisk deployment fremover

### Auto-deploy ved endringer
- **Frontend (Vercel)**: Deployer automatisk ved push til `main`
- **Backend (Render)**: Deployer automatisk ved push til `main`
- **Fork sync**: Synkroniserer automatisk hver 6. time

### Manuell sync av fork
Hvis du vil synkronisere umiddelbart:
1. Gå til din fork på GitHub
2. Klikk "Actions"
3. Velg "Sync Fork with Upstream"
4. Klikk "Run workflow"

## Kostnader

- **Vercel**: Gratis tier (100 GB bandwidth/måned)
- **Render**: Gratis tier (750 timer/måned, sovner etter 15 min inaktivitet)
- **Supabase**: Gratis tier (500 MB database, 50k monthly active users)

**Viktig**: Render free tier sovner etter inaktivitet. Første request etter søvn tar ~30 sekunder.

## Troubleshooting

### Backend sovner på Render
**Problem**: Backend tar lang tid å svare første gang.
**Løsning**: 
- Oppgrader til Render betalt plan ($7/mnd)
- Eller sett opp cron-job som pinger backend hvert 10. minutt

### CORS-feil
**Problem**: Frontend kan ikke nå backend.
**Løsning**: Sjekk at `CORS_ORIGINS` i Render matcher din Vercel URL nøyaktig.

### Environment variables mangler
**Problem**: Supabase-kall feiler.
**Løsning**: Dobbeltsjekk at alle environment variables er satt både i Vercel og Render.

### Fork ikke synkroniserer
**Problem**: Endringer fra upstream kommer ikke til fork.
**Sjekk**: 
1. Gå til Actions i din fork
2. Se om workflow kjører uten feil
3. Sjekk at du ikke har merge conflicts

## Neste steg

- Sett opp custom domain i Vercel
- Konfigurer HTTPS (automatisk i Vercel/Render)
- Sett opp monitoring/logging
- Vurder oppgradering til betalt Render plan for 24/7 uptime

## Support

Hvis du får problemer:
1. Sjekk logs i Vercel/Render dashboard
2. Verifiser environment variables
3. Test API endpoints direkte (f.eks. via curl)
