import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans


class Thisissodumb:
    def __init__(self, root):
        self.root = root
        self.root.title("What colors are the popular ones??")
        self.root.geometry("500x500")
        self.select_button = tk.Button(self.root, text="Choose picture you want", command=self.select_image)
        self.select_button.pack(padx=20, pady=10)
        self.canvas = None
        self.color_rects = None
        # hontestly i dont know what half of these do, I know it sets up the tkinter window with the window and the button
        # but i had to look up the class thing (self.) and how it works because if I tried to make this like a normal
        # python file with no classes, it wont work, so it needs to be class???

        #also its stupid because normally if you do root. it will show all the options but if you do it in classes
        #you need to know what you're referencing or else it won't show up and the IDE will think you belong in an
        # insane asylum

    def get_dominant_colors(self, image_path):
        # computers are stupid and need to convert the pictures to see it their own way, added X and Y for debugging
        thumbnailX = 300
        thumbnailY = 300
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.thumbnail((thumbnailX, thumbnailY))

        ########################################################
        img_array = np.array(img)
        reshaped_img_array = img_array.reshape((-1, 3))
        kmeans = KMeans(n_clusters=4)    # change clusters for how many colors you want shown
        kmeans.fit(reshaped_img_array)
        dominant_colors = kmeans.cluster_centers_.astype(int)
        ###### so basically

        return dominant_colors

    def display_colors(self, image_path):
        if self.canvas:
            self.canvas.destroy()
        if self.color_rects:
            self.color_rects.destroy()

        # check if we have an active canvas so we can choose another image



        dominant_colors = self.get_dominant_colors(image_path)

        # need to loan the images for some reason even though its already there
        thumbnailX = 300
        thumbnailY = 300
        img = Image.open(image_path)
        img.thumbnail((thumbnailX, thumbnailY))
        self.photo_image = ImageTk.PhotoImage(img)

        # Create canvas for image display
        self.canvas = tk.Canvas(self.root, width=self.photo_image.width(), height=self.photo_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.color_rects = tk.Frame(self.root)
        self.color_rects.pack(side=tk.LEFT, padx=10, pady=10)

        for color in dominant_colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            # Display color as a rectangle
            color_label = tk.Label(self.color_rects, bg=hex_color, width=5, padx=5)
            color_label.pack(anchor='w', padx=5, pady=2)

            # shows your the information about the color but it looks stupid and I cant figure out to make it pretty
            # color_text = f"RGB: {color},"
            # color_info_label = tk.Label(self.color_rects, width=10, anchor='w')
            # color_info_label.pack(anchor='w', padx=5, pady=2)


        # Im so proud of this
        self.select_button.config(text="Select Another Image")

    def select_image(self):
        # I wanted to make it so the else would give an error message saying you need the right format but filetype does it
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.display_colors(file_path)


if __name__ == "__main__":
    # I both love and hate how python supports classes because i dont understand it at all but it works???
    root = tk.Tk()
    app = Thisissodumb(root)
    root.mainloop()
