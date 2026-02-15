# 🎨 Image-Converter
<div align="left">
<img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
<img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Version">
<img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python">
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

BMP    ┐
TIFF   ┤
HEIC   ┤                             
GIF    ┤                             
JPG    ├──► [ Conversion Engine ] ├──► JPG
PNG    ┤                          ├──► PNG
JPEG   ┤                          └──► WEBP                             
TIF    ┤
WEBP   ┘

---------
