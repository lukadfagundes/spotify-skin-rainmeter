# Button Images - Design Specifications

## Control Buttons (32x32 pixels)

All control buttons are 32x32 PNG images optimized for size (<5KB each).

### Files Required:
1. **play.png** - Play button (triangle pointing right)
2. **pause.png** - Pause button (two vertical bars)
3. **next.png** - Next track (triangle with vertical bar on right)
4. **previous.png** - Previous track (triangle with vertical bar on left)

### Design Guidelines:
- Size: 32x32 pixels exactly
- Format: PNG-8 with transparency
- Color: White (#FFFFFF) or light gray (#CCCCCC)
- Background: Transparent
- Style: Minimal, flat design
- File size target: <5KB each

### Creating Images:

You can create these using any image editor:

**Option 1: Online Tools**
- Use https://www.pixilart.com/ or similar
- Create 32x32 canvas
- Draw simple geometric shapes
- Export as PNG

**Option 2: Image Editing Software**
- GIMP, Paint.NET, Photoshop, etc.
- Create 32x32 canvas with transparent background
- Use shape tools to draw icons
- Export/optimize as PNG

**Option 3: Icon Fonts**
- Use icon font generators
- Export individual icons as PNG at 32x32

**Option 4: Pre-made Icons**
- Download free icon packs (MIT/CC0 license)
- Resize to 32x32 if needed
- Ensure transparent background

## Default Album Art (200x200 pixels)

**default-album.png** - Placeholder when no album art available

### Specifications:
- Size: 200x200 pixels
- Format: PNG
- Design: Musical note symbol or vinyl record icon
- Background: Dark gray (#2A2A2A) or transparent
- Icon color: Light gray (#CCCCCC)
- File size target: <10KB

### Simple Design Idea:
```
Background: #2A2A2A (dark gray square)
Icon: Musical note (♪) in center, #CCCCCC color
OR
Icon: Vinyl record silhouette
```

## Placeholder Files

Until actual images are created, this README serves as documentation.
The skin will work once proper PNG files are added to this directory.

## Image Optimization

After creating images, optimize with:
- **TinyPNG** (https://tinypng.com/)
- **OptiPNG** (command-line tool)
- **ImageOptim** (Mac)
- **RIOT** (Windows)

Target compression: 70-80% size reduction while maintaining visual quality.
