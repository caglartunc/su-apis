# SU-APIS website

Website of the Applied Intelligence Systems Lab (SU-APIS) at Sabancı University.

Plain HTML/CSS, served by GitHub Pages. No build step.

- `index.html` — home (intro, research areas, contact)
- `people.html` — members; copy an `<article class="person">` block to add someone
- `publications.html` — publications
- `teaching.html` — courses
- `collaborators.html` — academic and industry partners
- `assets/css/style.css` — all styling
- `assets/img/people/` — member photos (portrait, ~4:5)

Preview locally by opening `index.html` in a browser.

## Regenerating images

- `tools/partners_map.py <ne_110m_admin_0_countries.shp> assets/img/partners-map.png` redraws the collaborators map
  (needs `geopandas matplotlib`; shapefile from naturalearthdata.com, "Admin 0 – Countries", 1:110m).
- `tools/make_cover.py <photo.jpg> assets/img/campus-cover.jpg 420 8 28` builds the half-photo / half-pixel-art cover
  (args: crop top offset, pixel block size, palette colours; needs `pillow numpy`).
