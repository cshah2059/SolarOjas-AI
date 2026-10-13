def find_best_solar_window(solar_power, workload):
    best_start = None
    best_solar_used = -1
    best_grid_used = 0

    total_energy_required = (
        workload.power_required * workload.duration
    )

    for start_hour in range(
        workload.earliest_start,
        workload.deadline - workload.duration + 1
    ):
        solar_used = 0

        for hour in range(
            start_hour,
            start_hour + workload.duration
        ):
            available_solar = solar_power[hour]

            solar_used += min(
                available_solar,
                workload.power_required
            )

        grid_used = total_energy_required - solar_used

        if solar_used > best_solar_used:
            best_solar_used = solar_used
            best_grid_used = grid_used
            best_start = start_hour

    renewable_percentage = (
        best_solar_used / total_energy_required
    ) * 100

    return (
        best_start,
        best_solar_used,
        best_grid_used,
        renewable_percentage
    )


def schedule_multiple_workloads(solar_power, workloads):
    remaining_solar = solar_power.copy()
    results = []

    for workload in workloads:
        best_start = None
        best_solar_used = -1

        total_energy_required = (
            workload.power_required * workload.duration
        )

        for start_hour in range(
            workload.earliest_start,
            workload.deadline - workload.duration + 1
        ):
            solar_used = 0

            for hour in range(
                start_hour,
                start_hour + workload.duration
            ):
                available_solar = remaining_solar[hour]

                solar_used += min(
                    available_solar,
                    workload.power_required
                )

            if solar_used > best_solar_used:
                best_solar_used = solar_used
                best_start = start_hour

        if best_start is not None:
            for hour in range(
                best_start,
                best_start + workload.duration
            ):
                solar_taken = min(
                    remaining_solar[hour],
                    workload.power_required
                )

                remaining_solar[hour] -= solar_taken

            grid_used = (
                total_energy_required - best_solar_used
            )

            renewable_percentage = (
                best_solar_used / total_energy_required
            ) * 100

            results.append(
                (
                    workload,
                    best_start,
                    best_solar_used,
                    grid_used,
                    renewable_percentage
                )
            )

    return results