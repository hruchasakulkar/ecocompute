# EcoCompute

**Data-driven Data Center Monitoring and Maintenance System**

EcoCompute combines structured operational records in MySQL with telemetry documents in MongoDB Atlas. A Streamlit dashboard provides monitoring summaries, telemetry visualizations, and maintenance information.

## Team Responsibilities

- **Member 1 — Relational Architect:** SQL schema, sample operational data, joins, nested subqueries, and stored procedures.
- **Member 2 — NoSQL/Data Engineer:** Telemetry document schema, 1,000+ mock telemetry records, and MongoDB aggregation pipeline.
- **Member 3 — Python/Backend Lead:** Modular SQL and MongoDB connectors, exception handling, and methods returning Pandas DataFrames.
- **Member 4 — UI/Presentation Lead:** Streamlit dashboard, charts, filters, and UI testing.

## Repository Structure

```text
ecocompute/
├── backend/
│   ├── sql_manager.py
│   └── mongo_manager.py
├── db_scripts/
│   ├── schema.sql
│   ├── seed.sql
│   └── advanced_queries.sql
├── frontend/
│   └── app.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Install Python 3.9 or newer.
2. Install MySQL Server and create a database named `ecocompute`.
3. Configure MongoDB Atlas and ensure your IP address is permitted in Atlas Network Access.
4. Configure the local environment files:
   - `.env` for MySQL settings.
   - `atlas-credentials.env` for the MongoDB Atlas connection URI and database name.
5. Activate your virtual environment and install dependencies:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

6. Execute `db_scripts/schema.sql`, followed by `db_scripts/seed.sql`, in MySQL Workbench.
7. Run the examples in `db_scripts/advanced_queries.sql` individually to inspect the results.
8. Start the dashboard from the repository root:

   ```powershell
   python -m streamlit run frontend/app.py
   ```

9. Open the local URL displayed in the terminal by Streamlit.

## Dashboard Features

- **Overview:** MySQL maintenance summaries, high-power racks, and a MongoDB telemetry snapshot.
- **Server Telemetry:** Hourly telemetry averages, time-window selection, rack filters, and temperature, power, and CPU charts.
- **Maintenance Logs:** Maintenance records with status filtering.
- **Rack and Zone Details:** High-power racks and maintenance status summaries.
- **Database Status:** Separate connection indicators for MySQL and MongoDB.

## Security

Never commit `.env`, `atlas-credentials.env`, passwords, or MongoDB connection URIs containing credentials. Use `.env.example` only for placeholder values. Share credentials through a secure method.

## Git Collaboration

Use short-lived task branches and pull requests. Do not commit directly to `main`.

```bash
git switch -c feature/ui-dashboard
# Make and test changes
git add frontend/ README.md .gitignore requirements.txt
git commit -m "Integrate Streamlit monitoring dashboard"
git push -u origin feature/ui-dashboard
```

Open a pull request to `main` and request a teammate's review. After a teammate merges a pull request, synchronize your local branch:

```bash
git switch main
git pull origin main
```

## Report Evidence to Collect

- ER diagram and relational schema.
- Database setup steps and executed DDL.
- Screenshots of sample records and advanced query outputs.
- Stored procedure execution and maintenance record insertion.
- Final dashboard screenshots and usage instructions.
- Test cases, validation results, and known limitations.
