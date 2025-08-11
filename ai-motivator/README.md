## AI Motivator

A small CLI tool that generates a daily motivational quote and a short description tailored to your company values. Uses OpenAI if available, with a local fallback. Optional Slack posting via webhook. Runs with only the Python standard library.

### Features
- Company-aware quotes and descriptions
- JSON and Markdown output
- Optional Slack posting via webhook
- Works without external Python packages (stdlib only)

### Setup
1. Ensure Python 3.10+ is available on your system
2. Copy `.env.example` to `.env` and set values as needed (optional)
3. Edit `config.yaml` to reflect your company name, tone, themes, and values

### Usage
Generate today's motivation and save to `out/`:
```bash
python3 -m motivator.cli generate --config config.yaml --out-dir out
```

Dry run (prints to console, still writes files):
```bash
python3 -m motivator.cli generate --config config.yaml --out-dir out --dry-run
```

Post to Slack (requires `SLACK_WEBHOOK_URL` in `.env`):
```bash
python3 -m motivator.cli generate --config config.yaml --out-dir out --post-slack
```

Environment loading: the CLI will load variables from `.env` if present (simple KEY=VALUE lines).

### Automation (cron)
Add a daily job at 8:55am local time:
```cron
55 8 * * * cd /workspace/ai-motivator && python3 -m motivator.cli generate --config config.yaml --out-dir out --post-slack >> cron.log 2>&1
```

### Configuration
See `config.yaml` for fields. You can also override via env vars:
- `OPENAI_API_KEY`, `OPENAI_MODEL` (e.g., `gpt-4o-mini`)
- `SLACK_WEBHOOK_URL`
- `TZ` (e.g., `UTC` or `America/New_York`)

### Output
- `out/YYYY-MM-DD.json`
- `out/YYYY-MM-DD.md`

### License
MIT