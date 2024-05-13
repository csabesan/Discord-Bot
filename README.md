# Discord Bot

This Discord bot project is a multifunctional bot developed using Python and the discord.py library. The bot includes features such as music playback, an economy system, interactive minigames, and utility commands like weather lookup.

## Features

- **Music Playback**: Play, pause, skip, and queue music from YouTube. Accessible via "!" commands.
- **Economy System**: Users can work, play blackjack, baccarat, check balances, deposit and withdraw virtual currency. Accessible via slash commands.
- **Minigames**: Includes interactive games such as 8ball, coinflip, and dice rolling. Accessible via slash commands.
- **Utility Commands**: Check the weather in any city, ping the bot, and more. Accessible via slash commands.

![Demo](https://s12.gifyu.com/images/Sayxn.gif)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Tristanv0/Discord-Bot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure bot token and WeatherAPI key in `config.py`. Example `config.py`:

    ```python
    # Discord Bot Token
    TOKEN = 'your_discord_token_here'

    # WeatherAPI Key
    API_KEY = 'your_weather_api_key_here'
    ```

### Setting up FFmpeg

FFmpeg is required for music playback functionality. Follow these steps to set it up:

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org).
2. Extract the downloaded FFmpeg folder and rename the bin folder to `ffmpeg`.
3. **Windows**:
    - Move the `ffmpeg` folder to the `C:\` drive.
    - Add the `C:\ffmpeg` directory to the system PATH variable.
4. **macOS / Linux**: Install FFmpeg via package manager (`brew install ffmpeg` for macOS, `sudo apt-get install ffmpeg` for Debian-based Linux).

## Usage

### Music Playback

- `!play <YouTube URL>`: Play a song from YouTube.
- `!pause`: Pause the currently playing song.
- `!skip`: Skip the current song.
- `!queue`: Add a song to the music queue.

### Economy System

- `/work`: Work to earn virtual currency.
- `/baccarat <player|banker|tie> <bet>`: Play baccarat and bet on player, banker, or tie.
- `/blackjack <bet>`: Play blackjack.
- `/balance [user]`: Check your account balance or the balance of a specified user.
- `/deposit <amount>`: Deposit virtual currency into your account.
- `/withdraw <amount>`: Withdraw virtual currency from your account.

### Minigames

- `/8ball <question>`: Ask the magic 8-ball a question.
- `/coinflip`: Flip a coin.
- `/roll`: Roll a dice.

### Utility Commands

- `/weather <city>`: Check the weather in a specific city.
- `/ping`: Ping the bot to check its responsiveness.
- `/help`: Display a list of available commands.

## Troubleshooting

If you encounter any issues during installation or usage, please check the following:

- Ensure all dependencies are installed correctly.
- Double-check the bot token and WeatherAPI key in `config.py`.
- Verify FFmpeg is properly set up according to the instructions.


