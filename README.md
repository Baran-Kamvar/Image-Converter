# 🖼️ Image-Converter
<div align="left">
<img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
<img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Version">
<img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python">
<img src="https://img.shields.io/github/issues/Baran-Kamvar/Image-Converter" alt="issues">
</div>

📸 Overview
Image Converter is a modern desktop application with a graphical interface designed for quick and easy conversion of hundreds of images to various formats. With a beautiful dark UI, WebP support, and intelligent handling of oversized images, this tool is the perfect choice for web image optimization, archiving, or format standardization.

---------

 ✨ Why Image Converter?
- 🚀 High Speed: Batch convert hundreds of files in seconds
- 🎯 Easy to Use: Simple GUI with no technical knowledge required
- 🔧 Highly Configurable: Complete control over quality, format, and advanced options
- 💎 Smart Management: Automatic handling of common issues like WebP size limitations
- 📊 Detailed Reporting: Complete log of all operations with copy capability

------------

🎯 Features

⚡ Core Capabilities
- ✅ Batch conversion of multiple images simultaneously
- 📁 Recursive processing of subfolders
- 🎨 Input formats: JPG, JPEG, PNG, BMP, TIFF, GIF, WEBP
- 💾 Output formats: JPG, PNG, WEBP
- 🎚️ Quality control: From 60% to 100%
- 🔄 Lossless mode for WebP

🛠️ Advanced Features
Smart WebP Handling
Images larger than 16383 pixels (WebP limitation) are automatically managed:

- 📏 Resize: Proportional downsizing
- ⏭️ Skip: Skip the file
- 🔄 Convert to JPG: Convert to JPG instead of WebP


💪Other Features
- 🗑️ Auto-delete original files after successful conversion
- 📊 Live progress bar and detailed logging
- 🎨 Modern dark interface with CustomTkinter
- ⌨️ CLI support for automation
- 🔍 Smart transparency handling: Automatic white background conversion for JPG

-----------
```
BMP    ┐
JPG    ┤
HEIC   ┤                             
GIF    ┤                             
TIFF   ├──► [ Conversion Engine ] ├──► JPG
PNG    ┤                          ├──► PNG
JPEG   ┤                          └──► WEBP                             
TIF    ┤
WEBP   ┘

```
---------

🚀 Installation

🔑Prerequisites
```
Python 3.7 or higher
```
🔎Install Dependencies
```
pip install pillow customtkinter
```

Or use requirements file (if available):
```
pip install -r requirements.txt
```
👩‍💻Download and Run

1.Clone the repository:
```
git clone https://github.com/yourusername/image-converter.git
cd image-converter
```
2.Install packages:
```
pip install -r requirements.txt
```
3.Run the application:
```
python image_converter.py
```
--------

💻 Usage
```
🖼️ GUI Mode (Recommended)
1.Select Input Folder: Click "Browse" next to "Input Folder"
2.Select Output Folder: Specify the save destination
3.Configure Formats: Choose input and output formats
4.Adjust Quality: Set the slider between 60 and 100
5.Additional Options:
  - ☑️ Process Subfolders
  - ☑️ Lossless Mode
  - ☑️ Delete Originals
6.Choose Oversized Handling: Resize / Skip / Convert to JPG
7.Start: Click "Start Converting"! 😀
```

-------

📞 Contact and Support  

- 🐛 Bug Reports: [Issues](https://github.com/Baran-Kamvar/Image-Converter/issues)  
- 💬 Q&A: [Discussions](https://github.com/username/Image-Converter/discussions)  
- 📧 Email: [barankamvar1@gmail.com](mailto:barankamvar1@gmail.com)
