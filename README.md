# logistics

## Pre-requests
[uv - Python package and project manager](https://docs.astral.sh/uv/getting-started/installation/) \
[gh - GitHub CLI](https://cli.github.com/)

## Setup

### Clone the repo
```bash
git clone git@github.com:yehor-core/logistics.git
cd logistics
```

### Install dependencies
```bash
uv sync
uv run pre-commit install
```

### Bot creation
1. In telegarm find `@BotFather`
2. Create your own bot
3. Save API token

### Enironment setup
1. Copy-paste `.env.example` and rename it to `.env`
```bash
cp .env.example .env
```
2. Fillout .env with API token and handler from `@BotFather`

### Run
```bash
uv run logistics
```