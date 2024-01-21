import os
from PIL import Image, ImageFilter

# TODO: run this file when Option is selected
# TODO: add Option in GUI for this
# at the moment, the Pictures are edited (darker, blur)


def pics_darker(folder):
    # Path to the folder with images
    # folder_path = './' # Root folder of script
    folder_path = folder


    # Create a subfolder for the modified images
    if not os.path.exists(f'{folder_path}/darker_pictures'):
        os.mkdir(f'{folder_path}/darker_pictures')

    # Loop through all images in the folder
    for filename in os.listdir(folder_path):


        # Check if the file is an image
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):

            # Open image
            image = Image.open(os.path.join(folder_path, filename))

            # Reduce brightness auf 60%
            image = image.point(lambda p: p * 0.75)

            # Add a Gaussian blur filter with moderate strength (radius=2)
            # Der radius-Parameter gibt den Radius des Filterkernels in Pixeln an,
            # der zur Berechnung der Gauss'schen Glättung verwendet wird.
            # Je höher der Radius, desto stärker ist die Unschärfe.
            image = image.filter(ImageFilter.GaussianBlur(radius=6))

            # Save the modified image in the subfolder
            image.convert('RGB').save(os.path.join(folder_path, f'{folder_path}/darker_pictures', filename))

    print("Bilder wurden erfolgreich bearbeitet")
