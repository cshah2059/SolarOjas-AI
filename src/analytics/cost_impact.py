def calculate_cost_impact(baseline, optimized, electricity_rate=0.12):
    # Convert MWh to kWh before calculating electricity cost
    baseline_grid_kwh = baseline["grid"] * 1000
    optimized_grid_kwh = optimized["grid"] * 1000

    baseline_cost = baseline_grid_kwh * electricity_rate
    optimized_cost = optimized_grid_kwh * electricity_rate

    cost_saved = baseline_cost - optimized_cost

    if baseline_cost > 0:
        cost_reduction = (cost_saved / baseline_cost) * 100
    else:
        cost_reduction = 0

    return {
        "baseline_cost": baseline_cost,
        "optimized_cost": optimized_cost,
        "cost_saved": cost_saved,
        "cost_reduction": cost_reduction
    }


def display_cost_impact(cost_data):
    print("\n" + "=" * 50)
    print("                 COST IMPACT")
    print("=" * 50)

    print(f"Without SolarOjas Cost: ${cost_data['baseline_cost']:,.2f}")
    print(f"With SolarOjas Cost:    ${cost_data['optimized_cost']:,.2f}")
    print(f"Estimated Cost Saved:   ${cost_data['cost_saved']:,.2f}")
    print(f"Cost Reduction:         {cost_data['cost_reduction']:.1f}%")