# Quickstart Guide: Verify Hero Section Image Responsiveness

**Date**: 2025-12-10
**Feature**: `003-hero-image-responsiveness`

This guide provides instructions to quickly set up the Docusaurus development environment and verify the responsiveness of the hero section image.

## Setup Development Environment

1.  **Navigate to the Docusaurus project root**:
    ```bash
    cd robotic-book
    ```
2.  **Install Dependencies**: Ensure all necessary Node.js packages are installed.
    ```bash
    npm install
    ```
3.  **Start the Development Server**:
    ```bash
    npm start
    ```
    This command will open a new browser tab with the Docusaurus website running locally, typically at `http://localhost:3000`.

## Verification Steps

Once the development server is running and the website is open in your browser:

1.  **Observe on Desktop**:
    *   Ensure your browser window is wide (e.g., wider than 768px).
    *   Verify that the hero image appears on the right side of the main text content, as per the original design.

2.  **Observe on Tablet/Mobile Viewports**:
    *   **Method A (Browser Developer Tools)**:
        *   Open your browser's developer tools (F12 or right-click -> Inspect).
        *   Activate the device toolbar/responsive mode (usually an icon resembling a phone and tablet).
        *   Select a tablet (e.g., iPad Mini) or mobile (e.g., iPhone) preset, or manually set the viewport width to 768px or less.
        *   Verify that the hero image now appears below the main text content and spans the full width of its container (while respecting the max-height constraint and aspect ratio).
    *   **Method B (Manually Resize Window)**:
        *   Gradually resize your browser window from a wide desktop size to a narrow mobile size.
        *   Observe the hero image's transition as the viewport crosses the 768px breakpoint. It should move from the side of the text to below the text, adapting its size and position.

3.  **Confirm Visual Separation**:
    *   On tablet/mobile viewports, ensure there is a subtle margin or padding separating the text content from the image, preventing them from appearing stuck together.

By following these steps, you can quickly confirm that the hero section image responsiveness has been correctly implemented according to the specification.
