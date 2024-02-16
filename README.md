# SpAnalyzer

## Project Information
SpAnalyzer is a simple package which is useful for returning information about Spotify playlists.

## Installing and Building the Package
Before running the SpAnalyzer, you need to set up the project and install the necessary dependencies. Follow the steps below to build the package, and install it to your system.

### System Dependencies
This project requires:
```bash
git
python3
tk
```

### Building and Installing the package
1. Make sure tk is installed. On Windows and MacOS, this should be done automatically when you install Python, however this isn't the case on Linux. Based on your distribution, you may have to install tkinter manually. Doing this, however, is very easy.

* On Debian and Ubuntu based systems, run the following command as `root`:
```bash
sudo apt install python3-tk
```
* On Red Hat and Fedora based systems, run the following command as `root`:
```bash
sudo dnf install python3-tk
```
* On SUSE Linux based distributions, run the following command as `root`:
```bash
sudo zypper in python-tk
```
* On Arch Linux based systems, run the following command as `root`:
```bash
sudo pacman -S tk
```
2. Clone the repository:
```bash
$ git clone https://gitlab.com/the-cat-collective/tcc-code/spotify-analyzer.git
```
3. Navigate to the Project Directory
```bash
$ cd spanalyzer
```
4. Create a virtual environment
```bash
$ python3 -m venv env
$ source ./env/bin/activate
```
5. Build and Install the Package (without docs)
```bash
$ pip install .
```
This command will also install the build dependencies for the project, so you don't need to go hunting for them seperately.

### Accessing docs online
Go to [Docs](https://the-cat-collective.gitlab.io/tcc-code/spanalyzer/).

### Manually building the docs
0. Make sure you're in a virtual environment
1. Install `sphinx` and required modules
```bash
$ pip install .[docs]
```
2. `cd` into the docs folder after following the steps above
```bash
$ cd src/spanalyzer/docs
```
3. Run the build command
```bash
$ make html
```
3. Open the HTML
```bash
$ firefox ./build/html/index.html
```

### Developing SpAnalyzer
1. Clone the repository:
```bash
$ git clone https://gitlab.com/the-cat-collective/tcc-code/spotify-analyzer.git
```
2. Navigate to the Project Directory
```bash
$ cd spanalyzer
```
3. Create a virtual environment
```bash
$ python3 -m venv env
$ source ./env/bin/activate
```
4. Build and Install the Package (with docs and extra modules for type safety)
```bash
$ pip install .[docs,dev]
$ pre-commit install
```
5. Occasionally check the validity of your code by running `pre-commit`
```bash
$ pre-commit run --all-files
```
This command will also install the build dependencies for the project, so you don't need to go hunting for them seperately.

## Project Structure
The root of the project contains the `src` directory which contains the`spanalyzer` directory, which contains `__main.py`, `__init__.py`, and `application/`. `application/` contains `core/`, `gui/`, `main/`, `parsers/`, and `utilities/`. Each of these directories contains some of the scripts originally within this directory, which have now been split up based on function. The root of the project contains the `README` and `LICENSE`, and the `scripts/` directory, which contains the `typecheck_repo.py` script.

## Acquiring API Keys
The script requires you to provide your Spotify Client ID and Spotify Client Secret along with a playlist URL.
You can acquire a Spotify Client ID and Client Secret by making an account at [The Spotify Developer Portal](https://developer.spotify.com) and then creating a blank app. This will expose the keys that you need to run the script.

## Example usage
Analyze a Spotify playlist and display the results on the screen:
```bash
$ python spotify-analyzer.py --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --playlist_url PLAYLIST_URL --output screen
```
Analyze a Spotify playlist, save the results to a file, and sort them:
```bash
$ python spotify-analyzer.py --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET --playlist_url PLAYLIST_URL --output file --sort
```
Show the script's help menu
```bash
$ spanalyzer -h
```
Use `-Y` to add a YAML config and use that for config options:
* First write a YAML file like the one below to `config.yaml`:
```yaml
Spotify:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  playlist_url: PLAYLIST_URL
  type: song
  output: screen
  sort: false
```
Then you can run SpAnalyzer much easier with:
```bash
$ spanalyzer -Y
```

## Licensing
* This project is licensed under the BSD 3-Clause License. Please refer to the [LICENSE](LICENSE) file for the full text of the project's license.

* For licensing information related to first and third-party components used in this project, please refer to the [LICENSING](LICENSING.md) file.

## Disclaimer
The code within this repository is provided "as-is", and no former, current, or future owners of this project and/or repository are liable for any modifications or changes undertaken to the script that violate Spotify's terms of use.
