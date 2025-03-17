import httpx
from .version import Version


class Github(httpx.Client):
    """
    A client for interacting with the GitHub API, specifically for retrieving release
    information and downloading repository assets.

    This class extends `httpx.Client` and provides methods to:
    - Fetch the latest release version of a repository.
    - Download the source code of a specific release.
    - Retrieve the latest Neonize release.
    - Determine the last Goneonize version based on available assets.
    """

    def __init__(self):
        """
        Initializes the GitHub client with the repository information and base API URL.
        """
        self.base_url = "https://api.github.com"
        self.versioning = Version()
        self.username, self.repository = self.versioning.github_url.split("/")[-2:]
        super().__init__(base_url=self.base_url)

    def get_last_version(self) -> str:
        """
        Retrieves the latest release version of the repository.

        Returns:
            str: The latest release tag name.
        """
        r = self.get(f"/repos/{self.username}/{self.repository}/releases").json()
        if isinstance(r, dict) and r.get("status") == '404':
            return "0.0.0"
        return r[0]["tag_name"]

    def download_neonize(self, version: str) -> bytes:
        """
        Downloads the source code for a specified release version as a ZIP archive.

        Args:
            version (str): The tag name of the release version to download.

        Returns:
            bytes: The content of the ZIP archive.
        """
        r = self.get(
            f"https://codeload.github.com/{self.username}/{self.repository}/zip/refs/tags/{version}"
        )
        return r.content

    def get_last_neonize_release(self) -> bytes:
        """
        Retrieves the latest Neonize release as a ZIP archive.

        Returns:
            bytes: The content of the latest Neonize release ZIP archive.
        """
        return self.download_neonize(self.get_last_version())

    def get_last_goneonize_version(self) -> str:
        """
        Finds the latest Goneonize version by checking releases with available assets.

        Returns:
            str: The latest release tag name that contains assets.

        Raises:
            TypeError: If no release with assets is found.
        """
        r = self.get(f"/repos/{self.username}/{self.repository}/releases").json()
        if isinstance(r, dict) and r.get("status") == '404':
            return "0.0.0"
        for release in r:
            if len(release["assets"]):
                return release["tag_name"]
        raise TypeError("Unavailable")
