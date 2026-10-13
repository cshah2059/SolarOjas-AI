class AIWorkload:
    def __init__(
        self,
        name,
        power_required,
        duration,
        earliest_start,
        deadline
    ):
        self.name = name
        self.power_required = power_required
        self.duration = duration
        self.earliest_start = earliest_start
        self.deadline = deadline

    def display(self):
        print("\nAI Workload")
        print("-" * 35)
        print(f"Job:              {self.name}")
        print(f"Power Required:   {self.power_required} MW")
        print(f"Duration:         {self.duration} hours")
        print(f"Earliest Start:   {self.earliest_start:02d}:00")
        print(f"Deadline:         {self.deadline:02d}:00")