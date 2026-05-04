# Lab 8: End-to-End MVP Delivery — From Idea to Deployed App

**Prerequisites:** Labs 1–7 complete. Node.js installed. A GitHub account. Free accounts on Vercel, Ticketmaster Developer, and Mapbox.
**Estimated time:** 2–4 hours
**What you will have at the end:** A live, deployed web application at a public URL — built with AI, integrated with real APIs, and ready to demo in interviews and hackathons.

---

## Overview

This lab brings everything together. You will take a real project — **OpenPath NearMe** — from a blank folder to a deployed, publicly accessible URL.

OpenPath NearMe is a Bay Area tech event finder. Users enter a city or ZIP code and see nearby tech events on a map with a synced list, powered by the Ticketmaster Discovery API and Mapbox.

The goal is not just to build this specific app. The goal is to learn the workflow: plan → scaffold → integrate → deploy. Once you know this sequence, you can apply it to any project in a hackathon or interview.

---

## Why MVP delivery skills matter

The skill that separates candidates in interviews and hackathons is the ability to ship something real.

- **Hackathons:** 24–48 hours to build a working demo. Teams that ship something win — ideas alone do not.
- **Interviews:** "Show me something you built" is the most powerful interview question. A live app beats a slide deck every time.
- **Conferences:** Lightning talks and demos need a working app. Static slides do not create the same impression.
- **Career growth:** Deployed projects on GitHub show initiative, API integration skills, and the ability to ship.

---

## The Project: OpenPath NearMe

### The problem

Students and professionals who want to attend local tech events have to manually search across five or more websites — Meetup, Eventbrite, Ticketmaster, LinkedIn, Luma — to find what is happening nearby this week. There is no single place to look.

### The MVP solution

A web app where you enter a city or ZIP code and see:
- A map with event markers for the next 14 days
- A synced list of events alongside the map
- Click an event marker → see a detail panel with title, date, venue, and a link to the source
- Falls back to curated sample data if the live API has no results

### Tech stack

| Tool | Role |
|------|------|
| Next.js | React framework with built-in API routes |
| Mapbox | Map rendering and geocoding (city/ZIP → lat/lng) |
| Ticketmaster Discovery API | Live event data |
| Vercel | One-click deployment from GitHub |
| TypeScript | Type-safe code |

---

## Step 1 — Get Your Free API Keys

You need two API keys. Both are free with no credit card required.

**Ticketmaster Discovery API:**

1. Go to https://developer.ticketmaster.com
2. Click **Get Your API Key**
3. Create a free account
4. After logging in, your API key appears on the dashboard
5. Copy the **Consumer Key** — this is your `EVENT_PROVIDER_API_KEY`

**Mapbox:**

1. Go to https://account.mapbox.com
2. Create a free account
3. Your default public token is on the dashboard
4. Copy it — this is your `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN`

Keep both keys ready.

---

## Step 2 — Clone the Starter Repository

The OpenPath NearMe starter is published on GitHub so you do not have to scaffold from scratch. Cloning it and running it locally is your starting point.

```bash
git clone git@github.com:naveenkgrg/openpath-nearme.git
cd openpath-nearme
npm install
```

**Set up environment variables:**

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
EVENT_PROVIDER_API_KEY=your_ticketmaster_consumer_key_here
NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=your_mapbox_public_token_here
```

**Start the development server:**

```bash
npm run dev
```

Open http://localhost:3000 in your browser. You should see the app.

---

## Step 3 — Understand the Architecture

Before extending anything, read through the code and understand how data flows. This is the core skill.

```
User types a city or ZIP
        ↓
Frontend (Next.js page)
        ↓
/api/events route (Next.js API route)
        ↓
Mapbox geocode API → converts city/ZIP to lat/lng
        ↓
Ticketmaster Discovery API → fetches events near that location
        ↓
Normalize & filter → converts raw API response to a consistent shape
        ↓
Returns JSON to the frontend
        ↓
Map + list UI renders the events
```

**Key files to read:**

| File | What it does |
|------|-------------|
| `pages/index.tsx` or `app/page.tsx` | Main page — map and list components |
| `pages/api/events.ts` | API route — receives city input, calls geocode + Ticketmaster |
| `lib/providers/ticketmaster.ts` | Ticketmaster adapter — fetches and normalizes event data |
| `lib/geocode.ts` | Mapbox geocoding — city/ZIP to lat/lng |
| `lib/fallback.ts` | Curated fallback dataset |
| `.env.example` | Template for required environment variables |

---

## Step 4 — Key API Integration Concepts

This lab teaches six patterns that appear in almost every real-world API integration project.

### 1. API Keys and Environment Variables

API keys are sensitive credentials. They must never appear in your code or be committed to Git.

Store them in a `.env` file:

```
API_KEY=your_key_here
```

Access them in code:

```typescript
const apiKey = process.env.API_KEY;
```

The `.env` file is in `.gitignore` — it stays on your machine. The `.env.example` file (no real values) is committed so others know what variables to set.

**Rule:** If a key is in your Git history, rotate it immediately.

### 2. HTTP Requests and JSON Normalization

Fetching from an external API:

```typescript
const response = await fetch(
  `https://app.ticketmaster.com/discovery/v2/events.json?apikey=${apiKey}&latlong=${lat},${lng}&radius=30&unit=miles`
);
const data = await response.json();
```

Raw API responses have inconsistent shapes across different providers. Normalization converts any provider's response into one consistent format your UI expects:

```typescript
// Normalize Ticketmaster event to your app's Event type
function normalize(raw: TicketmasterEvent): Event {
  return {
    id: raw.id,
    title: raw.name,
    lat: parseFloat(raw._embedded.venues[0].location.latitude),
    lng: parseFloat(raw._embedded.venues[0].location.longitude),
    start_at: raw.dates.start.dateTime,
    source_url: raw.url,
  };
}
```

This pattern — provider adapter + normalization — means you can swap Ticketmaster for another event API later by changing only the adapter.

### 3. Geocoding

Geocoding converts a human-readable location (city name or ZIP code) into coordinates (latitude and longitude). Map APIs work with coordinates, not city names.

```typescript
// Mapbox geocoding
const response = await fetch(
  `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(city)}.json?access_token=${token}`
);
const data = await response.json();
const [lng, lat] = data.features[0].center;
```

Location → coordinates is one of the most common patterns in apps that deal with places, addresses, or anything geographic.

### 4. Fallback Design

APIs fail. They return empty results, hit rate limits, or go down. A fallback prevents your UI from showing a broken empty state.

```typescript
try {
  const events = await fetchFromTicketmaster(lat, lng);
  if (events.length === 0) {
    return fallbackEvents; // curated sample data
  }
  return events;
} catch (error) {
  console.error('API error, using fallback:', error);
  return fallbackEvents;
}
```

Fallback design is the difference between amateur and professional code. Never show a broken empty state.

### 5. Deploying to Vercel

Vercel deploys Next.js apps in minutes, with automatic HTTPS and automatic deploys on every push to `main`.

1. Push your code to GitHub: `git push origin main`
2. Go to https://vercel.com and click **Add New Project**
3. Import your repository from GitHub
4. In the **Environment Variables** section, add:
   - `EVENT_PROVIDER_API_KEY` = your Ticketmaster key
   - `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN` = your Mapbox token
5. Click **Deploy**

Your app will be live at a public URL in under 5 minutes.

Every subsequent `git push origin main` will automatically redeploy.

### 6. Rate Limiting

APIs charge per request or impose request limits. A basic rate limiter on your API route protects your key quota and prevents abuse.

```typescript
// Simple in-memory rate limiter (for demo purposes)
const requestCounts = new Map<string, number>();

export default function handler(req, res) {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  const count = requestCounts.get(ip) || 0;

  if (count > 10) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  requestCounts.set(ip, count + 1);
  // continue handling the request...
}
```

This shows production awareness — something interviewers notice.

---

## Step 5 — Build Using AI as Your Pair Programmer

Use Claude (or your preferred AI tool) to extend the app. The five-phase workflow:

### Phase 1 — Plan

Start a new chat with this prompt:

```
I am building a Bay Area tech event finder web app. 
Tech stack: Next.js, TypeScript, Mapbox, Ticketmaster API, Vercel.

The app lets users:
- Enter a city or ZIP code
- See a map with event markers for the next 14 days  
- Click a marker to see event details
- Fall back to curated sample data if the API returns no results

Give me a phased build plan. Output as a PLAN.md file.
```

Review the output. Ask follow-up questions. Save it as `PLAN.md` in your project.

### Phase 2 — Build the shell

```
Create the file structure for this Next.js app:
- pages/index.tsx (main page with map and list)
- pages/api/events.ts (API route)
- lib/providers/ticketmaster.ts (provider adapter)
- lib/geocode.ts (Mapbox geocoding)
- lib/fallback.ts (curated fallback data)
- types/event.ts (Event type definition)

Output each file completely. Use TypeScript.
```

### Phase 3 — Integrate the APIs

```
Complete the Ticketmaster adapter in lib/providers/ticketmaster.ts.
It should:
- Accept lat, lng, and radius as parameters
- Call the Ticketmaster Discovery API
- Normalize each event to the Event type: { id, title, lat, lng, start_at, source_url }
- Return an array of Event objects

Use process.env.EVENT_PROVIDER_API_KEY for the Ticketmaster API key.
Handle errors and return an empty array on failure.
```

### Phase 4 — Connect end-to-end

```
Wire the complete data flow in pages/api/events.ts:
1. Accept a "city" query parameter
2. Call lib/geocode.ts to get lat/lng
3. Call lib/providers/ticketmaster.ts to get events
4. If events array is empty, return lib/fallback.ts data instead
5. Return the events as JSON

Add basic rate limiting: max 10 requests per IP per session.
```

### Phase 5 — Ship

```
Add a /api/health route that returns { status: "ok", timestamp: ... }.
Add basic rate limiting to /api/events.
Write a production deploy checklist as DEPLOY.md.
```

---

## Step 6 — Deploy and Verify

Once the app works locally:

```bash
git add .
git commit -m "Complete MVP — event finder with Ticketmaster and Mapbox"
git push origin main
```

Import to Vercel (if not already connected), add environment variables, and deploy.

Verify your deployment:
- Open the live URL in an incognito window (no local environment)
- Type "San Francisco" and confirm events load on the map
- Click a marker and confirm the detail panel opens
- Click the source link and confirm it goes to a real event page
- Open `/api/health` and confirm it returns `{ "status": "ok" }`

---

## Step 7 — Practice Your Demo and Interview Answers

A live app without a rehearsed demo is a missed opportunity.

### 90-second demo script

1. Open the live URL — not localhost
2. Type "San Francisco" → show the map loading with markers
3. Click a marker → show the detail panel with title, date, venue, source link
4. Click the source link → proves real API data
5. Open your GitHub repo → show the provider adapter pattern in the code

### Interview talking points

**Q: What problem does it solve?**

"Students spend hours manually searching across five different websites to find local tech events. I built one place that surfaces everything on a map."

**Q: What APIs did you integrate?**

"Ticketmaster Discovery API for live event data, Mapbox for geocoding city and ZIP inputs to coordinates, with a curated fallback dataset for resilience."

**Q: How does it handle API failures?**

"The API route uses a provider abstraction with graceful fallback — if the live API fails or returns empty results, the UI serves curated sample data instead of showing a broken empty state."

**Q: How did you deploy it?**

"Push to GitHub, import the repo in Vercel, add environment variables. The app was live in under five minutes with automatic HTTPS and deploys on every push."

**Q: What would you add next?**

"GitHub login with NextAuth to save favorite events, click analytics with Supabase, and broader city coverage beyond the Bay Area."

---

## Extensions for Your Portfolio

After completing the base app, these additions demonstrate progressively more advanced skills:

| Extension | What it shows |
|-----------|--------------|
| Add a city picker dropdown | UX thinking, controlled inputs |
| Filter by event category | State management, UI complexity |
| Email notification signup | User engagement, form handling |
| Click analytics with Supabase | Database integration, observability |
| GitHub login with NextAuth | Authentication, OAuth |
| Additional event API provider | Provider abstraction, multi-source data |

Each extension is a real interview talking point.

---

## Lab Complete

You have:
- Cloned and run a real Next.js application locally
- Understood the end-to-end data flow from user input to map display
- Learned six real API integration patterns: auth, HTTP, normalization, geocoding, fallback, rate limiting
- Used AI as a pair programmer through a five-phase build workflow
- Deployed a live app to a public URL on Vercel
- Prepared a demo script and interview talking points

---

## Resources

- OpenPath NearMe starter: https://github.com/naveenkgrg/openpath-nearme
- Ticketmaster Discovery API docs: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- Mapbox Geocoding API docs: https://docs.mapbox.com/api/search/geocoding/
- Vercel deployment docs: https://vercel.com/docs/deployments/overview
- Next.js API routes docs: https://nextjs.org/docs/pages/building-your-application/routing/api-routes

---

**You have completed all 8 OpenPath labs.**

Your GitHub profile now has:
- Active contribution history
- An open-source contribution (Lab 3)
- A live deployed product (this lab)
- Real API integration skills visible in code

→ For what to do next: `learning_path/STUDENT_JOB_SEEKER_PATH.md`
