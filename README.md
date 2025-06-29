# ❄️ FlakeCheck

FlakeCheck is an open-source tool to audit Snowflake health and optimize cost with simple CLI execution.

## 🚀 How to Run

1. Fill in your Snowflake credentials in `config.yaml`
2. Run the tool using the provided shell script:

```bash
./run_flakecheck.sh
```

## 📂 Config Example

```yaml
auth_method: externalbrowser  # or 'keypair'

snowflake:
  account: your_account
  user: your_user
  warehouse: COMPUTE_WH
  database: YOUR_DB
  schema: PUBLIC

keypair:
  private_key_path: /path/to/private_key.pk8
  private_key_passphrase: your_passphrase
```
