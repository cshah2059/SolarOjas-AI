from src.energy.solar_model import generate_solar_profile, display_solar_profile
from src.workload.ai_workload import AIWorkload
from src.optimizer.scheduler import schedule_multiple_workloads
from src.analytics.energy_impact import (
    calculate_baseline_energy,
    calculate_optimized_energy,
    display_energy_impact
)
from src.analytics.carbon_impact import (
    calculate_carbon_impact,
    display_carbon_impact
)
from src.analytics.cost_impact import (
    calculate_cost_impact,
    display_cost_impact
)


print("=" * 50)
print("                 SOLAROJAS AI")
print("=" * 50)
print()
print("Renewable-Aware AI Computing & Energy Optimization")
print()

# Generate solar energy profile
solar_profile = generate_solar_profile()

# Display solar energy profile
display_solar_profile(solar_profile)

# Create AI workloads
ai_jobs = [
    AIWorkload(
        name="AI Model Training",
        power_required=15,
        duration=2,
        earliest_start=8,
        deadline=18
    ),

    AIWorkload(
        name="LLM Inference",
        power_required=8,
        duration=3,
        earliest_start=6,
        deadline=20
    ),

    AIWorkload(
        name="Data Processing",
        power_required=12,
        duration=2,
        earliest_start=7,
        deadline=17
    ),

    AIWorkload(
        name="Model Fine-Tuning",
        power_required=20,
        duration=2,
        earliest_start=9,
        deadline=19
    )
]

# Display AI workloads
for job in ai_jobs:
    job.display()

# Optimize workloads using available solar energy
results = schedule_multiple_workloads(
    solar_profile,
    ai_jobs
)

print("\n" + "=" * 50)
print("        SOLAROJAS SCHEDULING RESULTS")
print("=" * 50)

analytics_results = []

for (
    job,
    best_start,
    solar_used,
    grid_used,
    renewable_percentage
) in results:

    best_end = best_start + job.duration
    total_energy = job.power_required * job.duration

    print(f"\nJob:                  {job.name}")
    print("-" * 50)
    print(f"Recommended Start:    {best_start:02d}:00")
    print(f"Recommended End:      {best_end:02d}:00")
    print(f"AI Energy Required:   {total_energy:.1f} MWh")
    print(f"Solar Energy Used:    {solar_used:.1f} MWh")
    print(f"Grid Energy Required: {grid_used:.1f} MWh")
    print(f"Renewable Coverage:   {renewable_percentage:.1f}%")

    analytics_results.append(
        {
            "energy_required": total_energy,
            "solar_used": solar_used,
            "grid_used": grid_used
        }
    )

# Calculate energy use without SolarOjas
baseline = calculate_baseline_energy(
    solar_profile,
    ai_jobs
)

# Calculate energy use with SolarOjas
optimized = calculate_optimized_energy(
    analytics_results
)

# Display energy impact
display_energy_impact(
    baseline,
    optimized
)

# Calculate and display carbon impact
carbon_data = calculate_carbon_impact(
    baseline,
    optimized
)

display_carbon_impact(carbon_data)

# Calculate and display electricity cost impact
cost_data = calculate_cost_impact(
    baseline,
    optimized
)

display_cost_impact(cost_data)

print()
print("SolarOjas AI energy engine initialized successfully.")