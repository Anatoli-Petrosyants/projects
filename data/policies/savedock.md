# Privacy Policy

This privacy policy applies to the **Savedock** app (hereby referred to as "Application") for Apple devices — iPhone, iPad, and Mac — created by Anatoli Petrosyants (hereby referred to as "Service Provider") as a Freemium service. This service is provided "AS IS".

---

## Summary

Savedock saves links, notes, photos, and PDFs for you to find again later.

- The Application does **not** require an account.
- The Application has **no analytics, tracking, or advertising**, and does not use any third-party analytics or crash-reporting service.
- Your saved content is stored **on your device** and, if iCloud is enabled, in **your own private iCloud account**. The Service Provider cannot see it.
- The AI summarization feature runs **entirely on your device**. No prompt, page text, or summary is ever sent anywhere — not to the Service Provider, and not to any AI provider.
- The Service Provider operates **no servers** and receives no data from the Application unless you personally email support.

---

## Apple Devices Only

The Application is built exclusively for Apple's platforms and is distributed only through Apple's App Store.

- It runs on **iPhone and iPad** (iOS/iPadOS 26 or later) and on **Mac** via Mac Catalyst.
- There is **no Android version, no web app, and no browser extension** — and no plan for your data to reach one.
- There is **no cross-platform account**. Because there is no account, your content cannot follow you to a non-Apple device, and no sign-in identity exists for the Service Provider or anyone else to link your usage to.
- Everything the Application syncs travels through **Apple's iCloud infrastructure using your own Apple Account** — never through infrastructure operated by the Service Provider.

Features that depend on Apple hardware or system capabilities (such as on-device AI summarization) are simply absent on devices that do not support them.

---

## Information Collection and Use

The Application does not collect personal information, and does not transmit usage data, device identifiers, or your IP address to the Service Provider.

The Application stores the following **on your device**:

- The links, notes, photos, PDFs, and folders you choose to save
- Titles, descriptions, favicons, and preview images fetched for saved links (see *Link Previews* below)
- Metadata already contained in the photos you save — dimensions, capture date, and GPS coordinates if the photo file carries them (see *Photos, Files, and Clipboard* below)
- Your preferences (theme, app icon, haptics, click sound, language)
- Your premium entitlement state
- A local diagnostic log (see *Diagnostic Logs* below)

---

## iCloud Sync

If you are signed in to iCloud and iCloud Drive is enabled for the Application, your saved content syncs across your devices using Apple's CloudKit.

- Data is stored in the Application's **private CloudKit database**, inside **your personal iCloud account**.
- The Service Provider **cannot access, read, or retrieve** this data. It is governed by [Apple's iCloud terms and privacy policy](https://www.apple.com/legal/privacy/).
- Sync can be turned off at any time in the iOS Settings app under your Apple Account → iCloud.
- If you sign out of iCloud or disable iCloud for the Application, your content remains on your device.

---

## Shared Folders

The Application lets you share a folder, and everything inside it, with other people. This is the only feature that makes your content visible to anyone besides you, and it happens **only when you explicitly start a share and invite someone**.

- Sharing uses Apple's **CloudKit sharing**. The shared folder lives in **your own iCloud account** and is made visible to the people you invite through **their** iCloud accounts. It never passes through a server operated by the Service Provider, and the Service Provider **cannot read it**.
- Invitations are sent through **Apple's standard sharing sheet**. Access is **invite-only** — there is no public or "anyone with the link" mode.
- People you invite have **read and write** access: they can view, add, edit, and delete items in that folder.
- **Only the folder's shareable content is shared** — its name, color, and icon, and for each item its type, title, timestamps, and content (link URL and page description, note text, image, or PDF file, plus its thumbnail).
  - For **photos**, this includes the metadata read from the photo file itself, which may include **capture date and GPS coordinates**. If you do not want to share where a photo was taken, do not add it to a shared folder.
  - Personal state stays yours and is **never** included in a shared folder — for example, which items you have already seen.
- **Stopping a share does not delete anyone's content.** If you stop sharing, remove a participant, or delete a shared folder, the other person keeps the copy already on their device; only the sharing connection ends. The same is true in reverse if you leave a folder someone shared with you.
- Once you share content with someone, the Service Provider has no ability to recall it. What they do with it is outside the Application's control.

---

## On-Device AI

The Application can generate a short summary of a saved item. This feature is **fully offline** and involves no AI service, no API key, and no account.

- Summaries are produced by **Apple's on-device system language model** (Apple Intelligence), which runs on your device's own hardware. **Nothing you summarize is transmitted** — not the item, not the extracted text, not the prompt, and not the result.
- Text inside a saved **photo** is read using **Apple's on-device Vision text recognition**. The image never leaves your device.
- Text inside a saved **PDF** is read locally on your device.
- Notes, photos, and PDFs summarize **in airplane mode**. The single exception is summarizing a **link**: the Application fetches that page from the website in order to have text to summarize, using the same device-to-site request described under *Link Previews*. No new destination is involved.
- **Summaries are not saved.** They are generated when you ask, shown, and discarded. They are not written to your device's storage, not synced to iCloud, not included in shared folders, and not indexed for search.
- **Your content is never used to train any model.** The Application performs no training, sends no feedback or telemetry about summaries, and has no mechanism to do so.
- The feature is only offered on devices where the on-device model is available and enabled. Where it is not, the option is hidden entirely rather than falling back to a server.

---

## Link Previews

When you save a link, the Application requests that page directly in order to build a useful preview — its title, description, favicon, thumbnail, and a rendered snapshot of the page.

- These requests go **from your device to the website you saved**. They do not pass through any server operated by the Service Provider.
- The website you save will therefore see the request, as it would if you opened the link in a browser. Its operator's own privacy policy governs that.
- Everything retrieved is stored on your device (and synced via your private iCloud, if enabled).

---

## Opening Links

Tapping a saved link opens it either in an app you already have installed or in the Application's built-in browser.

- If an installed app claims the link (for example a social or video app), iOS hands the link to that app. The Application asks the system a single yes/no question about that one link — it **cannot and does not enumerate which apps you have installed**, and it keeps no record of which app opened what.
- Otherwise, the link opens in the Application's **built-in browser**, which is a standard system web view. Your browsing there is subject to the website's own privacy policy, exactly as in any browser.
- Browsing data from the built-in browser (such as cookies set by sites you visit) is stored **on your device**, in storage belonging to the Application and separate from Safari. It is not synced to iCloud, not shared with the Service Provider, and is removed when you uninstall the Application.
- On Mac, saved links open in your default browser instead.

---

## Share Extension

The Application provides Share Sheet actions so you can save content from other apps.

- The extensions receive **only** the item you explicitly share with them.
- They have no access to other content in the app you shared from.
- Shared items are saved to the same on-device storage as anything else you save.

---

## Photos, Files, and Clipboard

- **Photos** — when you add a photo, you choose it through Apple's system photo picker, which hands the Application only the image you picked. The Application is not granted access to your photo library.
- **Photo metadata** — the Application reads metadata contained in the photo file itself (dimensions, capture date, and GPS coordinates if present) so it can show you where and when a photo was taken. This is read **locally, from the file**. The Application does not use Location Services, does not track your location, and does not send coordinates to any mapping or geocoding service.
- **Files** — PDFs you add are read only when you select them, and are stored with your other saved content.
- **Clipboard** — when you open the add-link field, the Application checks whether your clipboard contains a web address so it can pre-fill it for you. This check is silent and reveals nothing; the value is read only if a URL is actually present, and iOS shows its standard paste notification when that happens. Clipboard contents are never transmitted anywhere.

---

## Personal Data

The Application does **not require account creation** and does not actively collect personally identifiable information.

If you contact the Service Provider via the in-app "Ideas? Bugs? Contact us!" flow, your email opens pre-filled with your app version and build number, your device model, and your iOS version, and the diagnostic log is attached. This information is used only to respond to your request. You can review, edit, or delete any of it — including removing the attachment — before you send the email, and you can choose not to send it at all.

---

## Diagnostic Logs

The Application maintains a local diagnostic log on your device for troubleshooting. The log records app actions, network errors, and timestamped event descriptions. The log:

- Is written to your device's cache directory and **stays on your device**.
- Is shared with the Service Provider **only** if you send a support email with it attached.
- Does not contain your saved content, photos, or PDFs.

The log is not transmitted anywhere automatically.

---

## In-App Purchases

The Application offers a premium upgrade processed through Apple's App Store using StoreKit.

- All payment information is handled by Apple. The Service Provider does **not** see or store your credit card or billing details.
- The Application stores your premium entitlement state on your device and validates it via Apple's StoreKit APIs.
- Restoring purchases uses your Apple ID via standard StoreKit flows.

Refunds and purchase management are handled by Apple per their terms.

---

## Third-Party Services

The Application integrates **no** third-party analytics, crash-reporting, advertising, or tracking SDKs, and **no third-party AI service**.

It relies only on services and frameworks provided by Apple as part of the platform:

- **CloudKit / iCloud** — syncing your content within your own iCloud account, and sharing folders with people you invite
- **StoreKit** — processing the premium upgrade, and Apple's standard "rate this app" prompt
- **Apple Intelligence (on-device model) and Vision** — generating summaries and reading text in images, entirely on your device
- **WebKit and LinkPresentation** — fetching link previews and displaying web pages

Aggregate App Store metrics (such as downloads and crash reports) may be made available to the Service Provider by Apple through App Store Connect, subject to your device's "Share With App Developers" analytics setting in iOS Settings → Privacy & Security → Analytics & Improvements. This data comes from Apple, is not collected by the Application, and is not personally identifying.

---

## Data Sharing

The Service Provider does **not sell, trade, or rent** your personal information, and holds no user data to share.

The only way your content reaches another person is a **shared folder you create and invite them to** (see *Shared Folders* above). That exchange happens between your iCloud account and theirs.

Information may only be disclosed:

- If required by law
- To protect rights, safety, or prevent fraud

---

## Data Retention

The Service Provider stores no user data. Your content lives on your device and in your own iCloud account, and is retained until you delete it.

Content you have shared into a folder with other people also exists on **their** devices and in their iCloud accounts, and stopping a share does not remove it from them.

Support correspondence is retained only as long as necessary to resolve your request. To request deletion of data tied to support correspondence, contact:
**anatoli.petrosyants@gmail.com**

---

## Your Rights and Choices

- **Delete your content** — remove individual items or folders in the app at any time.
- **Stop syncing** — disable iCloud for the Application in iOS Settings.
- **Manage sharing** — for any folder you have shared, use the sharing options in the app to see participants, remove someone, or stop sharing entirely. For a folder shared *with* you, you can leave it.
- **Skip the AI features** — summaries are only generated when you ask for one, and Apple Intelligence can be turned off for your whole device in iOS Settings.
- **Remove everything** — uninstalling the Application removes its on-device storage, preferences, browsing data, and diagnostic log. To also remove synced content, delete the Application's data from your iCloud account in iOS Settings.

Because the Service Provider holds no personal data about you, there is no account to close and no data export to request.

---

## Children's Privacy

The Application is suitable for all ages. The Service Provider does not knowingly collect personal information from children, and parents or guardians can request deletion of any data inadvertently collected by contacting anatoli.petrosyants@gmail.com.

---

## Security

Your content is protected by your device's own security (passcode, Face ID/Touch ID, and iOS file encryption) and, when syncing, by Apple's iCloud security. Because the Service Provider operates no servers and stores no user data, there is no central database of your information to breach.

However, no method of transmission over a network or electronic storage is 100% secure.

---

## Changes to This Policy

This Privacy Policy may be updated from time to time. Updates will be reflected on this page with a revised effective date. You are advised to review this Privacy Policy periodically.

---

## Effective Date

This Privacy Policy is effective as of **2026-08-03**. It was first published on 2026-07-16 and last updated on 2026-08-03 to describe shared folders, on-device AI summarization, and the Application's Apple-only platform scope.

---

## Your Consent

By using the Application, you agree to the collection and use of information as described in this Privacy Policy.

---

## Contact Us

If you have any questions regarding this Privacy Policy or your data, please contact:

📧 anatoli.petrosyants@gmail.com
