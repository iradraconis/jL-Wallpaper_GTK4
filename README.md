# jLWallpaper

jLWallpaper is an application for personalizing the wallpaper images in the j-lawyer-client application. It is built using Gnome Builder and GTK4. The software allows you to choose a directory of images, reduce the brightness and sharpness of these images, and then integrate them as wallpapers into the j-lawyer-client application. The original images remain unchanged.

## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Installation](#Installation)
3. [Usage](#Usage)
4. [License](#License)

## Prerequisites

To use jLWallpaper, you need:
- Python 3.7 or higher
- GTK 4.0 or higher
- Gnome Builder

These can be installed with the package manager of your choice. 

## Installation

1. Download the repository:

```bash
git clone https://github.com/MaxSteinert/jLWallpaper.git
```

2. Navigate to the downloaded directory:

```bash
cd jLWallpaper
```

3. Open the project in Gnome Builder and build it:

```bash
gnome-builder .
```

Alternatively, you can use the command line to build and run the application:

```bash
meson _build
ninja -C _build
./_build/src/window.py
```

## Usage

1. Start the application.
2. Click the "Open Pictures Folder" button and select the folder containing the images you want to use as wallpapers.
3. Click the "Open jL Folder" button and select the directory where your j-lawyer-client application is located.
4. Click "Run" to start the process. The application reduces the brightness and sharpness of the images, packs them into the j-lawyer-client application, and replaces the original wallpapers.

## License

jLWallpaper is a free software project that has been released under the GNU General Public License (GPLv3). For further details, please see the [LICENSE](LICENSE) file.
