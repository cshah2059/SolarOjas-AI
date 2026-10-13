def calculate_baseline_energy(solar_power, workloads):
    total_energy = 0

    # Track the solar energy remaining during each hour
    remaining_solar = solar_power.copy()

    solar_energy = 0

    # Baseline: run every workload as early as possible
    for job in workloads:
        start = job.earliest_start
        end = start + job.duration

        job_energy = job.power_required * job.duration
        total_energy += job_energy

        for hour in range(start, end):
            available_solar = remaining_solar[hour]

            solar_used = min(
                available_solar,
                job.power_required
            )

            solar_energy += solar_used

            # Remove solar already used by this workload
            remaining_solar[hour] -= solar_used

    grid_energy = total_energy - solar_energy

    if total_energy > 0:
        renewable_percentage = (
            solar_energy / total_energy
        ) * 100
    else:
        renewable_percentage = 0

    return {
        "total": total_energy,
        "solar": solar_energy,
        "grid": grid_energy,
        "renewable_percentage": renewable_percentage
    }


def calculate_optimized_energy(results):
    total_energy = 0
    solar_energy = 0
    grid_energy = 0

    for result in results:
        total_energy += result["energy_required"]
        solar_energy += result["solar_used"]
        grid_energy += result["grid_used"]

    if total_energy > 0:
        renewable_percentage = (
            solar_energy / total_energy
        ) * 100
    else:
        renewable_percentage = 0

    return {
        "total": total_energy,
        "solar": solar_energy,
        "grid": grid_energy,
        "renewable_percentage": renewable_percentage
    }


def display_energy_impact(baseline, optimized):
    grid_saved = baseline["grid"] - optimized["grid"]

    print("\n" + "=" * 50)
    print("             ENERGY IMPACT SUMMARY")
    print("=" * 50)

    print("\nWithout SolarOjas")
    print("-" * 35)
    print(f"Total AI Energy:       {baseline['total']:.1f} MWh")
    print(f"Solar Energy Used:     {baseline['solar']:.1f} MWh")
    print(f"Grid Energy Used:      {baseline['grid']:.1f} MWh")
    print(
        f"Renewable Coverage:    "
        f"{baseline['renewable_percentage']:.1f}%"
    )

    print("\nWith SolarOjas")
    print("-" * 35)
    print(f"Total AI Energy:       {optimized['total']:.1f} MWh")
    print(f"Solar Energy Used:     {optimized['solar']:.1f} MWh")
    print(f"Grid Energy Used:      {optimized['grid']:.1f} MWh")
    print(
        f"Renewable Coverage:    "
        f"{optimized['renewable_percentage']:.1f}%"
    )

    print("\nSolarOjas Impact")
    print("-" * 35)
    print(f"Grid Energy Saved:     {grid_saved:.1f} MWh")

    if baseline["grid"] > 0:
        reduction = (
            grid_saved / baseline["grid"]
        ) * 100

        print(
            f"Grid Energy Reduction: "
            f"{reduction:.1f}%"
        )