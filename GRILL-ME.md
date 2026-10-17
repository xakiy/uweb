# Grill Me Results

Generated: 2026-10-17T05:53:47.994Z

## Plan

I want to have an admin dashboard where I can see user visit of any page, any suggestions?

## Shared Understanding

Admin dashboard for tracking Wagtail Page visits is implemented with: separate analytics.db, ApexCharts visualization, session deduplication, custom permission, and all endpoints working. Stopping for the day to continue tomorrow.

## Questions and Answers

### 1. What should the dashboard track?

**Recommended answer:** All public page visits (every URL path) — simplest and most useful for a CMS

**User answer:** Only Wagtail Page objects (HomePage, BlogPage, etc.)

**Status:** resolved

**Notes:** Narrower scope than all URLs; tracks per Wagtail Page model instance only.

### 2. Where should visit data be stored?

**Recommended answer:** Database table (Django model + migration) — full control, queryable from admin

**User answer:** I'm thinking about using sqlite as the analytical database instead of integrate it into the main database, what do you think?

**Status:** needs-codebase-check

**Notes:** User prefers separate SQLite DB for analytics. Need to check project's current DB setup.

### 3. What level of detail should the admin dashboard show?

**Recommended answer:** Both: per-page counts + time-series charts — most complete

**User answer:** Charts + time-series (daily/weekly/monthly trends)

**Status:** resolved

**Notes:** User chose charts/trends over per-page table or simple count.

### 4. What filters should be available in the dashboard?

**Recommended answer:** Both: presets + custom date range — best UX

**User answer:** Both: presets + custom date range

**Status:** resolved

**Notes:** User wants both predefined ranges and custom date picker.

### 5. Should each visit record the visitor's identity or session info?

**Recommended answer:** IP address only (anonymous) — lightweight and sufficient for most use cases

**User answer:** Session ID for deduplication

**Status:** resolved

**Notes:** User wants session-based deduplication to reduce noise from repeated refreshes.

### 6. Should the dashboard show real-time active visitors?

**Recommended answer:** No — historical data only, simpler to implement

**User answer:** No — historical data only

**Status:** resolved

**Notes:** User chose no real-time tracking.

### 7. Who should see the dashboard in the admin?

**Recommended answer:** Superusers only — more secure for analytics data

**User answer:** Custom permission (new Django permission)

**Status:** resolved

**Notes:** User wants fine-grained permission control.

### 8. Where should visit data be stored?

**Recommended answer:** Database table (Django model + migration) — full control, queryable from admin

**User answer:** Separate SQLite file (e.g., analytics.db) for analytics data

**Status:** resolved

**Notes:** Separate DB for separation of concerns. Will use Django's DATABASES with a second alias.

### 9. Which Wagtail pages should be tracked?

**Recommended answer:** All pages including sub-pages — complete visibility into every page's traffic

**User answer:** All pages including sub-pages

**Status:** resolved

**Notes:** User confirmed all pages. Will track every Wagtail Page object.

### 10. When a Wagtail page's URL changes, how should existing visit data be handled?

**Recommended answer:** Update existing visits to the new URL — cleaner and simpler

**User answer:** Update existing visits to the new URL

**Status:** resolved

**Notes:** All visits for a page point to its current URL.

### 11. Should admin page views be tracked?

**Recommended answer:** Exclude all admin pages — cleaner analytics for public-facing content

**User answer:** Exclude all admin pages (admin/, django-admin/)

**Status:** resolved

**Notes:** Only public-facing page views are tracked.

### 12. Where should the analytics code live?

**Recommended answer:** New app (e.g., webapps/analytics) — clean separation

**User answer:** New app (e.g., webapps/analytics or core/analytics)

**Status:** resolved

**Notes:** New app with its own models, migrations, admin views.

### 13. Which JavaScript charting library should be used for the analytics dashboard?

**Recommended answer:** Chart.js — lightweight and simple for time-series

**User answer:** ApexCharts — modern, beautiful defaults, great for dashboards

**Status:** resolved

**Notes:** User chose ApexCharts for polished visuals and modern dashboard feel.

## Agreed Decisions

- Separate SQLite file (analytics.db) for analytics data
- ApexCharts for chart visualization
- Session ID deduplication
- Custom Django permission (view_analytics)
- Exclude admin pages from tracking
- Update existing records when page URL changes
- New webapps/analytics app
- Raw SQL with STRFTIME for chart data
- Signal handler for URL change detection
- MenuItem icon_name parameter for Wagtail 7.4
- WAL mode for analytics.db
- Environment variable DB_ANALYTICS for analytics DB path

## Open Risks

- Treebeard E001 warnings about MP_NodeManager (non-blocking)
- analytics.db needs monitoring for growth
- API endpoint may need testing with real traffic data

## Next Decision Needed

Test chart_data API with real visit data and commit all changes
