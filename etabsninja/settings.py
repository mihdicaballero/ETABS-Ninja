class Settings:
    """A class to store all settings for the project."""

    def __init__(self):
        """Initialize the default settings."""

        # Drifts check for wind
        self.LoadCaseList = ["W Service"] # Load case with wind Load Sets
        self.max_InterstoryDrift = 1/400
        self.JointsGroupName = "Nodos" # Group with column joints to check interstory drift.
        self.max_BuildingDrift = 1/400