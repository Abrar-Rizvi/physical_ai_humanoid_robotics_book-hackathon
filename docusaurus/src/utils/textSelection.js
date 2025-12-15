// Text selection utility for capturing selected text context
// Implements text selection functionality per task T008 and T019

// Function to get the currently selected text in the document
export const getSelectedText = () => {
  const selection = window.getSelection();
  if (selection && selection.rangeCount > 0) {
    return selection.toString().trim();
  }
  return '';
};

// Function to get the position of selected text in the document
export const getSelectedTextPosition = () => {
  const selection = window.getSelection();
  if (selection && selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const preSelectionRange = range.cloneRange();
    preSelectionRange.selectNodeContents(document.body);
    preSelectionRange.setEnd(range.startContainer, range.startOffset);

    const start = preSelectionRange.toString().length;
    const end = start + range.toString().length;

    return { start, end };
  }
  return null;
};

// Function to get the context around the selected text
export const getSelectedTextContext = (contextLength = 100) => {
  const selectedText = getSelectedText();
  if (!selectedText) {
    return null;
  }

  const position = getSelectedTextPosition();
  const selection = window.getSelection();

  if (selection && selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const clonedRange = range.cloneRange();

    // Expand the range to include context
    clonedRange.collapse(true);
    clonedRange.setStart(range.startContainer, Math.max(0, range.startOffset - contextLength));

    const contextStart = clonedRange.toString();
    const contextEnd = range.toString();

    return {
      text: selectedText,
      context: contextStart + contextEnd,
      position: position
    };
  }

  return {
    text: selectedText,
    context: selectedText,
    position: position
  };
};

// Enhanced function to get selected text with metadata for context
export const getSelectedTextWithMetadata = () => {
  const selectedText = getSelectedText();
  if (!selectedText) {
    return null;
  }

  const position = getSelectedTextPosition();

  // Get additional metadata about the selection
  const selection = window.getSelection();
  let containerElement = null;
  if (selection && selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    containerElement = range.commonAncestorContainer;
    // Traverse up to find a more meaningful container
    while (containerElement && containerElement.nodeType !== Node.ELEMENT_NODE) {
      containerElement = containerElement.parentNode;
    }
  }

  return {
    text: selectedText,
    position: position,
    containerTag: containerElement ? containerElement.tagName : null,
    containerId: containerElement ? containerElement.id : null,
    containerClass: containerElement ? containerElement.className : null,
    url: window.location.href,
    timestamp: new Date().toISOString()
  };
};

// Function to clear the current text selection
export const clearSelection = () => {
  if (window.getSelection) {
    window.getSelection().removeAllRanges();
  } else if (document.selection) {
    document.selection.empty();
  }
};

// Function to highlight selected text (for visual feedback)
export const highlightSelection = () => {
  const selectedText = getSelectedText();
  if (selectedText) {
    // Add temporary styling for visual feedback
    // This is just for demonstration - actual implementation may vary
    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const span = document.createElement('span');
      span.style.backgroundColor = 'yellow';
      span.style.opacity = '0.3';
      range.surroundContents(span);

      // Remove highlight after a short time
      setTimeout(() => {
        if (span.parentNode) {
          span.parentNode.replaceChild(span.firstChild, span);
        }
      }, 200);
    }
  }
};