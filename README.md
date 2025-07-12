# Pixiv Deleted Artwork Finder

Find the deleted(private) artworks on Pixiv.

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- requests library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/FatShion-FTD/Pixiv-Deleted-Retrieval
cd PixivRetraval
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Step-by-Step Guide

#### Step 0: Find the artwork ID by F12
- On your bookmark page, press **F12** to open the developer tools.
- Press **Ctrl+Shift+C** to select the element by cursor.
- Hover on the deleted artwork's **TITLE**, e.g. `-----`
- See the element:
```html
<div class="sc-57c4d86c-1 bkMzEN"><span to="/artworks/{PixivArtworkID}" class="sc-57c4d86c-6 fNOdSq">-----</span></div>
```
- **PixivArtworkID** is the artwork ID you need to find.


#### Step 1: Input Pixiv Artwork ID
- Enter the target Pixiv artwork ID (e.g., 123456789)
- Click "Find Adjacent Artworks" or press Enter
- The application will automatically find valid artwork IDs before and after your target to narrow down the time range.

#### Step 2: Manual Image URI Input
- Visit the adjacent artwork pages from Step 1 in your browser
- Right-click on the first image and select "Open in new tab"
- Copy the URL from the address bar, e.g. `https://i.pximg.net/img-original/img/2025/07/12/12/00/00/123456789_p0.jpg`
- Paste the adjacent artworks' URLs to the corresponding input fields.

#### Step 4: File Type Selection
- Select the file formats you want to search for:
  - JPG (recommended)
  - PNG (recommended)
  - GIF

#### Step 5: Start Search
- Click "Start Resource Search"
- The application will:
  - Extract time ranges from the provided URIs
  - Search for your target artwork within that time window
  - Download the first available format found

### Output

Downloaded files will be saved in the `download/` directory with the original filename format.

# Common Issues

1. **Time cost**
   - The time cost varies based on the adjacent artworks' time range. **1 check per second**.
   - Be patient, it may take a few minutes to find the deleted artwork.
2. **No result**
   - The principle of this repo is to find the artworks still on CDN. If the artwork is **REALLY deleted** by the author, this will not work. Thus, it can only find the artworks **acutally PRIVATE**.
   - If the artwork has been **UPDATED**, this will not work. Because the URI is changed. Thus, it can only find the initial uploaded artworks.

## Disclaimer

This tool is intended for personal use only. Users are responsible for complying with Pixiv's terms of service and applicable copyright laws. 

## License

This project is for educational purposes only. Please respect Pixiv's terms of service and the rights of artwork creators.
