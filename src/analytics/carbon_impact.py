def calculate_carbon_impact(
    baseline,
    optimized,
    grid_emission_factor=0.4
):
    # grid_emission_factor is metric tons of CO2 per MWh

    baseline_emissions = (
        baseline["grid"] * grid_emission_factor
    )

    optimized_emissions = (
        optimized["grid"] * grid_emission_factor
    )

    emissions_avoided = (
        baseline_emissions - optimized_emissions
    )

    if baseline_emissions > 0:
        carbon_reduction = (
            emissions_avoided / baseline_emissions
        ) * 100
    else:
        carbon_reduction = 0

    return {
        "baseline_emissions": baseline_emissions,
        "optimized_emissions": optimized_emissions,
        "emissions_avoided": emissions_avoided,
        "carbon_reduction": carbon_reduction
    }


def display_carbon_impact(carbon_results):
    print("\n" + "=" * 50)
    print("               CARBON IMPACT")
    print("=" * 50)

    print(
        f"Baseline CO2 Emissions: "
        f"{carbon_results['baseline_emissions']:.2f} metric tons"
    )

    print(
        f"SolarOjas CO2 Emissions: "
        f"{carbon_results['optimized_emissions']:.2f} metric tons"
    )

    print(
        f"CO2 Emissions Avoided: "
        f"{carbon_results['emissions_avoided']:.2f} metric tons"
    )

    print(
        f"Carbon Reduction: "
        f"{carbon_results['carbon_reduction']:.1f}%"
    )