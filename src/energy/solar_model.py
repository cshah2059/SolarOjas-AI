def generate_solar_profile():
    """
    Returns simulated solar power available during each hour of a day.
    Power values are in megawatts (MW).
    """

    solar_power = [
        0, 0, 0, 0, 0, 0,       # 12 AM - 5 AM
        0.5, 2, 5, 10, 16, 22,  # 6 AM - 11 AM
        26, 28, 27, 23, 17, 10, # 12 PM - 5 PM
        4, 1, 0, 0, 0, 0        # 6 PM - 11 PM
    ]

    return solar_power


def display_solar_profile(solar_power):
    print("\n24-Hour Solar Energy Profile")
    print("-" * 35)

    for hour, power in enumerate(solar_power):
        print(f"{hour:02d}:00  |  {power:5.1f} MW")