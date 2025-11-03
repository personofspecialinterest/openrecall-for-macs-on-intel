# Encrypting Your OpenRecall Data

A sensible option to protect your (potentially sensitive) OpenRecall FMOI data is to use an external storage device, such as a USB stick or SD card with real-time disk encryption enabled. You can create an encrypted disk image to encrypt your data in this case. Before encrypting/formatting your storage device, ensure you have backed up any important data as the process will erase all existing data on the device. The OpenRecall for Macs on Intel project or its maintainers are not responsible for any data that can be damaged or lost during the below process or due to the use of OpenRecall for Macs on Intel.

There are several benefits to using an encrypted disk for your OpenRecall data:
- **Privacy**: Your data is encrypted and can only be accessed with the correct password.
- **Security**: In the event of loss or theft, your data is protected.
- **Portability**: You can easily move your OpenRecall data between different devices (using the same encryption software).
- **Peace of Mind**: You can rest easy knowing your data is secure.
- **Physical Control**: You have full, physical, control over your data, unlike cloud storage solutions. If you take the disk out of your computer, your data is safe and offline.

We strongly recommend to choose a strong password for your encrypted disk. A strong password should be at least 12 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters.

## Requirements
- A recent USB stick or (micro) SD card with sensible read/write speeds

## How To Make An Encrypted Disk Image
1. Insert your USB stick or SD card into your Mac.
2. Open **Disk Utility** from Applications > Utilities.
3. Click **File** > **New Image** > **Blank Image**.
4. Name your disk image and select a location (save it to your USB stick or SD card).
5. Choose a size for your disk image.
6. Set **Format** to **Mac OS Extended (Journaled)**.
7. Set **Encryption** to **128-bit AES encryption** and enter a secure password.
8. Set **Partitions** to **Single partition - GUID Partition Map**.
9. Set **Image Format** to **read/write**.
10. Click **Save** and wait for the disk image to be created.
11. Mount the disk image, and find its path in Finder by right-clicking on the disk image and selecting **Get Info**. The path is displayed next to **Where**.
12.  and launch OpenRecall FMOI with the argument `--storage-path "/Volumes/<name of your volume>"`.
