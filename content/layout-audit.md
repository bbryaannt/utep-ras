# Layout audit — November 8, 2026

Corrected project images by placing them in square overflow-hidden wrappers with explicit 100% image height. HTML image dimensions added for performance had allowed portrait images to retain their intrinsic height; the wrapper now owns geometry. Per-project object positions keep the rover, sensor, and pop-art subject in view.

All pages share a 1200px content span, centered on wide screens, with responsive minimum 24px gutters. This bounds text lengths, photos, headers, footers and callouts. The grid retains the shared gutter geometry.

Reduced title scale, normalized spacing, shortened wide sponsorship layout, added footer separation, and redesigned Join as welcome/schedule and contact columns. No project specifications or achievements were invented. Responsive image sizing hints were adjusted to the bounded content width.

Browser checks: 8 pages × widths 320, 390, 768, 1280, 1920 = 40 layouts. No document horizontal overflow; every project image frame stays square. Desktop crops and sponsor/footer separation were visually checked. Local asset references, headings, and IDs validated. Existing image optimization and local font loading retained.
