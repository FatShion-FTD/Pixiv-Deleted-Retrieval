import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import datetime
import time
import os
import re
from typing import Tuple, Optional
import threading

# Import functions from existing modules
from find_adj import find_adjacent_valid_artworks, build_pixiv_artwork_url
from find_resource import check_pixiv_image_existence
from resource_downloader import download_pixiv_gallery


class PixivResourceFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixiv Resource Finder")
        self.root.geometry("800x700")
        
        # Variables
        self.artwork_id = tk.StringVar()
        self.prev_artwork_url = tk.StringVar()
        self.next_artwork_url = tk.StringVar()
        self.prev_uri = tk.StringVar()
        self.next_uri = tk.StringVar()
        self.file_jpg = tk.BooleanVar(value=True)
        self.file_png = tk.BooleanVar(value=True)
        self.file_gif = tk.BooleanVar(value=False)
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Step 1: Input artwork ID
        ttk.Label(main_frame, text="Step 1: Input Pixiv Artwork ID", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(main_frame, text="Artwork ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.artwork_id_entry = ttk.Entry(main_frame, textvariable=self.artwork_id, width=20)
        self.artwork_id_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.artwork_id_entry.bind("<Return>", lambda e: self.find_adjacent_artworks())
        
        ttk.Button(main_frame, text="Find Adjacent Artworks", command=self.find_adjacent_artworks).grid(row=1, column=2, padx=(10, 0), pady=2)
        
        # Step 2: Show adjacent artworks
        ttk.Label(main_frame, text="Step 2: Adjacent Artworks", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        ttk.Label(main_frame, text="Previous Artwork URL:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.prev_url_entry = ttk.Entry(main_frame, textvariable=self.prev_artwork_url, width=60)
        self.prev_url_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Next Artwork URL:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.next_url_entry = ttk.Entry(main_frame, textvariable=self.next_artwork_url, width=60)
        self.next_url_entry.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Step 3: Manual URI input
        ttk.Label(main_frame, text="Step 3: Manual Image URI Input", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        instruction_text = """Please manually visit the artwork pages above and find the first image's img-original link:
1. Open the artwork page in your browser
2. Right-click on the first image and select "Inspect Element"
3. Find the href attribute containing img-original link
4. Copy the complete URI to the input fields below"""
        
        ttk.Label(main_frame, text=instruction_text, wraplength=700, justify=tk.LEFT).grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Previous Artwork URI:").grid(row=7, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.prev_uri, width=80).grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Next Artwork URI:").grid(row=8, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.next_uri, width=80).grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Step 4: File type selection
        ttk.Label(main_frame, text="Step 4: File Type Selection", font=("Arial", 12, "bold")).grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=10, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(file_frame, text="JPG", variable=self.file_jpg).grid(row=0, column=0, padx=(0, 10))
        ttk.Checkbutton(file_frame, text="PNG", variable=self.file_png).grid(row=0, column=1, padx=(0, 10))
        ttk.Checkbutton(file_frame, text="GIF", variable=self.file_gif).grid(row=0, column=2, padx=(0, 10))
        
        # Step 5: Search button
        ttk.Button(main_frame, text="Start Resource Search", command=self.start_search).grid(row=11, column=0, columnspan=3, pady=20)
        
        # Progress bar
        ttk.Label(main_frame, text="Search Progress:", font=("Arial", 10)).grid(row=12, column=0, sticky=tk.W, pady=(10, 5))
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=400)
        self.progress.grid(row=12, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Progress label
        self.progress_label = ttk.Label(main_frame, text="Ready", font=("Arial", 9))
        self.progress_label.grid(row=13, column=0, columnspan=3, sticky=tk.W, pady=0)
        
        # Status and log area
        ttk.Label(main_frame, text="Status and Log", font=("Arial", 12, "bold")).grid(row=14, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=90)
        self.log_text.grid(row=15, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(15, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def log(self, message: str):
        """Add message to log area"""
        self.log_text.insert(tk.END, f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, current: int, total: int, message: str = ""):
        """Update progress bar and label"""
        if total > 0:
            progress_value = (current / total) * 100
            self.progress['value'] = progress_value
            
            if message:
                self.progress_label.config(text=f"{message} ({current}/{total})")
            else:
                self.progress_label.config(text=f"Progress: {current}/{total} ({progress_value:.1f}%)")
        else:
            self.progress['value'] = 0
            self.progress_label.config(text=message if message else "Ready")
        
        self.root.update_idletasks()
    
    def reset_progress(self, message: str = "Ready"):
        """Reset progress bar"""
        self.progress['value'] = 0
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    

    

    
    def find_adjacent_artworks(self):
        """Find adjacent artwork IDs"""
        try:
            center_id = int(self.artwork_id.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid artwork ID")
            return
        
        self.log(f"Starting to find adjacent artworks for artwork {center_id}...")
        
        # Use existing function from find_adj.py
        prev_id, next_id = find_adjacent_valid_artworks(center_id)
        
        # Update GUI
        self.prev_artwork_url.set(build_pixiv_artwork_url(prev_id))
        self.next_artwork_url.set(build_pixiv_artwork_url(next_id))
        
        self.log(f"Previous artwork URL: {build_pixiv_artwork_url(prev_id)}")
        self.log(f"Next artwork URL: {build_pixiv_artwork_url(next_id)}")
        self.log("Please manually visit the URLs above to get the first image's img-original link")
    
    def extract_time_range(self, prev_uri: str, next_uri: str, target_id: int) -> Tuple[str, str, str]:
        """Extract time range from URIs"""
        # Extract time from URI pattern: img/2025/05/12/22/30/17/
        pattern = r'img/(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2})/(\d{2})/'
        
        prev_match = re.search(pattern, prev_uri)
        next_match = re.search(pattern, next_uri)
        
        if not prev_match or not next_match:
            raise ValueError("Unable to extract time information from URI")
        
        prev_time = f"{prev_match.group(4)}:{prev_match.group(5)}:{prev_match.group(6)}"
        next_time = f"{next_match.group(4)}:{next_match.group(5)}:{next_match.group(6)}"
        
        # Extract base URL template using the target artwork ID
        # Use the date structure from one of the URIs but with target artwork ID
        # Format: https://i.pximg.net/img-original/img/YYYY/MM/DD/{time}/ARTWORK_ID_p0
        base_url = f"https://i.pximg.net/img-original/img/{prev_match.group(1)}/{prev_match.group(2)}/{prev_match.group(3)}/{{time}}/{target_id}_p0"
        
        return prev_time, next_time, base_url
    

    
    def start_search(self):
        """Start searching for resources"""
        if not self.prev_uri.get() or not self.next_uri.get():
            messagebox.showerror("Error", "Please enter both previous and next artwork URIs")
            return
        
        if not any([self.file_jpg.get(), self.file_png.get(), self.file_gif.get()]):
            messagebox.showerror("Error", "Please select at least one file type")
            return
        
        # Extract target artwork ID
        try:
            target_id = int(self.artwork_id.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid artwork ID")
            return
        
        # Start search in background thread
        thread = threading.Thread(target=self.search_worker, args=(target_id,))
        thread.daemon = True
        thread.start()
    
    def search_worker(self, target_id: int):
        """Worker thread for searching resources"""
        try:
            # Reset progress bar
            self.reset_progress("Initializing search...")
            
            # Extract time range
            prev_uri = self.prev_uri.get()
            next_uri = self.next_uri.get()
            
            prev_time, next_time, base_url = self.extract_time_range(prev_uri, next_uri, target_id)
            
            self.log(f"Time range: {prev_time} to {next_time}")
            self.log(f"Base URL template: {base_url}")
            
            # Prepare extensions
            extensions = []
            if self.file_jpg.get():
                extensions.append('jpg')
            if self.file_png.get():
                extensions.append('png')
            if self.file_gif.get():
                extensions.append('gif')
            
            self.log(f"Searching file types: {', '.join(extensions)}")
            
            # Calculate total possible checks
            start_time = datetime.datetime.strptime(prev_time, '%H:%M:%S')
            end_time = datetime.datetime.strptime(next_time, '%H:%M:%S')
            time_range_seconds = int((end_time - start_time).total_seconds()) + 1
            total_checks = len(extensions) * time_range_seconds
            current_check = 0
            
            self.log(f"Total time range: {time_range_seconds} seconds")
            self.log(f"Maximum possible checks: {total_checks}")
            self.update_progress(0, total_checks, "Starting search...")
            
            # First, check which resource type exists
            found_extension = None
            found_resource_url = None
            
            for ext_index, ext in enumerate(extensions):
                image_id = f"{target_id}_p0.{ext}"
                self.log(f"Checking {ext.upper()} format resource existence...")
                
                # Use find_resource.py function to check existence
                # We need to manually check for existence first
                headers = {
                    'Referer': 'https://www.pixiv.net/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                # Try a few time points to find the resource
                current_time = datetime.datetime.strptime(prev_time, '%H:%M:%S')
                end_time = datetime.datetime.strptime(next_time, '%H:%M:%S')
                
                while current_time <= end_time:
                    current_check += 1
                    time_for_url = current_time.strftime('%H/%M/%S')
                    test_url = f"{base_url.replace('{time}', time_for_url)}.{ext}"
                    
                    # Update progress
                    self.update_progress(current_check, total_checks, f"Checking {ext.upper()} at {time_for_url}")
                    
                    try:
                        response = requests.get(test_url, headers=headers, timeout=10)
                        if response.status_code == 200:
                            found_extension = ext
                            found_resource_url = test_url
                            self.log(f"✅ Found {ext.upper()} format resource: {test_url}")
                            self.update_progress(current_check, total_checks, f"Found {ext.upper()} resource!")
                            break
                    except Exception:
                        pass
                    
                    current_time += datetime.timedelta(seconds=1)
                
                if found_extension:
                    break
                else:
                    self.log(f"❌ {ext.upper()} format resource not found")
            
            # If we found a resource, download it using resource_downloader
            if found_extension and found_resource_url:
                self.update_progress(total_checks, total_checks, "Downloading resource...")
                self.log(f"Starting to download found {found_extension.upper()} format resource...")
                
                download_dir = "download"
                os.makedirs(download_dir, exist_ok=True)
                
                # Use resource_downloader function to download the gallery
                download_pixiv_gallery(found_resource_url, download_dir)
                
                self.log(f"✅ Successfully downloaded {found_extension.upper()} format resource")
                self.reset_progress("Download completed successfully!")
                messagebox.showinfo("Success", f"Found and successfully downloaded {found_extension.upper()} format resource to download/ directory")
            else:
                self.log("❌ No resources found in the specified time range with selected formats")
                self.reset_progress("Search completed - No resources found")
                messagebox.showwarning("Not Found", "No resources found in the specified time range with selected formats")
                
        except Exception as e:
            self.log(f"❌ Error occurred during search: {e}")
            self.reset_progress("Search failed due to error")
            messagebox.showerror("Error", f"Error occurred during search: {e}")
    



def main():
    root = tk.Tk()
    app = PixivResourceFinder(root)
    root.mainloop()


if __name__ == "__main__":
    main() 