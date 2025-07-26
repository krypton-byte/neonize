from datetime import datetime
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
        self.username, self.repository = self.versioning.github_url.split(
            "/")[-2:]
        super().__init__(base_url=self.base_url)

    def get_last_version(self) -> str:
        """
        Retrieves the latest release version of the repository.

        Returns:
            str: The latest release tag name, or "0.0.0" if no releases are found.
        """
        resp = self.get(f"/repos/{self.username}/{self.repository}/releases")
        if resp.status_code == 404:
            return "0.0.0"
        resp.raise_for_status()

        releases = resp.json()
        if not isinstance(releases, list) or not releases:
            return "0.0.0"

        # Annotate each with a timestamp for easy comparison
        for rel in releases:
            rel["_created_ts"] = datetime.strptime(
                rel["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).timestamp()

        latest = max(releases, key=lambda r: r["_created_ts"])
        return latest["tag_name"]

    def download_neonize(self, version: str) -> bytes:
        """
        Downloads the source code for a specified release version as a ZIP archive.

        Args:
            version (str): The tag name of the release version to download.

        Returns:
            bytes: The content of the ZIP archive.
        """
        url = (
            f"https://codeload.github.com/{self.username}/{self.repository}/zip/refs/tags/{version}"
        )
        resp = self.get(url)
        resp.raise_for_status()
        return resp.content

    def get_last_neonize_release(self) -> bytes:
        """
        Retrieves the latest Neonize release as a ZIP archive.

        Returns:
            bytes: The content of the latest Neonize release ZIP archive.
        """
        latest_tag = self.get_last_version()
        return self.download_neonize(latest_tag)

    def get_last_goneonize_version(self) -> str:
        """
        Finds the latest Goneonize version by checking releases with available assets.

        Returns:
            str: The latest release tag name that contains more than 12 assets.

        Raises:
            TypeError: If no suitable release is found.
        """
        resp = self.get(f"/repos/{self.username}/{self.repository}/releases")
        if resp.status_code == 404:
            return "0.0.0"
        resp.raise_for_status()

        releases = resp.json()
        if not isinstance(releases, list) or not releases:
            raise TypeError("No releases available")

        # Add timestamps for sorting
        for rel in releases:
            rel["_created_ts"] = datetime.strptime(
                rel["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).timestamp()

        # Iterate newest→oldest
        for rel in sorted(
                releases, key=lambda r: r["_created_ts"], reverse=True):
            if len(rel.get("assets", [])) > 12:
                return rel["tag_name"]

        raise TypeError("Unavailable")
