

import streamlit as st

import pandas as pd

from src.energy.solar_model import generate_solar_profile

from src.workload.ai_workload import AIWorkload

from src.optimizer.scheduler import schedule_multiple_workloads

from src.analytics.energy_impact import (

    calculate_baseline_energy,

    calculate_optimized_energy

)

from src.analytics.carbon_impact import calculate_carbon_impact

from src.analytics.cost_impact import calculate_cost_impact

st.set_page_config(

    page_title="SolarOjas AI",

    page_icon="☀️",

    layout="wide"

)

st.title("☀️ SolarOjas AI")

st.subheader("Renewable-Aware AI Computing & Energy Optimization")

st.write(

    "Configure AI workloads, optimize their schedules using "

    "simulated solar availability, and compare estimated "

    "energy, carbon, and electricity cost impacts."

)

DEFAULT_WORKLOADS = [

    {

        "name": "AI Model Training",

        "power_required": 15.0,

        "duration": 2,

        "earliest_start": 8,

        "deadline": 18

    },

    {

        "name": "LLM Inference",

        "power_required": 8.0,

        "duration": 3,

        "earliest_start": 6,

        "deadline": 20

    },

    {

        "name": "Data Processing",

        "power_required": 12.0,

        "duration": 2,

        "earliest_start": 7,

        "deadline": 17

    },

    {

        "name": "Model Fine-Tuning",

        "power_required": 20.0,

        "duration": 2,

        "earliest_start": 9,

        "deadline": 19

    }

]

if "workloads" not in st.session_state:

    st.session_state.workloads = [

        job.copy() for job in DEFAULT_WORKLOADS

    ]

if "optimized_workloads" not in st.session_state:

    st.session_state.optimized_workloads = [

        job.copy() for job in DEFAULT_WORKLOADS

    ]

st.sidebar.header("⚙️ Simulation Settings")

electricity_rate = st.sidebar.number_input(

    "Electricity Price ($/kWh)",

    min_value=0.0,

    value=0.12,

    step=0.01,

    format="%.2f"

)

carbon_factor = st.sidebar.number_input(

    "Grid Carbon Intensity (tCO₂/MWh)",

    min_value=0.0,

    value=0.40,

    step=0.05,

    format="%.2f"

)

st.sidebar.info(

    "This application uses simulated solar generation "

    "and workload data. Results are estimates."

)

st.divider()

st.header("🧠 Interactive AI Workload Management")

st.write(

    "Edit workloads in the table below. You can add new rows "

    "or delete existing rows."

)

edited_df = st.data_editor(

    pd.DataFrame(st.session_state.workloads),

    num_rows="dynamic",

    width="stretch",

    hide_index=True,

    column_config={

        "name": st.column_config.TextColumn(

            "Workload Name",

            required=True

        ),

        "power_required": st.column_config.NumberColumn(

            "Power (MW)",

            min_value=0.1,

            step=1.0,

            required=True

        ),

        "duration": st.column_config.NumberColumn(

            "Duration (hours)",

            min_value=1,

            max_value=24,

            step=1,

            required=True

        ),

        "earliest_start": st.column_config.NumberColumn(

            "Earliest Start (hour)",

            min_value=0,

            max_value=23,

            step=1,

            required=True

        ),

        "deadline": st.column_config.NumberColumn(

            "Deadline (hour)",

            min_value=1,

            max_value=24,

            step=1,

            required=True

        )

    },

    key="workload_editor"

)

col_run, col_reset = st.columns([2, 1])

with col_run:

    run_clicked = st.button(

        "🚀 Run Optimization",

        type="primary",

        width="stretch"

    )

with col_reset:

    reset_clicked = st.button(

        "Reset Workloads",

        width="stretch"

    )

if reset_clicked:

    st.session_state.workloads = [

        job.copy() for job in DEFAULT_WORKLOADS

    ]

    st.session_state.optimized_workloads = [

        job.copy() for job in DEFAULT_WORKLOADS

    ]

    st.session_state.pop("workload_editor", None)

    st.rerun()

if run_clicked:

    proposed = edited_df.to_dict("records")

    errors = []

    if not proposed:

        errors.append("Add at least one workload.")

    for index, job in enumerate(proposed, start=1):

        try:

            name = str(job["name"]).strip()

            power = float(job["power_required"])

            duration = int(job["duration"])

            earliest = int(job["earliest_start"])

            deadline = int(job["deadline"])

            if not name or name.lower() in ("none", "nan"):

                raise ValueError("Workload name is required.")

            if power <= 0:

                raise ValueError("Power must be positive.")

            if duration < 1 or duration > 24:

                raise ValueError("Duration must be 1–24 hours.")

            if earliest < 0 or earliest > 23:

                raise ValueError("Earliest start must be 0–23.")

            if deadline < 1 or deadline > 24:

                raise ValueError("Deadline must be 1–24.")

            if earliest + duration > deadline:

                raise ValueError(

                    "Earliest start + duration must not exceed deadline."

                )

        except (ValueError, TypeError, KeyError) as error:

            errors.append(f"Row {index}: {error}")

    if errors:

        for error in errors:

            st.error(error)

    else:

        st.session_state.workloads = proposed

        st.session_state.optimized_workloads = [

            job.copy() for job in proposed

        ]

        st.session_state.optimization_message = "Optimization updated successfully!"
        st.rerun()

# Make the active inputs visible, so a stale calculation is easy to spot.
if st.session_state.get("optimization_message"):
    st.success(st.session_state.pop("optimization_message"))

active_df = pd.DataFrame(st.session_state.optimized_workloads)
active_energy = sum(
    float(job["power_required"]) * int(job["duration"])
    for job in st.session_state.optimized_workloads
)
st.caption(f"Currently calculated from {len(active_df)} workload(s); "
           f"total requested energy: {active_energy:.1f} MWh. "
           "Click Run Optimization to apply edits.")

ai_jobs = [

    AIWorkload(

        name=job["name"],

        power_required=float(job["power_required"]),

        duration=int(job["duration"]),

        earliest_start=int(job["earliest_start"]),

        deadline=int(job["deadline"])

    )

    for job in st.session_state.optimized_workloads

]

solar_profile = generate_solar_profile()

results = schedule_multiple_workloads(

    solar_profile,

    ai_jobs

)

records = []

analytics_results = []

for job, start, solar, grid, coverage in results:

    if start is None:

        continue

    energy = job.power_required * job.duration

    records.append({

        "Workload": job.name,

        "Start": f"{start:02d}:00",

        "End": f"{start + job.duration:02d}:00",

        "Energy (MWh)": energy,

        "Solar (MWh)": solar,

        "Grid (MWh)": grid,

        "Renewable Coverage (%)": coverage

    })

    analytics_results.append({

        "energy_required": energy,

        "solar_used": solar,

        "grid_used": grid

    })

if len(records) != len(ai_jobs):

    st.error("One or more workloads could not be scheduled.")

    st.stop()

df = pd.DataFrame(records)

baseline = calculate_baseline_energy(

    solar_profile,

    ai_jobs

)

optimized = calculate_optimized_energy(

    analytics_results

)

carbon_data = calculate_carbon_impact(

    baseline,

    optimized,

    grid_emission_factor=carbon_factor

)

cost_data = calculate_cost_impact(

    baseline,

    optimized,

    electricity_rate=electricity_rate

)

grid_saved = baseline["grid"] - optimized["grid"]

grid_reduction = (

    grid_saved / baseline["grid"] * 100

    if baseline["grid"] > 0 else 0

)

st.divider()

st.header("📊 Energy Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(

    "Total AI Energy",

    f"{optimized['total']:.1f} MWh"

)

col2.metric(

    "Solar Energy Used",

    f"{optimized['solar']:.1f} MWh"

)

col3.metric(

    "Grid Energy Used",

    f"{optimized['grid']:.1f} MWh"

)

col4.metric(

    "Renewable Coverage",

    f"{optimized['renewable_percentage']:.1f}%"

)

st.divider()

st.header("☀️ Solar Energy Availability")

solar_df = pd.DataFrame({

    "Hour": list(range(24)),

    "Solar Power (MW)": solar_profile

})

st.line_chart(solar_df.set_index("Hour"))

st.divider()

st.header("🧠 Optimized AI Workload Schedule")

st.dataframe(

    df,

    width="stretch",

    hide_index=True

)

st.divider()

st.header("⚡ Workload Energy Distribution")

st.bar_chart(

    df.set_index("Workload")[

        ["Solar (MWh)", "Grid (MWh)"]

    ]

)

st.divider()

st.header("🔄 Baseline vs. SolarOjas")

comparison_df = pd.DataFrame({

    "Scenario": [

        "Without SolarOjas",

        "With SolarOjas"

    ],

    "Solar Energy (MWh)": [

        baseline["solar"],

        optimized["solar"]

    ],

    "Grid Energy (MWh)": [

        baseline["grid"],

        optimized["grid"]

    ]

})

st.dataframe(

    comparison_df,

    width="stretch",

    hide_index=True

)

st.bar_chart(

    comparison_df.set_index("Scenario")

)

st.divider()

st.header("🌱 Energy Savings")

col1, col2, col3 = st.columns(3)

col1.metric(

    "Grid Energy Saved",

    f"{grid_saved:.1f} MWh"

)

col2.metric(

    "Grid Energy Reduction",

    f"{grid_reduction:.1f}%"

)

col3.metric(

    "Renewable Coverage Improvement",

    (

        f"{optimized['renewable_percentage'] - baseline['renewable_percentage']:.1f} pp"

    )

)

st.divider()

st.header("🌍 Carbon Impact")

col1, col2, col3 = st.columns(3)

col1.metric(

    "Baseline CO₂",

    f"{carbon_data['baseline_emissions']:.2f} t"

)

col2.metric(

    "Optimized CO₂",

    f"{carbon_data['optimized_emissions']:.2f} t"

)

col3.metric(

    "Estimated CO₂ Avoided",

    f"{carbon_data['emissions_avoided']:.2f} t"

)

st.divider()

st.header("💰 Electricity Cost Impact")

col1, col2, col3 = st.columns(3)

col1.metric(

    "Baseline Grid Cost",

    f"${cost_data['baseline_cost']:,.2f}"

)

col2.metric(

    "Optimized Grid Cost",

    f"${cost_data['optimized_cost']:,.2f}"

)

col3.metric(

    "Estimated Cost Savings",

    f"${cost_data['cost_saved']:,.2f}"

)

st.caption(

    "Simulation estimates only. Costs exclude solar generation, "

    "storage, infrastructure, demand charges, and operating expenses. "

    "The greedy scheduler does not guarantee a globally optimal schedule."

)

st.divider()

st.success("SolarOjas AI simulation completed successfully.")
