
# PyNowify

A simple app to display your currently playing Spotify track on a Raspberry Pi, made with python-tk.

This repo is a re-implementation of [Nowify](https://github.com/jonashcroft/Nowify) in python

PyNowify will:

* ✅ - Use Spotify Web API to get your current track
* ✅ - Only access that and no other data
* ✅ - Use Access and Refresh Tokens to ensure that you're kept logged in between sessions
* ✅ - Display the current track artist, cover, and a matching vibrant background colour

Preview:
![Nowify Preview Image 1](assets/preview-1.png?raw=true "Nowify preview image, cover art for the song 'Child' by Shir Frum")
![Nowify Preview Image 2](assets/preview-2.png?raw=true "Nowify preview image, cover art for the song 'Evangeline' by Whitney & Madison Cunningham")

---
## How to use

### Prerequisites

You will need:
* Python >= 3.10 (with Tk)
* Spotify Client Keys
* A device to display Nowify

### Installation
1. Clone this repository or install from [Pypi](https://pypi.org/project/PyNowify/)
2. Create [Spotify client keys](#create-spotify-client-keys-spotify-keys)
3. Create the `.env` file with the keys and you configuration

### Usgae
Launch `py-nowify` from the directory your `.env` resides

Alternatively you can create a launcher to run it on stratup

## Create Spotify Client keys
* Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
* Log in and click **Create an App**.
* Copy the **Client ID** and **Client Secret**.
* In your app settings on the dashboard, add `http://127.0.0.1:3000` (or your custom URI) under **Redirect URIs**.
* Copy down the Client Secret and Client ID and save your app in the Spotify Dashboard.
* Copy your parameters into a file named `.env` in the root of your project directory.
   * Replace `<SPOTIFY_CLIENT_ID>` and `<SPOTIFY_SECRET>` with your actual credentials.

## Configuration

This document provides details for configuring the environment variables required by the application. Create a `.env` file in the directory from which you will run the app.

### Variable Reference

#### 🎵 Spotify API Credentials

| Variable | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `SPOTIPY_CLIENT_ID` | `String` | *Required* | Your Spotify Developer Application Client ID. Obtained from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). |
| `SPOTIPY_CLIENT_SECRET` | `String` | *Required* | Your Spotify Developer Application Client Secret. Keep this secure and never commit it to public repositories. |
| `SPOTIPY_REDIRECT_URI` | `String` | `http://127.0.0.1:3000` | The URI to redirect to after user authentication. Must match one of the Redirect URIs specified in your Spotify App settings. |


#### 🖥️ Display & Window Settings

| Variable | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `FULLSCREEN` | `Boolean` | `false` | Controls whether the application launches in fullscreen mode (`true` or `false`). |
| `WINDOW_HEIGHT` | `Integer` | `480` | Sets the initial vertical height of the application window in pixels. |
| `WINDOW_WIDTH` | `Integer` | `800` | Sets the initial horizontal width of the application window in pixels. |
| `LOCK_ASPECT_RATIO` | `Boolean` | `false` | Determines whether to enforce a fixed aspect ratio when the window is resized (`true` or `false`). |
| `RESIZEABLE` | `Boolean` | `true` | Allows users to manually resize the application window (`true` or `false`). |

### Example `.env` File

```env
SPOTIPY_CLIENT_ID="<SPOTIFY_CLIENT_ID>"
SPOTIPY_CLIENT_SECRET="<SPOTIFY_SECRET>"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:3000"
FULLSCREEN=false
WINDOW_HEIGHT=480
WINDOW_WIDTH=800
LOCK_ASPECT_RATIO=false
RESIZEABLE=true
```
