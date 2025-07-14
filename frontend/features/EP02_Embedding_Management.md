# Embedding and Vector Store Management

## User Stories

- **US2.1:** As a user, I want to monitor the status of document embeddings.
- **US2.2:** As a user, I want to manage vector store data (view, clear, re-index).
- **US2.3:** As a user, I want to view statistics about the vector store.

## Components

1. **EmbeddingStatus**
   - Status indicators for each document
   - Progress bars for embedding generation
   - Success/failure counts
   - Error logs display

2. **VectorStoreManager**
   - Statistics dashboard
   - Action buttons (clear, re-index)
   - Confirmation dialogs
   - Status updates

3. **EmbeddingHistory**
   - Timeline view of embedding operations
   - Detailed logs
   - Filter options
   - Export functionality

## API Integration

- GET `/retrieve/stats` - Get vector store statistics
- POST `/agents/re-index` - Re-index documents
- DELETE `/retrieve/clear` - Clear vector store

## UI/UX Requirements

- Clear visual hierarchy
- Loading states
- Confirmation dialogs
- Success/error notifications
- Dark mode support
