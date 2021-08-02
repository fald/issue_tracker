# Issue Tracker

Issue Tracker is a Flask-based web app made to track issues across multiple projects.

### Current Features
- Create tickets that include a project name, a title, description, status, and priority for the issue, and the creator/assignee for dealing with the bug.
- Reading issues, either by checking all issues on the home-page, or by searching using a simple search term.
- Updating issues by modifying any of the fields. This also notes the last modified date.
- Deleting issues, which removes them entirely from the DB
- All these functions can be used through making requests (though currently, no API) as well as by using the web app's GUI

### Future Features (in no particular order)
- Implement an auth system. Users will be able to create accounts.
    - A logged-in user will be able to filter issues that mention them in some way (in notes, that they created, or that they have been assigned to)
    - With user accounts, the forms will become simplified, as you won't have to enter your name into the 'creator' section.
    - Authorization will be required for some actions, notable the issue deletion.
- Better search functionality.
    - More search types accounted for; ability to filter and sort by field, for example.
    - A separate 'Advanced Search' form that basically accounts for this increased functionality, but displayed as a form
- Implement a project creation wizard plugin.
    - This will allow you to create a project within the database with all the trimmings, as opposed to just a name. This will help with consistency, and will allow the issue form field to be changed to a drop-down/search instead of just a text input.
- With the addition of users and projects, a page system that includes a 'my projects' or 'my issues', maybe 'current issues'
- Expand on issue statuses
- Adding an extra 'notes' section to issues.
- Linking to Github's issues
- Adding of labels/tags
- Ability to @mention users
- Option for email notification
    - Also would need a notification/message system, I suppose.
- Ability to follow projects, tags, or users
- Add markdown formatting to text fields
- User + Group permissions
- Linking issues; issues may be connected, or there may be a bottleneck, for example


## Installation


# Usage


## Notes
A simple (and as of yet, horrendous) CRUD issue tracker written using Flask which makes use of a database (sqlite).
Currently, the basic functionality is in. However, I have a huge list of additional features that I'm interested in adding.

Let me tell you, holding off on them during the initial project was the hardest thing I've ever (not) done, but I look forward to adding them in now that the threat of scope-creep is effectively nil.


## Motivation
The initial idea was to create an application to demonstrate my understanding of Python and to incorporate various technologies in doing so. Effectively to demonstrate job readiness.
However, pretty quickly, I realized I could actually make use of this myself. Not just in it's basic form, but as part of a larger project management tool - so look forward to that.
The main drive, apart from general job readiness is, due to my interest in data science, Python is a good language to demonstrate ability in. Flask, specficially, is quite simple, and seems to mesh well with displaying simpler projects.

## The Problem
Strictly speaking, there are many issue trackers out there already, so it's a bit of a wheel reinventing, but its something that I can build to my own specifications (as well as expanding it for more generalised use).
We've basically all gone through (or are still going through) those periods of infinitely sprawling project ideas, never finishing one before moving to the next, and then summarily forgetting about the earlier ones.
It's basically nature - what's the next shiny thing?
I hope to create a system that, at least for me, will keep things organized and easily accessible enough that I can flit between projects in a natural way without completely losing the thread on temporarily-abandoned projects.

This will, I hope, result in many more complete and useful projects.

## Tech
As mentioned earlier, this is a **Python** project making use of the **Flask** framework.
As I built it, I also needed to brush up on my **SQL** (using **sqlite3**) skills.
For the front-end, I naturally used **HTML** and tried my hand at some **CSS** - though that quickly overwhelmed and annoyed me, so I simplified by learning some **Bootstrap**
I also made use of some formalized testing (although this was after manually tested and was pretty sure it was working...hm) using **pytest** and **coverage**.
