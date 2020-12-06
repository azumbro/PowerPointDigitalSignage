<p align="center">
<img src="https://zumbro.me/assets/images/PowerPointDigitalSignageLogo.png" width="40%;" style="margin: 0 auto;">
</p>

PowerPoint Digital Signage makes it easy to run digital signage on any display, using the familiar PowerPoint software for signage creation. Paired with cloud storage (Dropbox, Google Drive, OneDrive, etc) or a network file share, the PowerPoint Digital Signage program can run on any Windows computer and automatically sync slide sets that are edited on remote machines. This provides an easy-to-use digital signage system with a low point of entry.

# Usage Overview
  - A Windows computer (called the "signage computer" below) is connected to a digital signage display. This can be a basic computer and any type of display (monitor, TV, etc). The computer must have PowerPoint 2013 or newer installed.
  - The PowerPoint Digital Signage program is set to run on the computer as outlined in the "Usage" section below.
  - A cloud storage account or network share is set up on the computer to facilitate remote slide set syncing. The PowerPoint Digital Signage config is pointed to this synced/shared location as the slide set source.
  - Users create slide sets on remote computers and add them to the synced/shared location. They can also define a schedule for when to refresh slide sets or change between slide types.
  - The PowerPoint Digital Signage program automatically refreshes slide set content as defined in the schedule without the user needing to access the signage computer directly.

# Building Executable from Source
- Executable must be created on a Windows computer (and not through WSL)
- Requires Python (https://www.python.org/downloads/windows/) and PyInstaller (https://pyinstaller.readthedocs.io/en/stable/index.html) 
- Command to create executable: ```pyinstaller  DigitalSignage.py --onefile```
  - Must be run from the folder containing DigitalSignage.py
- The output executable will appear in the ```dist``` folder
