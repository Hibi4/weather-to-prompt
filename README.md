# website-to-prompts

Transforme un site web en prompts et blueprints réutilisables pour l’IA.

## Structure

```
website-to-prompts/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
└── frontend/          # Application React (Vite + TypeScript + Tailwind)
```

## Démarrage rapide

1. Copier les variables d’environnement :

```bash
cp .env.example .env
```

2. Installer et lancer le frontend :

```bash
cd frontend
npm install
npm run dev
```

L’application est disponible sur [http://localhost:5173](http://localhost:5173).

## Docker

```bash
docker compose up --build
```

## Pages

| Route | Description |
| --- | --- |
| `/` | Accueil et saisie d’URL |
| `/login` | Authentification |
| `/dashboard` | Blueprints générés |
| `/blueprint/:id` | Détail d’un blueprint |
