# Bulk Invite Users

## 1. Download and fill the template

Add multiple users at once by following these steps:

1. Download our CSV template
2. Add your users' information to the spreadsheet
3. Save the file and upload it here
4. After creation, download the results file containing the API keys for each user

## Template Column Names

### Required Fields

- **user_email** *(required)*
  - User's email address

- **user_role** *(required)*
  - User's role (one of: "proxy_admin", "proxy_admin_view_only", "internal_user", "internal_user_view_only")

### Optional Fields

- **teams**
  - Comma-separated team IDs (e.g., "team-1,team-2")

- **max_budget**
  - Maximum budget as a number (e.g., "100")

- **budget_duration**
  - Budget reset period (e.g., "30d", "1mo")

- **models**
  - Comma-separated allowed models (e.g., "gpt-3.5-turbo,gpt-4")

---

*Download the CSV template to get started with bulk user invitations.*