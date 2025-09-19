# Bulk Invite + Email Notification Flow

A simple, repeatable checklist for importing users into LiteLLM and emailing their credentials.

Last validated: 2025-09-18

---

## 0) Prereqs
- Team exists in LiteLLM (or create it first) and you know the team ID(s)
- Gmail: you have OAuth client JSON and can authenticate once
- Repo paths (relative to `contact/src/`):
  - Credentials JSON in `../credentials/` or directly in `./`
  - CSVs in `../files/`
  - Templates in `../templates/`
  - Logs in `../logs/`

---

## 1) Prepare the import CSV for LiteLLM
- Start from the template: `contact/templates/bulk_users_template.csv`
- Required columns: `user_email`, `user_role`
- Optional columns: `teams`, `max_budget`, `budget_duration`, `models`
- Example row for all-permissions on a team (no restrictions):
  
  user_email,user_role,teams,max_budget,budget_duration,models
  user@example.com,internal_user,TEAM_ID,,,

- Save your filled file to `contact/files/your_bulk_users.csv`

---

## 2) Import users in LiteLLM
- Use the LiteLLM UI/API to bulk import using your CSV
- After completion, download the results CSV (contains keys/links)
- Save the results CSV to `contact/files/your_bulk_users_results.csv`

---

## 3) Configure the email sender
- Copy `contact/src/.env.example` to `contact/src/.env`
- Set these keys (paths are relative to `contact/src/`):
  - CLIENT_SECRETS_PATH=../credentials/client_secret_XXXX.json
  - TOKEN_PATH=../credentials/token.json
  - CSV_PATH=../files/your_bulk_users_results.csv  ← main input with keys/links
  - RESULTS_CSV_PATH=  (leave empty unless you want to merge a second CSV)
  - SUBJECT=Your access to modelos.ai.ulusofona.pt
  - BODY_FILE=../templates/welcome_with_credentials.txt
  - SENDER=your-email@ulusofona.pt
  - DRY_RUN=true   ← preview first

- Template placeholders supported: `{user_email}`, `{teams}`, `{key}`, `{invitation_link}`

---

## 4) Run and verify
From `contact/src/`:

1) Create/activate venv (first time):
- python3 -m venv ../venv
- source ../venv/bin/activate
- pip install -r requirements.txt

2) Dry-run:
- ./run.sh
- Check the printed previews and `../logs/bulk_email_log.csv`

3) Send for real:
- Set `DRY_RUN=false` in `.env`
- ./run.sh
- Verify outcomes in the log

---

## 5) Troubleshooting
- Client secrets not found: check `CLIENT_SECRETS_PATH` matches the actual JSON filename
- Re-auth: delete `../credentials/token.json` and run again
- Gmail API errors: ensure Gmail API is enabled and scope `gmail.send` is on consent screen
- CSV not merging: only needed if using both `CSV_PATH` and `RESULTS_CSV_PATH`; merge key is `user_email`
- Placeholders empty: ensure your CSV has the columns used in the template (e.g., `key`, `invitation_link`, `teams`)
- Duplicates: keep `DEDUPE=true` to avoid re-sending in the same run
- Rate limits: adjust `SLEEP_BETWEEN_SENDS` (e.g., 0.5–1.0s)

---

## Quick reference
- Main script: `contact/src/litellm_bulk_sender.py`
- Runner: `contact/src/run.sh`
- Env file: `contact/src/.env`
- Template: `contact/templates/welcome_with_credentials.txt`
- Logs: `contact/logs/bulk_email_log.csv`
