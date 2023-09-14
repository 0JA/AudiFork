# Profile Management
class ProfileManager:
    def __str__(self) -> str:
        return f"ProfileManager({self.profiles})"

    def __init__(self):
        self.profiles = {}
        self.__initialize_default()

    def __initialize_default(self) -> bool:
        self.__create("Default", {}, 0)
        return True

    def __create(self, name: str, settings: dict, id: int = None) -> bool:
        if id is not None:
            next_id = id
        else:
            next_id = self.__generate_id()
        self.profiles[next_id] = {"name": name, **settings}
        return True

    def __generate_id(self) -> int:
        if not self.profiles or len(self.profiles) == 1 and 0 in self.profiles:
            return 1
        return max(self.profiles.keys()) + 1

    def __delete_all(self) -> bool:
        self.profiles.clear()
        self.__initialize_default()
        return True

    def __delete(self, profile_id: int) -> bool:
        try:
            if self.exists(profile_id):
                del self.profiles[profile_id]
                return True
        except Exception as e:
            print(f"An error occurred while deleting profile: {e}")
            return False

    def delete(self, profile_id: int) -> bool:
        """Deletes a profile by id.

        Args:
            profile_id (int): The id of the profile to delete.

        Returns:
            bool: True if the profile was deleted, False otherwise.
        """
        self.__delete(profile_id)
        return True

    def delete_all(self) -> bool:
        """Deletes all profiles and re-initializes the default profile.

        Returns:
            bool: True if all profiles were deleted and the default profile was re-initialized, False otherwise.
        """
        try:
            self.__delete_all()
            return True
        except Exception as e:
            print(f"An error occurred while deleting all profiles: {e}")
            return False

    def update(self, profile_id: int, new_settings: dict) -> bool:
        """Updates a profile with new settings.

        Args:
            profile_id (int): The id of the profile to update.
            new_settings (dict): The new settings to apply to the profile.

        Returns:
            bool: True if the profile was updated, False otherwise.
        """
        if profile_id in self.profiles:
            self.profiles[profile_id].update(new_settings)
            return True
        return False

    def get_profiles(self) -> dict:
        """Returns all profiles.

        Returns:
            dict: A dictionary of all profiles.
        """
        return self.profiles

    def get_total(self) -> int:
        """Returns the total number of profiles.

        Returns:
            int: The total number of profiles.
        """
        return len(self.profiles)

    def create_profile(self, name: str, settings: dict) -> bool:
        """Creates a new profile.

        Args:
            name (str): The name of the profile.
            settings (dict): The settings to apply to the profile.

        Returns:
            bool: True if the profile was created, False otherwise.
        """
        if not self.exists(self.get_id(name)):
            id = self.__generate_id()
            self.__create(name, settings, id)
            return True

    def exists(self, profile_id: int) -> bool:
        """Checks if a profile exists by id.

        Args:
            profile_id (int): The id of the profile to check.

        Returns:
            bool: True if the profile exists, False otherwise.
        """
        return profile_id in self.profiles

    def get_id(self, name: str) -> int:
        """Returns the id of a profile by name.

        Args:
            name (str): The name of the profile.

        Returns:
            int: The id of the profile, or False if the profile doesn't exist.

        """
        for profile_id, profile in self.profiles.items():
            if profile["name"] == name:
                return profile_id
        return None  # Changed from False to None <<< Why??
