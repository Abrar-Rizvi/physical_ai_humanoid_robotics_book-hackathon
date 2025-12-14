## Summary

- Fix bug in main.py where preprocess_text was called with only one argument instead of two
- The function requires both text and logger arguments: preprocess_text(text, logger)
- This enables successful URL content extraction and storage to Qdrant
- Add, commit and push workflow execution
- Restore original main.py file functionality for RAG embeddings pipeline

## Test plan

- [ ] Verify main.py runs without the preprocess_text error
- [ ] Test URL extraction and storage to Qdrant
- [ ] Confirm the pipeline processes content successfully

🤖 Generated with [Claude Code](https://claude.com/claude-code)