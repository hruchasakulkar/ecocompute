
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Make the project root available for backend imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.sql_manager import SQLConnector
from backend.mongo_manager import MongoConnector


st.set_page_config(
    page_title="EcoCompute Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 EcoCompute")
st.subheader("Data Center Monitoring Dashboard")


@st.cache_resource
def get_sql_connector():
    connector = SQLConnector()
    connector.connect()
    return connector


@st.cache_resource
def get_mongo_connector():
    connector = MongoConnector()
    connector.connect()
    return connector


sql = get_sql_connector()
mongo = get_mongo_connector()

sql_connected = (
    sql.connection is not None
    and sql.connection.is_connected()
)

mongo_connected = mongo.database is not None

st.sidebar.subheader("Database Status")
if sql_connected:
    st.sidebar.success("MySQL Connected")
else:
    st.sidebar.error("MySQL Unavailable")

if mongo_connected:
    st.sidebar.success("MongoDB Connected")
else:
    st.sidebar.error("MongoDB Unavailable")


page = st.sidebar.selectbox(
    "Navigate",
    [
        "Overview",
        "Server Telemetry",
        "Maintenance Logs",
        "Rack and Zone Details"
    ]
)


def display_data(df):
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found, or the query returned no data.")


@st.cache_data(ttl=60)
def load_telemetry(hours=48):
    # Use the existing backend connector and aggregation pipeline.
    return mongo.get_hourly_telemetry(hours=hours)


if page == "Overview":
    st.header("Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    if sql_connected:
        logs = sql.get_maintenance_details()
        statuses = sql.get_logs_by_status()
        racks = sql.get_high_power_racks()

        total_logs = len(logs) if not logs.empty else 0
        total_statuses = (
            int(statuses["total_logs"].sum())
            if not statuses.empty else 0
        )

        col1.metric("Maintenance Records", total_logs)
        col2.metric("High-Power Racks", len(racks))
        col3.metric("Logged Status Counts", total_statuses)

        st.subheader("Maintenance Status Summary")
        display_data(statuses)

        st.subheader("High-Power Server Racks")
        display_data(racks)
    else:
        st.warning(
            "MySQL is unavailable. Check your local .env settings "
            "and confirm that the MySQL service is running."
        )

    st.divider()
    st.subheader("Telemetry Snapshot")

    if mongo_connected:
        telemetry = load_telemetry(48)

        if not telemetry.empty:
            latest_hour = telemetry["hour"].max()
            latest = telemetry[telemetry["hour"] == latest_hour]

            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Average Temperature",
                f"{latest['avg_temperature_c'].mean():.1f} °C"
            )
            c2.metric(
                "Average Power Draw",
                f"{latest['avg_power_draw_kw'].mean():.1f} kW"
            )
            c3.metric(
                "Average CPU Usage",
                f"{latest['avg_cpu_usage_pct'].mean():.1f}%"
            )
            st.caption(
                f"Snapshot from {latest_hour}. Values are averages "
                "across racks with readings in that hour."
            )
        else:
            st.info("No telemetry results were returned for the last 48 hours.")
    else:
        st.warning(
            "MongoDB is unavailable. Check atlas-credentials.env "
            "and your Atlas network access."
        )


elif page == "Server Telemetry":
    st.header("Server Telemetry")
    st.caption("Hourly rack-level averages from MongoDB Atlas.")

    hours = st.selectbox(
        "Time window",
        [6, 12, 24, 48],
        index=3,
        format_func=lambda h: f"Last {h} hours"
    )

    if mongo_connected:
        telemetry = load_telemetry(hours)

        if not telemetry.empty:
            rack_options = sorted(telemetry["rack_name"].dropna().unique())
            selected_racks = st.multiselect(
                "Filter by rack",
                options=rack_options,
                default=rack_options
            )

            filtered = telemetry[
                telemetry["rack_name"].isin(selected_racks)
            ].copy()

            if filtered.empty:
                st.info("No telemetry data matches the selected racks.")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric(
                    "Average Temperature",
                    f"{filtered['avg_temperature_c'].mean():.2f} °C"
                )
                c2.metric(
                    "Average Power Draw",
                    f"{filtered['avg_power_draw_kw'].mean():.2f} kW"
                )
                c3.metric(
                    "Average CPU Usage",
                    f"{filtered['avg_cpu_usage_pct'].mean():.2f}%"
                )

                st.subheader("Temperature Over Time")
                temperature_chart = filtered.pivot_table(
                    index="hour",
                    columns="rack_name",
                    values="avg_temperature_c",
                    aggfunc="mean"
                )
                st.line_chart(temperature_chart)

                st.subheader("Power Draw Over Time")
                power_chart = filtered.pivot_table(
                    index="hour",
                    columns="rack_name",
                    values="avg_power_draw_kw",
                    aggfunc="mean"
                )
                st.line_chart(power_chart)

                st.subheader("CPU Usage Over Time")
                cpu_chart = filtered.pivot_table(
                    index="hour",
                    columns="rack_name",
                    values="avg_cpu_usage_pct",
                    aggfunc="mean"
                )
                st.line_chart(cpu_chart)

                st.subheader("Hourly Telemetry Records")
                display_data(filtered)
        else:
            st.info(
                "No telemetry records found for this time window. "
                "Try a longer time window or check the Atlas collection."
            )
    else:
        st.error(
            "MongoDB is unavailable. Verify atlas-credentials.env, "
            "database credentials, and Atlas Network Access."
        )


elif page == "Maintenance Logs":
    st.header("Maintenance Logs")

    if sql_connected:
        logs = sql.get_maintenance_details()

        if logs is not None and not logs.empty:
            if "status" in logs.columns:
                statuses = sorted(logs["status"].dropna().unique())
                selected_statuses = st.multiselect(
                    "Filter by status",
                    options=statuses,
                    default=statuses
                )
                logs = logs[logs["status"].isin(selected_statuses)]

        display_data(logs)
    else:
        st.error("Connect to MySQL to view maintenance records.")


elif page == "Rack and Zone Details":
    st.header("Rack and Zone Details")

    if sql_connected:
        st.subheader("Racks Above Their Zone's Average Power")
        display_data(sql.get_high_power_racks())

        st.subheader("Maintenance Statuses with at least 3 Logs")
        display_data(sql.get_busy_statuses())
    else:
        st.error("Connect to MySQL to view rack and zone information.")
