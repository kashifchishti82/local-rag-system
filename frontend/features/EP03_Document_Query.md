# Document Query Interface (RAG Search)

## User Stories

- **US3.1:** As a user, I want to perform natural language queries and see relevant results.
- **US3.2:** As a user, I want to view the source documents for answers.
- **US3.3:** As a user, I want to configure search parameters (top_k, score_threshold).

## Components

1. **SearchBar**
   - Natural language input
   - Parameter configuration (top_k, score_threshold)
   - Search history
   - Clear button

2. **SearchResults**
   - Card-based results display
   - Relevance scoring
   - Document source links
   - Expandable content

3. **SourceViewer**
   - Document context viewer
   - Highlighted relevant sections
   - Navigation between sources
   - Copy functionality

## API Integration

- POST `/retrieve/search` - Perform semantic search
- POST `/agents/qna` - Get Q&A responses
- GET `/retrieve/{id}` - Get document details

## UI/UX Requirements

- Clean, intuitive search interface
- Loading states
- Error handling
- Responsive design
- Dark mode support
