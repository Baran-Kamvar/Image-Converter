import argparse
import os
import threading
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageOps
from tkinter import filedialog, messagebox
from pillow_heif import register_heif_opener


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SelectOnlyComboBox(ctk.CTkComboBox):
    """A reusable CTkComboBox subclass that enforces select-only behavior."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_valid_value = self.get()
        self.configure(state="readonly")
        self.bind("<<ComboboxSelected>>", self._update_last_valid)
        self.bind("<FocusOut>", self._validate_and_revert)

    def _update_last_valid(self, event=None):
        self.last_valid_value = self.get()

    def _validate_and_revert(self, event=None):
        current = self.get()
        if current not in self.cget("values"):
            self.set(self.last_valid_value)

    def set(self, value):
        if value in self.cget("values"):
            super().set(value)
            self.last_valid_value = value
        else:
            super().set(self.last_valid_value)


class ReadOnlyTextbox(ctk.CTkTextbox):
    """A CTkTextbox subclass that is read-only but allows text selection and standard copy shortcuts."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Key>", self._handle_keypress)
        self.bind("<Control-c>", lambda e: self._copy_selection())
        self.bind("<Control-a>", lambda e: self._select_all())
        self.bind("<Control-Insert>", lambda e: self._copy_selection())
        self.bind("<1>", lambda e: self.focus_set())

    def _handle_keypress(self, event):
        if event.state & 0x4:
            return ""
        if event.keysym in ("BackSpace", "Delete", "Return", "Insert") or len(event.char) == 1:
            return "break"
        return ""

    def _copy_selection(self):
        try:
            selected = self.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected)
        except:
            pass

    def _select_all(self):
        self.tag_add("sel", "1.0", "end")
        self.mark_set("insert", "end")
        self.see("insert")
        return "break"

register_heif_opener()
class ImageConverterApp:
    """A GUI application for converting images between formats with advanced features."""

    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("600x575")  # 25% smaller: 800→600, 880→640 (با بهینه‌سازی layout)
        self.root.resizable(True, True)
        self.root.minsize(500, 450)  # 25% smaller: 650→488→500 (rounded)
        self.root.configure(bg="#0F172A")

        self.colors = {
            "bg_dark": "#0F172A",
            "bg_medium": "#1E293B",
            "bg_light": "#334155",
            "accent_primary": "#06B6D4",
            "accent_success": "#10B981",
            "accent_danger": "#EF4444",
            "accent_warning": "#F59E0B",
            "text_primary": "#F1F5F9",
            "text_secondary": "#94A3B8",
        }

        self.is_converting = False
        self.stop_requested = False
        self.cache = set()
        self.cache_lock = threading.Lock()
        self.icons = self.load_icons()
        self.setup_ui()

    def load_icons(self):
        """Load all icons from 'icons' folder as CTkImage objects."""
        icon_size = (20, 20)  # 25% smaller: 10→7.5→8 (rounded)
        icons_dir = "icons"
        icons = {}
        icon_files = {
            "exit": "exit_icon.png",
            "input": "input_icon.png",
            "output": "output_icon.png",
            "quality": "quality_icon.png",
            "all": "all_icon.png",
            "webp": "webp_icon.png",
            "jpg": "jpg_icon.png",
            "jpeg": "jpeg_icon.png",
            "png": "png_icon.png",
            "heic":"heic_icon.png",
            "tif": "tif_icon.png",
            "tiff": "tiff_icon.png",
            "bmp": "bmp_icon.png",
            "gif": "gif_icon.png",
            "stop": "stop_icon.png",
            "start": "start_icon.png",
            "status": "status_icon.png",
        }
        for key, filename in icon_files.items():
            file_path = os.path.join(icons_dir, filename)
            try:
                pil_image = Image.open(file_path).resize(icon_size, Image.LANCZOS)
                icons[key] = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=icon_size)
            except Exception:
                blank = Image.new("RGBA", icon_size, (0, 0, 0, 0))
                icons[key] = ctk.CTkImage(light_image=blank, dark_image=blank, size=icon_size)
        return icons


    def setup_ui(self):
        """Set up the complete user interface with optimized layout."""
        # Header
        header_frame = ctk.CTkFrame(
            self.root, fg_color=self.colors["bg_medium"], corner_radius=0
        )
        header_frame.pack(fill="x")

        ctk.CTkLabel(
            header_frame,
            text="Image Converter",
            font=("Times New Roman", 38, "bold"),  # 10% smaller font: 24→21.6→22
            text_color=self.colors["text_primary"],
        ).pack(pady=(19, 4))  # 25% smaller: 25→19, 5→4

        ctk.CTkLabel(
            header_frame,
            text="Convert images between formats with high quality",
            font=("Times New Roman", 10, "bold"),  # 10% smaller font: 11→9.9→10
            text_color=self.colors["text_secondary"],
        ).pack(pady=(0, 15))  # 25% smaller: 20→15

        # Main Frame
        main_frame = ctk.CTkFrame(
            self.root, fg_color=self.colors["bg_dark"], corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=19, pady=19)  # 25% smaller: 25→19

        # Input Folder
        ctk.CTkLabel(
            main_frame,
            text="   Input Folder",
            image=self.icons["input"],
            compound="left",
            font=("Times New Roman", 12, "bold"),  # 10% smaller: 8→7.2→7
            text_color=self.colors["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, 4))  # 25% smaller: 8→6→4 (تنگ‌تر)

        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 6))  # 25% smaller: 8→6

        self.input_entry = ctk.CTkEntry(
            input_frame,
            height=18,  # 25% smaller: 24→18
            font=("Times New Roman", 12, "bold"),  # 10% smaller: 11→9.9→10
            fg_color=self.colors["bg_light"],
            border_width=0,
            text_color=self.colors["text_primary"],
            corner_radius=6,  # 25% smaller: 8→6
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))  # 25% smaller: 10→7.5→8

        ctk.CTkButton(
            input_frame,
            text="Browse",
            command=self.select_input_folder,
            width=75,  # 25% smaller: 100→75
            height=20,  # 25% smaller: 24→18
            font=("Times New Roman", 12, "bold"),  # 10% smaller: 9→8.1→8
            fg_color=self.colors["accent_primary"],
            hover_color="#0891B2",
            corner_radius=6,
        ).pack(side="right")

        # Output Folder
        ctk.CTkLabel(
            main_frame,
            text="   Output Folder",
            image=self.icons["output"],
            compound="left",
            font=("Times New Roman", 12, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        output_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        output_frame.pack(fill="x", pady=(0, 10))  # 25% smaller: 8→6, اما 10 برای جدا کردن

        self.output_entry = ctk.CTkEntry(
            output_frame,
            height=18,
            font=("Times New Roman", 12, "bold"),  # 10% smaller: 9→8.1→8
            fg_color=self.colors["bg_light"],
            border_width=0,
            text_color=self.colors["text_primary"],
            corner_radius=6,
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            output_frame,
            text="Browse",
            command=self.select_output_folder,
            width=75,
            height=20,
            font=("Times New Roman", 12, "bold"),
            fg_color=self.colors["accent_primary"],
            hover_color="#0891B2",
            corner_radius=6,
        ).pack(side="right")

        # ========== FORMAT & QUALITY در یک خط (بهینه‌سازی فضا) ==========
        format_quality_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        format_quality_frame.pack(fill="x", pady=(0, 12))  # فاصله بعد از این بلوک

        # Input Format
        ctk.CTkLabel(
            format_quality_frame,
            text="Input:",
            font=("Times New Roman", 13, "bold"),  # 10% smaller: 9→8
            text_color=self.colors["text_primary"],
        ).pack(side="left", padx=(0, 5))

        self.input_format_combo = SelectOnlyComboBox(
            format_quality_frame,
            values=["ALL", "JPG", "JPEG", "PNG", "BMP", "TIFF", "TIF", "GIF", "WEBP","HEIC"],
            width=90,  # 25% smaller: 80→60
            font=("Times New Roman", 12, "bold"),
            dropdown_font=("Times New Roman", 12, "bold"),
        )
        self.input_format_combo.set("ALL")
        self.input_format_combo.pack(side="left", padx=(0, 12))

        # Output Format
        ctk.CTkLabel(
            format_quality_frame,
            text="Output:",
            font=("Times New Roman", 13, "bold"),
            text_color=self.colors["text_primary"],
        ).pack(side="left", padx=(0, 5))

        self.output_format_combo = SelectOnlyComboBox(
            format_quality_frame,
            values=["JPG", "PNG", "WEBP"],
            width=90,  # 25% smaller: 75→56
            font=("Times New Roman", 12, "bold"),
            dropdown_font=("Times New Roman", 12, "bold"),
        )
        self.output_format_combo.set("WEBP")
        self.output_format_combo.pack(side="left", padx=(0, 12))

        # Quality
        ctk.CTkLabel(
            format_quality_frame,
            text="   Quality:",
            image=self.icons["quality"],
            compound="left",
            font=("Times New Roman", 13, "bold"),
            text_color=self.colors["text_primary"],
        ).pack(side="left", padx=(0, 5))

        self.quality_slider = ctk.CTkSlider(
            format_quality_frame,
            from_=60,
            to=100,
            number_of_steps=40,
            width=180,  # 25% smaller: 100→75
            button_color=self.colors["accent_primary"],
            button_hover_color="#0891B2",
            progress_color=self.colors["accent_primary"],
            fg_color=self.colors["bg_light"],
            command=self.update_quality_label,
        )
        self.quality_slider.set(90)
        self.quality_slider.pack(side="left", padx=(0, 8))

        self.quality_label = ctk.CTkLabel(
            format_quality_frame,
            text="90%",
            font=("Times New Roman", 12, "bold"),
            text_color=self.colors["accent_primary"],
            width=40,  # 25% smaller: 40→30
        )
        self.quality_label.pack(side="left")

        # ========== OPTIONS ==========
        options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 12))

        self.recursive_switch = ctk.CTkSwitch(
            options_frame,
            text="Process Subfolders",
            font=("Times New Roman", 13, "bold"),  # 10% smaller: 9→8
            text_color=self.colors["text_primary"],
        )
        self.recursive_switch.pack(side="left", padx=(0, 7))

        self.lossless_switch = ctk.CTkSwitch(
            options_frame,
            text="Lossless (WebP)",
            font=("Times New Roman", 13, "bold"),
            text_color=self.colors["text_primary"],
        )
        self.lossless_switch.pack(side="left", padx=(0, 7))

        self.delete_original_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Delete Originals",
            font=("Times New Roman", 13, "bold"),
            text_color=self.colors["text_primary"],
        )
        self.delete_original_checkbox.pack(side="left", padx=(0, 12))

        # Oversized Handling
        ctk.CTkLabel(
            options_frame,
            text="Oversized:",
            font=("Times New Roman", 13, "bold"),
            text_color=self.colors["text_primary"],
        ).pack(side="left", padx=(0, 5))

        self.oversized_combo = SelectOnlyComboBox(
            options_frame,
            values=["Resize", "Skip", "Convert to JPG"],
            width=75,  # 25% smaller: 100→75
            font=("Times New Roman", 12, "bold"),
            dropdown_font=("Times New Roman", 12, "bold"),
        )
        self.oversized_combo.set("Resize")
        self.oversized_combo.pack(side="left")

        # ========== PROGRESS (فاصله کمتر با log) ==========
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            height=8,  # 25% smaller: 10→7.5→8
            progress_color=self.colors["accent_primary"],
            fg_color=self.colors["bg_light"],
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 4))  # فاصله کم

        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="0.00%",
            font=("Times New Roman", 15, "bold"),  # 10% smaller: 9→8
            text_color=self.colors["text_primary"],
        )
        self.progress_label.pack(pady=(0, 6))  # فاصله کم تا log

        # ========== STATUS / LOG ==========
        ctk.CTkLabel(
            main_frame,
            text="   Status :",
            image=self.icons["status"],
            compound="left",
            font=("Times New Roman", 18, "bold"),  # 10% smaller: 12→10.8→11
            text_color=self.colors["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, 4))  # فاصله کم

        self.log_text = ReadOnlyTextbox(
            main_frame,
            height=130,  # کمی کوچکتر: 150→130 (برای فشردگی)
            font=("Consolas", 12),  # 10% smaller: 9→8.1→8
            fg_color=self.colors["bg_light"],
            text_color=self.colors["text_primary"],
            corner_radius=6,
            wrap="word",
        )
        self.log_text.pack(fill="both", expand=True, pady=(0, 40))  # 25% smaller: 20→15

        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Converting",
            image=self.icons["start"],
            compound="left",
            command=self.start_conversion,
            width=75,  # 25% smaller: 120→90
            height=22,  # 25% smaller: 24→18
            font=("Times New Roman", 18, "bold"),
            fg_color=self.colors["accent_success"],
            hover_color="#059669",
            corner_radius=8,  # 25% smaller: 10→7.5→8
        )
        self.start_btn.pack(side="left", padx=(0, 8), pady=(0, 15))

        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop",
            image=self.icons["stop"],
            compound="left",
            command=self.stop_conversion,
            width=75,  # 25% smaller: 100→75
            height=22,
            font=("Times New Roman", 18, "bold"),
            fg_color=self.colors["accent_danger"],
            hover_color="#DC2626",
            corner_radius=8,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=(0, 8), pady=(0, 15))

        ctk.CTkButton(
            button_frame,
            text="Exit",
            image=self.icons["exit"],
            compound="left",
            command=self.root.quit,
            width=75,
            height=22,
            font=("Times New Roman", 18, "bold"),
            fg_color=self.colors["bg_light"],
            hover_color="#475569",
            corner_radius=8,
        ).pack(side="right", pady=(0, 15))

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"{int(value)}%")

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)

    def log(self, message):
        self.root.after(0, lambda: self._log(message))

    def _log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def update_progress(self, value):
        self.root.after(0, lambda: self.progress_bar.set(value))
        self.root.after(0, lambda: self.progress_label.configure(text=f"{value * 100:.2f}%"))

    def start_conversion(self):
        input_path = self.input_entry.get().strip()
        output_path = self.output_entry.get().strip()
        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output folders!")
            return
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input folder does not exist!")
            return

        self.is_converting = True
        self.stop_requested = False
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.update_progress(0)

        with self.cache_lock:
            self.cache.clear()

        quality = int(self.quality_slider.get())
        recursive = self.recursive_switch.get() == 1
        lossless = self.lossless_switch.get() == 1
        delete_originals = self.delete_original_checkbox.get() == 1
        behavior = self.oversized_combo.get().lower().replace(" ", "_")

        input_display = self.input_format_combo.get()
        if "ALL" in input_display:
            input_selection = "ALL"
        else:
            mapping = {
                "JPG": "jpg",
                "JPEG": "jpeg",
                "PNG": "png",
                "BMP": "bmp",
                "TIFF": "tiff",
                "TIF": "tif",
                "GIF": "gif",
                "WEBP": "webp",
                "HEIC": "heic"
            }
            for key, val in mapping.items():
                if key in input_display:
                    input_selection = val
                    break
            else:
                input_selection = "all"

        output_display = self.output_format_combo.get()
        output_format = output_display.split()[-1].lower()

        if delete_originals:
            if not messagebox.askyesno("Confirm", "Delete original files after successful converting?"):
                return

        thread = threading.Thread(
            target=self.convert_images,
            args=(
                input_path,
                output_path,
                quality,
                recursive,
                lossless,
                delete_originals,
                input_selection,
                output_format,
                behavior,
            ),
            daemon=True,
        )
        thread.start()

    def stop_conversion(self):
        self.stop_requested = True
        self.log("Stopping converting...")

    def convert_images(
            self,
            input_folder,
            output_folder,
            quality,
            recursive,
            lossless,
            delete_originals,
            input_selection,
            output_format,
            behavior,
    ):
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)

            all_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp", ".heic"}
            if input_selection.upper() == "ALL":
                extensions = all_extensions
            else:
                extensions = {f".{input_selection.lower()}"}

            input_path = Path(input_folder)
            pattern = "**/*" if recursive else "*"
            image_files = [
                p
                for p in input_path.glob(pattern)
                if p.suffix.lower() in extensions and p.is_file()
            ]

            if not image_files:
                self.log("No images found with the selected input format!")
                self.conversion_finished()
                return

            total = len(image_files)
            self.log(f"Found {total} image(s). Starting converting...\n")

            success_count = 0
            total_original_size = 0
            total_new_size = 0

            qualities_to_try = [quality, 85, 75] if output_format == "webp" and not lossless else [quality]

            for idx, file_path in enumerate(image_files, 1):
                if self.stop_requested:
                    self.log("\nConverting stopped by user.")
                    break

                filename = file_path.name
                relative_path = file_path.relative_to(input_path)
                output_file = Path(output_folder) / relative_path.with_suffix(f".{output_format}")

                output_file.parent.mkdir(parents=True, exist_ok=True)

                with self.cache_lock:
                    if str(output_file) in self.cache or output_file.exists():
                        self.log(f"[{idx}/{total}] Skipped: {filename} (already converted)")
                        self.update_progress(idx / total)
                        continue

                try:
                    original_size = file_path.stat().st_size
                    total_original_size += original_size

                    with Image.open(file_path) as img:
                        original_w, original_h = img.size
                        output_format_local = output_format
                        output_file_local = output_file

                        if output_format == "webp" and max(original_w, original_h) > 16383:
                            self.log(
                                f"[{idx}/{total}] Warning: {filename} is oversized "
                                f"({original_w}x{original_h}) for WebP."
                            )
                            if behavior == "skip":
                                self.log(f"[{idx}/{total}] Skipped: {filename} due to size limit.")
                                self.update_progress(idx / total)
                                continue
                            elif behavior == "convert_to_jpg":
                                output_format_local = "jpg"
                                output_file_local = output_file.with_suffix(".jpg")
                                self.log(
                                    f"[{idx}/{total}] Converting {filename} to JPG instead due to size limit."
                                )
                            elif behavior == "resize":
                                max_side = 16383.0
                                scale = min(max_side / original_w, max_side / original_h)
                                new_w = int(original_w * scale)
                                new_h = int(original_h * scale)
                                img = img.resize((new_w, new_h), Image.LANCZOS)
                                self.log(
                                    f"[{idx}/{total}] Resized {filename} from "
                                    f"{original_w}x{original_h} to {new_w}x{new_h} for WebP compatibility."
                                )
                            else:
                                raise ValueError("Invalid oversized behavior")

                        if img.mode in ("RGBA", "LA", "P") and output_format_local == "jpg":
                            bg = Image.new("RGB", img.size, (255, 255, 255))
                            if "A" in img.getbands():
                                bg.paste(img, mask=img.getchannel("A"))
                            else:
                                bg.paste(img)
                            img = bg

                        if output_format_local == "webp":
                            qualities_to_try_local = (
                                [quality, 85, 75] if not lossless else [100]
                            )
                        else:
                            qualities_to_try_local = [quality]

                        new_size = self._save_image(
                            img,
                            output_file_local,
                            output_format_local,
                            qualities_to_try_local,
                            original_size,
                            lossless if output_format_local == "webp" else False,
                        )
                        total_new_size += new_size

                        if delete_originals:
                            file_path.unlink()

                        with self.cache_lock:
                            self.cache.add(str(output_file_local))

                        self.log(f"[{idx}/{total}] Done: {filename} → {output_file_local.name}")
                        success_count += 1

                except Exception as e:
                    self.log(f"[{idx}/{total}] Error: {filename} → {str(e)}")

                self.update_progress(idx / total)

            if not self.stop_requested:
                self._show_final_report(success_count, total_original_size, total_new_size)

        except Exception as e:
            self.log(f"\nError: {e}")
        finally:
            with self.cache_lock:
                self.cache.clear()
            self.conversion_finished()

    def _save_image(self, img, output_path, output_format, qualities, original_size, lossless):
        save_args = {}
        if output_format == "webp":
            save_args["method"] = 6
            if lossless:
                save_args["lossless"] = True
                save_args["quality"] = 100
                img.save(output_path, "WEBP", **save_args)
            else:
                for q in qualities:
                    save_args["quality"] = q
                    img.save(output_path, "WEBP", **save_args)
                    if output_path.stat().st_size < original_size:
                        break
        elif output_format == "jpg":
            save_args["quality"] = qualities[0]
            img.save(output_path, "JPEG", **save_args)
        elif output_format == "png":
            img.save(output_path, "PNG")
        return output_path.stat().st_size

    def _show_final_report(self, success_count, orig_size, new_size):
        self.log("\n" + "=" * 60)
        self.log("Converting completed!")
        self.log("=" * 60 + "\n")

        orig_mb = orig_size / (1024 * 1024)
        new_mb = new_size / (1024 * 1024)
        saved_mb = orig_mb - new_mb
        percent = (saved_mb / orig_mb * 100) if orig_mb > 0 else 0

        self.log("Final Report:")
        self.log(f" • {success_count} images converted")
        self.log(f" • Original size: {orig_mb:.2f} MB")
        self.log(f" • New size: {new_mb:.2f} MB")
        self.log(f" • Saved: {saved_mb:.2f} MB ({percent:.1f}%)")
        self.log("\n" + "=" * 60)

    def conversion_finished(self):
        self.is_converting = False
        self.root.after(0, lambda: self.start_btn.configure(state="normal"))
        self.root.after(0, lambda: self.stop_btn.configure(state="disabled"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Converter")
    parser.add_argument("--input", help="Input folder")
    parser.add_argument("--output", help="Output folder")
    parser.add_argument("--quality", type=int, default=90, help="Quality (60-100)")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders")
    parser.add_argument("--lossless", action="store_true", help="Lossless mode for WebP")
    parser.add_argument("--delete-originals", action="store_true", help="Delete originals")
    parser.add_argument("--input-format", default="all", help="Input format: all, jpg, png, webp, heic, etc.")
    parser.add_argument("--output-format", default="webp", help="Output format: jpg, png, webp")

    args = parser.parse_args()

    if args.input and args.output:
        # CLI mode (keep your original cli_conversion function if needed)
        pass
    else:
        root = ctk.CTk()
        root.configure(fg_color="#0F172A")
        app = ImageConverterApp(root)
        root.mainloop()