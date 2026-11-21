# Candidate Google APIs - outline

Generated 11-21-2026 by describe_apis.py from Google's public discovery documents.

## appsmarket v2 - Google Workspace Marketplace API

Lets your Google Workspace Marketplace applications integrate with Google's installtion and licensing services.

Base URL: `https://appsmarket.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/appsmarketplace.license` - View your installed application's licensing information

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| customerLicense | get | GET | `appsmarket/v2/customerLicense/{applicationId}/{customerId}` | applicationId, customerId |
| userLicense | get | GET | `appsmarket/v2/userLicense/{applicationId}/{userId}` | applicationId, userId |

## script v1 - Apps Script API

Manages and executes Google Apps Script projects.

Base URL: `https://script.googleapis.com/`

OAuth scopes:
* `https://mail.google.com/` - Read, compose, send, and permanently delete all your email from Gmail
* `https://www.google.com/calendar/feeds` - See, edit, share, and permanently delete all the calendars you can access using Google Calendar
* `https://www.google.com/m8/feeds` - See, edit, download, and permanently delete your contacts
* `https://www.googleapis.com/auth/admin.directory.group` - View and manage the provisioning of groups on your domain
* `https://www.googleapis.com/auth/admin.directory.user` - View and manage the provisioning of users on your domain
* `https://www.googleapis.com/auth/documents` - See, edit, create, and delete all your Google Docs documents
* `https://www.googleapis.com/auth/drive` - See, edit, create, and delete all of your Google Drive files
* `https://www.googleapis.com/auth/forms` - View and manage your forms in Google Drive
* `https://www.googleapis.com/auth/forms.currentonly` - View and manage forms that this application has been installed in
* `https://www.googleapis.com/auth/groups` - View and manage your Google Groups
* `https://www.googleapis.com/auth/script.deployments` - Create and update Google Apps Script deployments
* `https://www.googleapis.com/auth/script.deployments.readonly` - View Google Apps Script deployments
* `https://www.googleapis.com/auth/script.metrics` - View Google Apps Script project's metrics
* `https://www.googleapis.com/auth/script.processes` - View Google Apps Script processes
* `https://www.googleapis.com/auth/script.projects` - Create and update Google Apps Script projects
* `https://www.googleapis.com/auth/script.projects.readonly` - View Google Apps Script projects
* `https://www.googleapis.com/auth/spreadsheets` - See, edit, create, and delete all your Google Sheets spreadsheets
* `https://www.googleapis.com/auth/userinfo.email` - See your primary Google Account email address

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| processes | list | GET | `v1/processes` |  |
| processes | listScriptProcesses | GET | `v1/processes:listScriptProcesses` |  |
| projects | create | POST | `v1/projects` |  |
| projects | get | GET | `v1/projects/{scriptId}` | scriptId |
| projects | getContent | GET | `v1/projects/{scriptId}/content` | scriptId |
| projects | getMetrics | GET | `v1/projects/{scriptId}/metrics` | scriptId |
| projects | updateContent | PUT | `v1/projects/{scriptId}/content` | scriptId |
| projects/deployments | create | POST | `v1/projects/{scriptId}/deployments` | scriptId |
| projects/deployments | delete | DELETE | `v1/projects/{scriptId}/deployments/{deploymentId}` | deploymentId, scriptId |
| projects/deployments | get | GET | `v1/projects/{scriptId}/deployments/{deploymentId}` | deploymentId, scriptId |
| projects/deployments | list | GET | `v1/projects/{scriptId}/deployments` | scriptId |
| projects/deployments | update | PUT | `v1/projects/{scriptId}/deployments/{deploymentId}` | deploymentId, scriptId |
| projects/versions | create | POST | `v1/projects/{scriptId}/versions` | scriptId |
| projects/versions | get | GET | `v1/projects/{scriptId}/versions/{versionNumber}` | scriptId, versionNumber |
| projects/versions | list | GET | `v1/projects/{scriptId}/versions` | scriptId |
| scripts | run | POST | `v1/scripts/{scriptId}:run` | scriptId |

## slides v1 - Google Slides API

Reads and writes Google Slides presentations.

Base URL: `https://slides.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/drive` - See, edit, create, and delete all of your Google Drive files
* `https://www.googleapis.com/auth/drive.file` - See, edit, create, and delete only the specific Google Drive files you use with this app
* `https://www.googleapis.com/auth/drive.readonly` - See and download all your Google Drive files
* `https://www.googleapis.com/auth/presentations` - See, edit, create, and delete all your Google Slides presentations
* `https://www.googleapis.com/auth/presentations.readonly` - See all your Google Slides presentations
* `https://www.googleapis.com/auth/spreadsheets` - See, edit, create, and delete all your Google Sheets spreadsheets
* `https://www.googleapis.com/auth/spreadsheets.readonly` - See all your Google Sheets spreadsheets

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| presentations | batchUpdate | POST | `v1/presentations/{presentationId}:batchUpdate` | presentationId |
| presentations | create | POST | `v1/presentations` |  |
| presentations | get | GET | `v1/presentations/{+presentationId}` | presentationId |
| presentations/pages | get | GET | `v1/presentations/{presentationId}/pages/{pageObjectId}` | pageObjectId, presentationId |
| presentations/pages | getThumbnail | GET | `v1/presentations/{presentationId}/pages/{pageObjectId}/thumbnail` | pageObjectId, presentationId |

## workspaceevents v1 - Google Workspace Events API

The Google Workspace Events API lets you subscribe to events and manage change notifications across Google Workspace applications.

Base URL: `https://workspaceevents.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/chat.app.all.memberships.readonly` - On their own behalf, apps in Google Chat can see all members in Google Chat spaces and conversations throughout your Workspace organization, even when the Chat app isn't a member
* `https://www.googleapis.com/auth/chat.app.all.messages.readonly` - On their own behalf, apps in Google Chat can see all messages and reactions throughout your Workspace organization, even when the Chat app isn't a member of a space or conversation
* `https://www.googleapis.com/auth/chat.app.all.spaces.readonly` - On their own behalf, apps in Google Chat can see metadata about all spaces and conversations in Google Chat throughout your Workspace organization, even when the Chat app isn't a member
* `https://www.googleapis.com/auth/chat.app.all.users.readstate.readonly` - On their own behalf, apps in Google Chat can see the last read time for all users in all spaces and conversations throughout your Workspace organization, even when the Chat app isn't a member.
* `https://www.googleapis.com/auth/chat.app.memberships` - On their own behalf, apps in Google Chat can see, add, update, and remove members from conversations and spaces
* `https://www.googleapis.com/auth/chat.app.memberships.readonly` - On their own behalf, apps in Google Chat can see members of conversations and spaces
* `https://www.googleapis.com/auth/chat.app.messages.readonly` - On their own behalf, apps in Google Chat can see all messages and their associated reactions and message content
* `https://www.googleapis.com/auth/chat.app.spaces` - On their own behalf, apps in Google Chat can create conversations and spaces and see or update their metadata (including history settings and access settings)
* `https://www.googleapis.com/auth/chat.app.spaces.readonly` - On their own behalf, apps in Google Chat can see conversations and spaces and their metadata (including history settings and access settings)
* `https://www.googleapis.com/auth/chat.bot` - Private Service: https://www.googleapis.com/auth/chat.bot
* `https://www.googleapis.com/auth/chat.memberships` - See, add, update, and remove members from conversations and spaces in Google Chat
* `https://www.googleapis.com/auth/chat.memberships.readonly` - View members in Google Chat conversations.
* `https://www.googleapis.com/auth/chat.messages` - See, compose, send, update, and delete messages, their content, and attached cards; add, see, and delete reactions to messages.
* `https://www.googleapis.com/auth/chat.messages.reactions` - See, add, and delete reactions as well as their reaction content to messages in Google Chat
* `https://www.googleapis.com/auth/chat.messages.reactions.readonly` - View reactions as well as their reaction content to messages in Google Chat
* `https://www.googleapis.com/auth/chat.messages.readonly` - See messages as well as their reactions and message content in Google Chat
* `https://www.googleapis.com/auth/chat.spaces` - Create conversations and spaces and see or update metadata (including history settings and access settings) in Google Chat
* `https://www.googleapis.com/auth/chat.spaces.readonly` - View chat and spaces in Google Chat
* `https://www.googleapis.com/auth/chat.users.availability` - See and change your availability status in Google Chat.
* `https://www.googleapis.com/auth/chat.users.availability.readonly` - See your availability status in Google Chat.
* `https://www.googleapis.com/auth/chat.users.readstate` - View and modify last read time for Google Chat conversations
* `https://www.googleapis.com/auth/chat.users.readstate.readonly` - View last read time for Google Chat conversations
* `https://www.googleapis.com/auth/drive` - See, edit, create, and delete all of your Google Drive files
* `https://www.googleapis.com/auth/drive.file` - See, edit, create, and delete only the specific Google Drive files you use with this app
* `https://www.googleapis.com/auth/drive.metadata` - View and manage metadata of files in your Google Drive
* `https://www.googleapis.com/auth/drive.metadata.readonly` - See information about your Google Drive files
* `https://www.googleapis.com/auth/drive.readonly` - See and download all your Google Drive files
* `https://www.googleapis.com/auth/meetings.space.created` - Create, edit, and see information about your Google Meet conferences created by the app.
* `https://www.googleapis.com/auth/meetings.space.readonly` - Read information about any of your Google Meet conferences

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| operations | get | GET | `v1/{+name}` | name |
| subscriptions | create | POST | `v1/subscriptions` |  |
| subscriptions | delete | DELETE | `v1/{+name}` | name |
| subscriptions | get | GET | `v1/{+name}` | name |
| subscriptions | list | GET | `v1/subscriptions` |  |
| subscriptions | patch | PATCH | `v1/{+name}` | name |
| subscriptions | reactivate | POST | `v1/{+name}:reactivate` | name |

## gmailpostmastertools v2 - Gmail Postmaster Tools API

The Postmaster Tools API is a RESTful API that provides programmatic access to email traffic metrics (like spam reports, delivery errors etc) otherwise available through the Gmail Postmaster Tools UI currently.

Base URL: `https://gmailpostmastertools.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/postmaster` - Get email traffic metrics, manage domains, and manage domain users for the domains you have registered with Postmaster Tools
* `https://www.googleapis.com/auth/postmaster.domain` - View and manage the domains you have registered with Postmaster Tools
* `https://www.googleapis.com/auth/postmaster.traffic.readonly` - Get email traffic metrics for the domains you have registered with Postmaster Tools
* `https://www.googleapis.com/auth/postmaster.user` - View and manage users for the domains you have registered with Postmaster Tools

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| domainStats | batchQuery | POST | `v2/domainStats:batchQuery` |  |
| domains | create | POST | `v2/domains` |  |
| domains | delete | DELETE | `v2/{+name}` | name |
| domains | get | GET | `v2/{+name}` | name |
| domains | getComplianceStatus | GET | `v2/{+name}` | name |
| domains | getVerificationToken | GET | `v2/{+name}` | name |
| domains | list | GET | `v2/domains` |  |
| domains | verify | POST | `v2/{+name}:verify` | name |
| domains/domainStats | query | POST | `v2/{+parent}/domainStats:query` | parent |
| domains/users | create | POST | `v2/{+parent}/users` | parent |
| domains/users | delete | DELETE | `v2/{+name}` | name |
| domains/users | get | GET | `v2/{+name}` | name |
| domains/users | list | GET | `v2/{+parent}/users` | parent |
| domains/users | patch | PATCH | `v2/{+name}` | name |

## cloudsearch v1 - Cloud Search API

Cloud Search provides cloud-based search capabilities over Google Workspace data. The Cloud Search API allows indexing of non-Google Workspace data into Cloud Search.

Base URL: `https://cloudsearch.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/cloud_search` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.debug` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.indexing` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.query` - Search your organization's data in the Cloud Search index
* `https://www.googleapis.com/auth/cloud_search.settings` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.settings.indexing` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.settings.query` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.stats` - Index and serve your organization's data with Cloud Search
* `https://www.googleapis.com/auth/cloud_search.stats.indexing` - Index and serve your organization's data with Cloud Search

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| debug/datasources/items | checkAccess | POST | `v1/debug/{+name}:checkAccess` | name |
| debug/datasources/items | searchByViewUrl | POST | `v1/debug/{+name}/items:searchByViewUrl` | name |
| debug/datasources/items/unmappedids | list | GET | `v1/debug/{+parent}/unmappedids` | parent |
| debug/identitysources/items | listForunmappedidentity | GET | `v1/debug/{+parent}/items:forunmappedidentity` | parent |
| debug/identitysources/unmappedids | list | GET | `v1/debug/{+parent}/unmappedids` | parent |
| indexing/datasources | deleteSchema | DELETE | `v1/indexing/{+name}/schema` | name |
| indexing/datasources | getSchema | GET | `v1/indexing/{+name}/schema` | name |
| indexing/datasources | updateSchema | PUT | `v1/indexing/{+name}/schema` | name |
| indexing/datasources/items | delete | DELETE | `v1/indexing/{+name}` | name |
| indexing/datasources/items | deleteQueueItems | POST | `v1/indexing/{+name}/items:deleteQueueItems` | name |
| indexing/datasources/items | get | GET | `v1/indexing/{+name}` | name |
| indexing/datasources/items | index | POST | `v1/indexing/{+name}:index` | name |
| indexing/datasources/items | list | GET | `v1/indexing/{+name}/items` | name |
| indexing/datasources/items | poll | POST | `v1/indexing/{+name}/items:poll` | name |
| indexing/datasources/items | push | POST | `v1/indexing/{+name}:push` | name |
| indexing/datasources/items | unreserve | POST | `v1/indexing/{+name}/items:unreserve` | name |
| indexing/datasources/items | upload | POST | `v1/indexing/{+name}:upload` | name |
| media | upload | POST | `v1/media/{+resourceName}` | resourceName |
| operations | get | GET | `v1/{+name}` | name |
| operations/lro | list | GET | `v1/{+name}/lro` | name |
| query | removeActivity | POST | `v1/query:removeActivity` |  |
| query | search | POST | `v1/query/search` |  |
| query | suggest | POST | `v1/query/suggest` |  |
| query/sources | list | GET | `v1/query/sources` |  |
| settings | getCustomer | GET | `v1/settings/customer` |  |
| settings | updateCustomer | PATCH | `v1/settings/customer` |  |
| settings/datasources | create | POST | `v1/settings/datasources` |  |
| settings/datasources | delete | DELETE | `v1/settings/{+name}` | name |
| settings/datasources | get | GET | `v1/settings/{+name}` | name |
| settings/datasources | list | GET | `v1/settings/datasources` |  |
| settings/datasources | patch | PATCH | `v1/settings/{+name}` | name |
| settings/datasources | update | PUT | `v1/settings/{+name}` | name |
| settings/searchapplications | create | POST | `v1/settings/searchapplications` |  |
| settings/searchapplications | delete | DELETE | `v1/settings/{+name}` | name |
| settings/searchapplications | get | GET | `v1/settings/{+name}` | name |
| settings/searchapplications | list | GET | `v1/settings/searchapplications` |  |
| settings/searchapplications | patch | PATCH | `v1/settings/{+name}` | name |
| settings/searchapplications | reset | POST | `v1/settings/{+name}:reset` | name |
| settings/searchapplications | update | PUT | `v1/settings/{+name}` | name |
| stats | getIndex | GET | `v1/stats/index` |  |
| stats | getQuery | GET | `v1/stats/query` |  |
| stats | getSearchapplication | GET | `v1/stats/searchapplication` |  |
| stats | getSession | GET | `v1/stats/session` |  |
| stats | getUser | GET | `v1/stats/user` |  |
| stats/index/datasources | get | GET | `v1/stats/index/{+name}` | name |
| stats/query/searchapplications | get | GET | `v1/stats/query/{+name}` | name |
| stats/session/searchapplications | get | GET | `v1/stats/session/{+name}` | name |
| stats/user/searchapplications | get | GET | `v1/stats/user/{+name}` | name |
| v1 | initializeCustomer | POST | `v1:initializeCustomer` |  |

## dataportability v1 - Data Portability API

The Data Portability API lets you build applications that request authorization from a user to move a copy of data from Google services into your application. This enables data portability and facilitates switching services.

Base URL: `https://dataportability.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/dataportability.alerts.subscriptions` - Move a copy of the Google Alerts subscriptions you created
* `https://www.googleapis.com/auth/dataportability.chrome.autofill` - Move a copy of the information you entered into online forms in Chrome
* `https://www.googleapis.com/auth/dataportability.chrome.bookmarks` - Move a copy of pages you bookmarked in Chrome
* `https://www.googleapis.com/auth/dataportability.chrome.dictionary` - Move a copy of words you added to Chrome's dictionary
* `https://www.googleapis.com/auth/dataportability.chrome.extensions` - Move a copy of extensions you installed from the Chrome Web Store
* `https://www.googleapis.com/auth/dataportability.chrome.history` - Move a copy of sites you visited in Chrome
* `https://www.googleapis.com/auth/dataportability.chrome.reading_list` - Move a copy of pages you added to your reading list in Chrome
* `https://www.googleapis.com/auth/dataportability.chrome.settings` - Move a copy of your settings in Chrome
* `https://www.googleapis.com/auth/dataportability.discover.follows` - Move a copy of searches and sites you follow, saved by Discover
* `https://www.googleapis.com/auth/dataportability.discover.likes` - Move a copy of links to your liked documents, saved by Discover
* `https://www.googleapis.com/auth/dataportability.discover.not_interested` - Move a copy of content you marked as not interested, saved by Discover
* `https://www.googleapis.com/auth/dataportability.maps.aliased_places` - Move a copy of the places you labeled on Maps
* `https://www.googleapis.com/auth/dataportability.maps.commute_routes` - Move a copy of your pinned trips on Maps
* `https://www.googleapis.com/auth/dataportability.maps.commute_settings` - Move a copy of your commute settings on Maps
* `https://www.googleapis.com/auth/dataportability.maps.ev_profile` - Move a copy of your electric vehicle profile on Maps
* `https://www.googleapis.com/auth/dataportability.maps.factual_contributions` - Move a copy of the corrections you made to places or map information on Maps
* `https://www.googleapis.com/auth/dataportability.maps.offering_contributions` - Move a copy of your updates to places on Maps
* `https://www.googleapis.com/auth/dataportability.maps.photos_videos` - Move a copy of the photos and videos you posted on Maps
* `https://www.googleapis.com/auth/dataportability.maps.questions_answers` - Move a copy of the questions and answers you posted on Maps
* `https://www.googleapis.com/auth/dataportability.maps.reviews` - Move a copy of your reviews and posts on Maps
* `https://www.googleapis.com/auth/dataportability.maps.starred_places` - Move a copy of your Starred places list on Maps
* `https://www.googleapis.com/auth/dataportability.maps.vehicle_profile` - Move a copy of your vehicle profile on Maps
* `https://www.googleapis.com/auth/dataportability.myactivity.maps` - Move a copy of your Maps activity
* `https://www.googleapis.com/auth/dataportability.myactivity.myadcenter` - Move a copy of your My Ad Center activity
* `https://www.googleapis.com/auth/dataportability.myactivity.play` - Move a copy of your Google Play activity
* `https://www.googleapis.com/auth/dataportability.myactivity.search` - Move a copy of your Google Search activity
* `https://www.googleapis.com/auth/dataportability.myactivity.shopping` - Move a copy of your Shopping activity
* `https://www.googleapis.com/auth/dataportability.myactivity.youtube` - Move a copy of your YouTube activity
* `https://www.googleapis.com/auth/dataportability.mymaps.maps` - Move a copy of the maps you created in My Maps
* `https://www.googleapis.com/auth/dataportability.nest.camera_event` - Copy Nest camera event data
* `https://www.googleapis.com/auth/dataportability.nest.camera_feature` - Copy Nest camera feature data
* `https://www.googleapis.com/auth/dataportability.nest.camera_video` - Copy Nest camera footage
* `https://www.googleapis.com/auth/dataportability.nest.store` - Copy your Nest Store and Nest Renew billing and payment information
* `https://www.googleapis.com/auth/dataportability.nest.user` - Copy your Nest user information
* `https://www.googleapis.com/auth/dataportability.pixel.device_data` - Usage and diagnostic data from your Pixel devices.
* `https://www.googleapis.com/auth/dataportability.play.devices` - Move a copy of information about your devices with Google Play Store installed
* `https://www.googleapis.com/auth/dataportability.play.grouping` - Move a copy of your Google Play Store Grouping tags created by app developers
* `https://www.googleapis.com/auth/dataportability.play.installs` - Move a copy of your Google Play Store app installations
* `https://www.googleapis.com/auth/dataportability.play.library` - Move a copy of your Google Play Store downloads, including books, games, and apps
* `https://www.googleapis.com/auth/dataportability.play.playpoints` - Move a copy of information about your Google Play Store Points
* `https://www.googleapis.com/auth/dataportability.play.promotions` - Move a copy of information about your Google Play Store promotions
* `https://www.googleapis.com/auth/dataportability.play.purchases` - Move a copy of your Google Play Store purchases
* `https://www.googleapis.com/auth/dataportability.play.redemptions` - Move a copy of your Google Play Store redemption activities
* `https://www.googleapis.com/auth/dataportability.play.subscriptions` - Move a copy of your Google Play Store subscriptions
* `https://www.googleapis.com/auth/dataportability.play.usersettings` - Move a copy of your Google Play Store user settings and preferences
* `https://www.googleapis.com/auth/dataportability.saved.collections` - Move a copy of your saved links, images, places, and collections from your use of Google services
* `https://www.googleapis.com/auth/dataportability.search_ugc.comments` - Move a copy of your comments on Google Search
* `https://www.googleapis.com/auth/dataportability.search_ugc.media.reviews_and_stars` - Move a copy of your media reviews on Google Search
* `https://www.googleapis.com/auth/dataportability.search_ugc.media.streaming_video_providers` - Move a copy of your self-reported video streaming provider preferences from Google Search and Google TV
* `https://www.googleapis.com/auth/dataportability.search_ugc.media.thumbs` - Move a copy of your indicated thumbs up and thumbs down on media in Google Search and Google TV
* `https://www.googleapis.com/auth/dataportability.search_ugc.media.watched` - Move a copy of information about the movies and TV shows you marked as watched on Google Search and Google TV
* `https://www.googleapis.com/auth/dataportability.searchnotifications.settings` - Move a copy of your notification settings on the Google Search app
* `https://www.googleapis.com/auth/dataportability.searchnotifications.subscriptions` - Move a copy of your notification subscriptions on Google Search app
* `https://www.googleapis.com/auth/dataportability.shopping.addresses` - Move a copy of your shipping information on Shopping
* `https://www.googleapis.com/auth/dataportability.shopping.reviews` - Move a copy of reviews you wrote about products or online stores on Google Search
* `https://www.googleapis.com/auth/dataportability.streetview.imagery` - Move a copy of the images and videos you uploaded to Street View
* `https://www.googleapis.com/auth/dataportability.youtube.channel` - Move a copy of information about your YouTube channel
* `https://www.googleapis.com/auth/dataportability.youtube.clips` - Move a copy of your YouTube clips metadata
* `https://www.googleapis.com/auth/dataportability.youtube.comments` - Move a copy of your YouTube comments
* `https://www.googleapis.com/auth/dataportability.youtube.conversations` - Move a copy of all your YouTube messages
* `https://www.googleapis.com/auth/dataportability.youtube.live_chat` - Move a copy of your YouTube messages in live chat
* `https://www.googleapis.com/auth/dataportability.youtube.music` - Move a copy of your uploaded YouTube music tracks and your YouTube music library
* `https://www.googleapis.com/auth/dataportability.youtube.playable` - Move a copy of your YouTube playables saved game progress files
* `https://www.googleapis.com/auth/dataportability.youtube.posts` - Move a copy of your YouTube posts
* `https://www.googleapis.com/auth/dataportability.youtube.private_playlists` - Move a copy of your YouTube private playlists
* `https://www.googleapis.com/auth/dataportability.youtube.private_videos` - Move a copy of your private YouTube videos and information about them
* `https://www.googleapis.com/auth/dataportability.youtube.public_playlists` - Move a copy of your public YouTube playlists
* `https://www.googleapis.com/auth/dataportability.youtube.public_videos` - Move a copy of your public YouTube videos and information about them
* `https://www.googleapis.com/auth/dataportability.youtube.shopping` - Move a copy of your YouTube shopping wishlists, and wishlist items
* `https://www.googleapis.com/auth/dataportability.youtube.subscriptions` - Move a copy of your YouTube channel subscriptions, even if they're private
* `https://www.googleapis.com/auth/dataportability.youtube.unlisted_playlists` - Move a copy of your unlisted YouTube playlists
* `https://www.googleapis.com/auth/dataportability.youtube.unlisted_videos` - Move a copy of your unlisted YouTube videos and information about them

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| accessType | check | POST | `v1/accessType:check` |  |
| archiveJobs | cancel | POST | `v1/{+name}:cancel` | name |
| archiveJobs | getPortabilityArchiveState | GET | `v1/{+name}` | name |
| archiveJobs | retry | POST | `v1/{+name}:retry` | name |
| authorization | reset | POST | `v1/authorization:reset` |  |
| portabilityArchive | initiate | POST | `v1/portabilityArchive:initiate` |  |

## chromewebstore v2 - Chrome Web Store API

The Chrome Web Store API provides access to data about apps and extensions, as well as developer tools for managing them.

Base URL: `https://chromewebstore.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/chromewebstore` - See, edit, update, or publish your Chrome Web Store extensions, themes, apps, and licences you have access to
* `https://www.googleapis.com/auth/chromewebstore.readonly` - See and download your Chrome Web Store extensions and apps, and see licenses you have access to

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| media | upload | POST | `v2/{+name}:upload` | name |
| publishers/items | cancelSubmission | POST | `v2/{+name}:cancelSubmission` | name |
| publishers/items | fetchReviews | GET | `v2/{+name}:fetchReviews` | name |
| publishers/items | fetchStatus | GET | `v2/{+name}:fetchStatus` | name |
| publishers/items | getRatingSummary | GET | `v2/{+name}` | name |
| publishers/items | publish | POST | `v2/{+name}:publish` | name |
| publishers/items | queryMetrics | GET | `v2/{+name}:queryMetrics` | name |
| publishers/items | rollback | POST | `v2/{+name}:rollback` | name |
| publishers/items | setPublishedDeployPercentage | POST | `v2/{+name}:setPublishedDeployPercentage` | name |

## verifiedaccess v2 - Chrome Verified Access API

API for Verified Access chrome extension to provide credential verification for chrome devices connecting to an enterprise network

Base URL: `https://verifiedaccess.googleapis.com/`

OAuth scopes:
* `https://www.googleapis.com/auth/verifiedaccess` - Verify your enterprise credentials

| resource | method | HTTP | path | required parameters |
|---|---|---|---|---|
| challenge | generate | POST | `v2/challenge:generate` |  |
| challenge | verify | POST | `v2/challenge:verify` |  |

