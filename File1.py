import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk
import glob
import os
import re


class MapFlipper():

	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Map Viewer")
		self.root.geometry("1000x600")

		base_dir = os.path.dirname(__file__)
		images_dir = os.path.join(base_dir, "PALEOMAP PaleoAtlas Rasters v3")

		Map_Images = glob.glob(os.path.join(images_dir, "*.jpg"))
		
		def extract_suffix_number(path):
			name = os.path.basename(path)
			m = re.search(r'_(\d+)\.jpg$', name)
			return int(m.group(1)) if m else 10**9   # push malformed files to end
		
		Map_Images.sort(key=extract_suffix_number, reverse = True)

		def extract_time(path):
			name = os.path.basename(path)
			name = os.path.splitext(name)[0]
			name = re.sub(r'^Map\d+[a-zA-Z]*\s*', '', name)
			name = re.sub(r'_\d+$', '', name)
			return name.strip()

		self.index = 0

		
		self.times = [extract_time(f) for f in Map_Images]
		
		self.time_label = tk.Label(master = self.root, text = "")
		self.time_label.pack()

		self.original_maps = [Image.open(f) for f in Map_Images]
		#self.maps = [ImageTk.PhotoImage(Image.open(f)) for f in Map_Images]
        
		# Label to show image
		# self.label = tk.Label(self.root, image = self.maps[self.index])
		self.label = tk.Label(self.root, bg = "black")
		# self.label.pack()
		self.label.pack(fill="both", expand=True)
        
		# Button frame
		btn_frame = tk.Frame(self.root)
		# btn_frame.pack()
		btn_frame.pack(fill = "x", pady = 10, padx = 5)
        
		self.prev_btn = tk.Button(master = btn_frame, text = "Prev", command = self.prev_image)
		self.prev_btn.pack(side = "left", padx = 5)

		self.next_btn = tk.Button(master = btn_frame, text = "Next", command = self.next_image)
		self.next_btn.pack(side = "left")

		self.root.bind("<Configure>", self.on_resize)
		
		self.update_image()
		self.update_buttons()

	def resize_image(self, width, height):
		img = self.original_maps[self.index].copy()
		img.thumbnail((width, height), Image.Resampling.LANCZOS)
		return ImageTk.PhotoImage(img)

	def update_image(self):
		width = self.label.winfo_width()
		height = self.label.winfo_height()

		if width <= 1 or height <= 1:
			return
		
		photo = self.resize_image(width, height)
		self.label.configure(image = photo)
		self.label.image = photo
		self.time_label['text'] = self.times[self.index]
	
	def on_resize(self, event):
		if event.widget == self.root:
			self.update_image()

	def update_buttons(self):
		self.prev_btn.config(state="normal" if self.index > 0 else "disabled")
		self.next_btn.config(state="normal" if self.index < len(self.original_maps) - 1 else "disabled")


	def prev_image(self):
		if self.index > 0:
			self.index -= 1
			self.update_image()
			self.update_buttons()

	def next_image(self):
		if self.index < len(self.original_maps) - 1:
			self.index += 1
			self.update_image()
			self.update_buttons()


if __name__ == "__main__":
	app = MapFlipper()
	app.root.mainloop()