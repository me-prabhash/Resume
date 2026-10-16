---
name: linkedin-banner-updater
description: "LinkedIn Banner Updater - Update Prabhash Thakur's LinkedIn banner HTML with new content, certifications, or styling changes. Use when: user wants to update their LinkedIn banner, change banner content, update certification badges, modify banner text. Triggers: update linkedin banner, linkedin banner, banner update, update banner, linkedin banner updater."
---

# LinkedIn Banner Updater

Update the LinkedIn banner HTML with new content while preserving the established design.

## Setup

**Load** `assets/template.html` to understand the exact HTML structure, CSS styling, and layout.

## Template Structure

The banner is a fixed 1584x396px LinkedIn banner with this layout:

```
+--------------------------------------------------------------+
|  DARK BACKGROUND (navy #0a1628 with gradient overlays)       |
|  City silhouette + glowing city lights (CSS only, no images) |
|                                                              |
|  [LEFT: 300px             |  RIGHT SECTION (flex-end)        |
|   empty space for         |    Top-right: Contact info       |
|   profile picture          |     (email + LinkedIn icons)    |
|   overlay area]           |    Middle-right: Name + Title    |
|                           |    Bottom-right: Cert badges     |
|                           |     (4 image cards in a row)     |
+--------------------------------------------------------------+
```

**Design tokens:**
- Background: `#0a1628` navy with gradient overlays creating depth
- City silhouette: CSS gradients (no images) at bottom
- City lights: radial-gradient dots simulating window lights
- Accent color: `#29b5e8` (LinkedIn blue) for title text and email icon
- Fonts: Montserrat (name, 42px, 800 weight), Open Sans (contact, title)
- Name: white, uppercase, letter-spacing 4px, text-shadow
- Title: `#29b5e8`, uppercase, letter-spacing 3px
- Cert badges: 205x205px cards with glassmorphism (backdrop-filter blur), hover effect
- Contact icons: colored square badges (email: blue gradient, LinkedIn: #0077b5)

**Certification images:**
Badge images are stored at `Linkedin Banner/certification/` and referenced via relative paths.
The output HTML must be written to `Linkedin Banner/` so these paths resolve correctly.

## Workflow

### Step 1: Receive Update Request

The user will provide updates via:
- **Text description** of what to change (e.g., "update my title to Senior Lead Engineer", "add a new certification badge")
- **Attaching a file** with new certification badge images or updated content

**Actions:**
1. Parse the user's request to identify what needs changing:
   - Contact info (email, LinkedIn handle)
   - Name or title text
   - Certification badges (add/remove/reorder)
   - Any styling tweaks
2. If adding a new certification badge, ask the user to provide the image file
3. **Read** the existing banner at `Linkedin Banner/Prabhash_LinkedIn_Banner.html` to merge changes

If the request is ambiguous, ask for clarification.

### Step 2: Generate Updated HTML

**Actions:**
1. **Load** `assets/template.html` for the exact HTML structure and CSS
2. **Apply** the requested changes to the content while preserving all styling:
   - Keep all CSS exactly as-is (backgrounds, gradients, city silhouette, lights)
   - Preserve the 1584x396px dimensions
   - Maintain the left-empty / right-content layout
   - Keep glassmorphism cert badge styling
3. If a new certification badge image is provided:
   - Save it to `Linkedin Banner/certification/` with its original or a descriptive filename
   - Add a new `<div class="cert-badge"><img>` entry
4. **Write** the HTML file to `Linkedin Banner/Prabhash_LinkedIn_Banner.html`

**Rules:**
- Do NOT change the background CSS (gradients, city silhouette, city lights)
- Do NOT change the banner dimensions (1584x396)
- Do NOT change fonts, icon styles, or hover effects
- Do NOT modify the left-section width (300px profile pic space)
- Keep certification badges at 205x205px
- Preserve the instructions div at the bottom for screenshot guidance
- All cert image paths must be relative: `certification/<filename>.png`

### Step 3: Present and Confirm

**Actions:**
1. Tell the user the file has been written
2. Remind them to open in browser and use DevTools screenshot (Ctrl+Shift+P → "Capture node screenshot" on the `.banner` element) to save as image
3. Ask if any adjustments are needed

**STOP**: Wait for user confirmation or revision requests.

### Step 4: Iterate (if needed)

If the user requests changes:
1. **Read** the current banner HTML
2. **Apply** modifications
3. **Write** the updated file
4. Return to Step 3

## Stopping Points

- After Step 1 if request is ambiguous
- After Step 3 for user review

## Output

A single HTML file at `Linkedin Banner/Prabhash_LinkedIn_Banner.html` matching the template design, ready for screenshot capture.
