# Example Commands: OpenPath Local

These example commands show one practical path from idea to MVP.

## 1. Create the App

```bash
npx create-next-app@latest openpath-local
cd openpath-local
git init
git add .
git commit -m "Initial Next.js app"
```

## 2. Create the GitHub Repo

```bash
gh repo create openpath-local --public --source=. --remote=origin --push
```

If needed, create the repo on GitHub manually and then connect it:

```bash
git remote add origin https://github.com/<your-username>/openpath-local.git
git branch -M main
git push -u origin main
```

## 3. Start Development

```bash
npm run dev
```

Open:

```bash
http://localhost:3000
```

## 4. Use a Simple GitHub Workflow

```bash
git checkout -b feature/search-form
git add .
git commit -m "Add search form"
git push -u origin feature/search-form
gh pr create --fill
```

## 5. Add an API Route

Example file:

```bash
src/app/api/events/route.ts
```

Start with mock JSON data first.

## 6. Optional Database

```bash
npm install @supabase/supabase-js
```

or

```bash
npm install pg
```

## 7. Deploy

```bash
vercel
```

Or import the repo into Vercel from the web UI.

## 8. Verify the MVP

Check:
- homepage loads
- city search works
- events render
- empty state works
- deployed site works
