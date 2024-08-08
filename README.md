# Jellyfin Discord RPC Integration
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

## Overview

This project integrates Jellyfin with Discord Rich Presence, allowing you to display your currently playing media on Jellyfin as your Discord status. The script fetches the currently playing media from Jellyfin, retrieves the album cover or default image, and updates your Discord status with details about the media, including the track name, artists, album, and progress.

## Features

- Displays the currently playing media from Jellyfin on Discord.
- Shows track name, artists, album, and progress.
- Fetches album covers or uses a default image if none is found.
- Automatically reconnects to Discord RPC if the connection is lost.
- Logging for debugging and monitoring the script's activities.

## Prerequisites

- A running instance of Jellyfin with a valid API key.
- A Discord application with the Client ID to connect to Discord RPC.
- Python 3.x installed.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Ray-kong/jellyfin-discord-rich-presence.git
    cd jellyfin-discord-rich-presence
    ```

2. **Install the Required Python Packages:**

    Use the `requirements.txt` file to install all the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` File:**

    Create a `.env` file in the project root directory with the following environment variables:

    ```bash
    JELLYFIN_URL=<Your Jellyfin server URL>
    JELLYFIN_API_KEY=<Your Jellyfin API key>
    JELLYFIN_USER_ID=<Your Jellyfin user ID>
    DISCORD_CLIENT_ID=<Your Discord application client ID>
    ```

    ### How to Obtain Required Values:

    - **Jellyfin API Key:**
        1. Log in to your Jellyfin server.
        2. Go to `Dashboard` -> `API Keys`.
        3. Click `Create API Key`.
        4. Copy the generated API key and use it in the `.env` file.

    - **Jellyfin User ID:**
        1. Go to `Dashboard` -> `Users`.
        2. Click on the user you want to use.
        3. The user ID is in the URL after `/users/`.

    - **Discord Client ID:**
        1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
        2. Create a new application.
        3. Copy the Client ID from the application's General Information page.

4. **Set Up Your Discord Application:**

    - Ensure your Discord application has the necessary permissions to use Rich Presence.

## Usage

1. **Run the Script:**

    ```bash
    python jellyfin_rpc.py
    ```

2. **Ensure Continuous Operation:**

    - The script needs to run 24/7 to continuously update your Discord status with your Jellyfin activity. It can be run on any machine where Python is installed, but you might want to use a server or a device that's always on.

3. The status is updated every 5 seconds. If no media is playing, the Discord status will be cleared.

## Logging

- Logs are stored in the `jellyfin_rpc.log` file in the project root directory.
- Logs include connection status, current playing media, and any errors encountered.




## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes. Make sure to update the documentation if you add any new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.