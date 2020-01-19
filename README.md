# Personal Website

This is a personal website I initially wrote while pulling my first all-nighter in college (couldn't sleep because
I had an energy drink). It's currently hosted on Berkeley's Open Computing Facility server and on my GitHub Pages
site. The site is designed to allow for it to be easily repurposed as a template (see instructions below).

* OCF Link: https://ocf.io/jmo
* Github Pages Link: http://yuzhoumo.github.io/

## Using the site as a template

**Change the following files located in** `assets/includes` **to customize page content:**

| File                    | Description                                |
|-------------------------|--------------------------------------------|
| head.html               | Add items to the head tag of all pages     |
| footer.html             | Change the footer text on all pages        |
| nav-links.html          | Change navbar links on all pages           |
| terminal-data.html      | Change the terminal text on all pages      |
| about-main.html         | Main section of home page                  |
| project-tabs.html       | Tabs and tab content of projects page      |
| article-list.html       | Links to posts that appear on blog.html    |
| blog-content-head.html  | Adds html to the top of all articles       |
| blog-content-sub.html   | Adds html to the subtitles of all articles |
| blog-pre-footer.html    | Adds html to the bottom of all articles    |
| blog-quote.html         | Adds blockquote to the top of blog.html    |

Note: Any script tags imported from includes are ignored (presumably to prevent XSS attacks), so scripts must be
directly added to each page.

**Follow these instructions to customize other elements:**

| Element         | Instructions                                                             |
|-----------------|--------------------------------------------------------------------------|
| Profile picture | Replace the jpg file `assets/img/header/profile-picture.jpg`             |
| Navbar logo     | Replace the png file `assets/img/icons/logo.png`                         |
| Terminal title  | Replace the text on lines 13 and 17 in `assets/scipts/terminalRender.js` |

## Creating Blog Posts

Blog posts can be automated by running `make_post.py` from the `cms` folder. Simply input your post in markdown and
specify the paths or links to any media you included in your post. It will automatically update `article-list.html`,
add your markdown to the `blogs/markdown` directory, and add your post to the `blogs` folder after converting it to
HTML and beautifying it. All posts are given a chronological ID (starting from 1) and added to `_post-log.csv`. The
CSV file logs all of the metadata for each post (ID, date, title, length, and post link).