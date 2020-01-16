# Personal Website

This is a personal website I wrote while pulling my first all-nighter in college. It's currently
hosted on Berkeley's Open Computing Facility server. `website-optimized` is a version of the site
with minified HTML/CSS/JS and compressed images. The site is designed to allow it to be easily
repurposed (see instructions below).

Link: https://ocf.io/jmo

## Using the site as a template

Change the following files located in `assets/includes` to customize page content:

| File               | Description                            |
|--------------------|----------------------------------------|
| head.html          | Add items to the head tag of all pages |
| footer.html        | Change the footer text on all pages    |
| nav-links.html     | Change navbar links on all pages       |
| terminal-data.html | Change the terminal text on all pages  |
| about-main.html    | Main section of home page              |
| project-tabs.html  | Tabs and tab content of projects page  |

Follow these instructions to customize other elements:

| Element         | Instructions                                                             |
|-----------------|--------------------------------------------------------------------------|
| Profile picture | Replace the jpg file `assets/img/header/profile-picture.jpg`             |
| Navbar logo     | Replace the png file `assets/img/icons/logo.png`                         |
| Terminal title  | Replace the text on lines 13 and 17 in `assets/scipts/terminalRender.js` |
