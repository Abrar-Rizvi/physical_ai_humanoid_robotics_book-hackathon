// Unit tests for text selection utility
import { getSelectedText, getSelectedTextPosition, getSelectedTextContext, getSelectedTextWithMetadata, clearSelection, highlightSelection } from '../textSelection';

// Mock the window.getSelection API
const mockGetSelection = jest.fn();
Object.defineProperty(window, 'getSelection', {
  value: mockGetSelection,
});

describe('Text Selection Utility', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getSelectedText', () => {
    test('returns selected text when selection exists', () => {
      mockGetSelection.mockReturnValue({
        toString: () => 'Selected text',
        rangeCount: 1,
      });

      const result = getSelectedText();
      expect(result).toBe('Selected text');
    });

    test('returns empty string when no selection exists', () => {
      mockGetSelection.mockReturnValue({
        toString: () => '',
        rangeCount: 0,
      });

      const result = getSelectedText();
      expect(result).toBe('');
    });

    test('trims the selected text', () => {
      mockGetSelection.mockReturnValue({
        toString: () => '  Selected text  ',
        rangeCount: 1,
      });

      const result = getSelectedText();
      expect(result).toBe('Selected text');
    });
  });

  describe('getSelectedTextWithMetadata', () => {
    test('returns null when no text is selected', () => {
      mockGetSelection.mockReturnValue({
        toString: () => '',
        rangeCount: 0,
      });

      const result = getSelectedTextWithMetadata();
      expect(result).toBeNull();
    });

    test('returns selected text with metadata when text is selected', () => {
      // Mock the range and selection behavior
      const mockRange = {
        startContainer: { nodeValue: 'Some text here' },
        startOffset: 5,
        commonAncestorContainer: {
          nodeType: Node.ELEMENT_NODE,
          tagName: 'P',
          id: 'test-paragraph',
          className: 'content-paragraph'
        }
      };

      mockGetSelection.mockReturnValue({
        toString: () => 'text',
        rangeCount: 1,
        getRangeAt: (index) => {
          if (index === 0) return mockRange;
          throw new Error('Invalid range index');
        }
      });

      const result = getSelectedTextWithMetadata();
      expect(result).toHaveProperty('text', 'text');
      expect(result).toHaveProperty('containerTag', 'P');
      expect(result).toHaveProperty('containerId', 'test-paragraph');
      expect(result).toHaveProperty('containerClass', 'content-paragraph');
      expect(result).toHaveProperty('url');
      expect(result).toHaveProperty('timestamp');
    });
  });

  describe('getSelectedTextContext', () => {
    test('returns context for selected text', () => {
      // This is difficult to test without a DOM environment
      // We'll test the basic functionality assuming the selection exists
      mockGetSelection.mockReturnValue({
        toString: () => 'selected',
        rangeCount: 1,
        getRangeAt: (index) => {
          if (index === 0) {
            return {
              startContainer: { nodeValue: 'Full text content' },
              startOffset: 5,
              toString: () => 'selected'
            };
          }
          throw new Error('Invalid range index');
        }
      });

      const result = getSelectedTextContext(10);
      expect(result).toHaveProperty('text', 'selected');
      expect(result).toHaveProperty('context');
      expect(result).toHaveProperty('position');
    });
  });

  describe('clearSelection', () => {
    test('attempts to clear selection using modern API', () => {
      const mockRemoveAllRanges = jest.fn();
      const mockSelection = {
        removeAllRanges: mockRemoveAllRanges
      };

      mockGetSelection.mockReturnValue(mockSelection);

      clearSelection();

      expect(mockRemoveAllRanges).toHaveBeenCalled();
    });
  });
});