---
description: description Develop NextJS multipage application with modren UI
---

## PHASE 0: Project Initialization

**Purpose:** Establish a scalable, modern development foundation.

### Tasks:

1. **Setup Project**

- Use `create-next-app` with `appDir` structure.
- Enable SWC for fast builds, Tailwind CSS, and PostCSS setup.

2. **Configure Aliases & Environment**

- Configure `jsconfig.json` or `webpack.config.js` for `@/` alias.
- `.env.local` for API URLs, feature flags, etc.

3. **Directory Structure**

```
/app
  /auth
  /dashboard
  /docs
  /agents
  /settings
/components
/lib
/hooks
/services (API calls)
/styles
/middleware (auth check)
```

4. **Dependencies**

- TailwindCSS + ShadCN UI or Radix UI
- Axios or custom fetch wrapper
- React Query or SWR (for caching + retries)
- Zustand or Context API (for global states like user, theme)
- NextAuth or JWT session store

---

## PHASE 1: Authentication & Session Management

**Goal:** Create secure user login, registration, and route protection.

### Pages:

- `/auth/login`
- `/auth/register`
- `/auth/reset`

### Features:

- JWT login with `/auth/login`
- Token refresh using `/auth/refresh`
- `/auth/me` for user session bootstrapping
- Middleware for route protection
- Show/hide sidebar if user not authenticated

### UI/UX:

- Use toast for invalid logins.
- Add social auth placeholder (Google, GitHub) for future proofing.
- Store session tokens in secure HTTP-only cookies.

---

## PHASE 2: Global Layout & Navigation

**Goal:** Define shared layout, navigation, and theming.

### Components:

- `<MainLayout />`: Sidebar + Topbar
- `<Sidebar />`: Navigation items (collapsible)
- `<Topbar />`: User info, theme toggle, notifications

### Features:

- Responsive layout (mobile drawer)
- Dark/light mode toggle (via Tailwind + localStorage or context)
- Active route highlighting
- Skeleton loader when loading content

---

## PHASE 3: Dashboard Pages

**Goal:** Provide quick access to user profile, analytics, and settings.

### Pages:

- `/dashboard`
- `/profile`
- `/settings`
- `/analytics`

### Features:

- Show document stats, chunk count, active agents
- Editable user profile (update password, name)
- Notification preferences
- Usage analytics from backend (via custom API `/usage/stats` if needed)

---

## PHASE 4: Component Library

**Goal:** Build reusable, scalable UI components.

### Components:

- `<Card />`, `<Table />`, `<Alert />`, `<Modal />`, `<Dropdown />`
- `<FileUploader />` (Drag & drop + preview)
- `<Form />` with `react-hook-form` or `formik`
- `<Toast />` or `notistack` integration
- `<ThemeSwitcher />` toggle
- `<Loader />`, `<ErrorBoundary />`

---

## PHASE 5: Document Management

**Goal:** Manage uploads, ingestion status, chunking strategy.

### Pages:

- `/docs/upload`
- `/docs/list`
- `/docs/view/[id]`

### Features:

- Chunk strategy dropdown: `length` | `headings`
- Display chunk size/overlap inputs with defaults
- Show document list (with pagination or infinite scroll)
- Status badges (Ingested, Pending, Failed)
- Delete or reprocess options
- Visual chunk explorer (optional)

---

## PHASE 6: Semantic Search & QA Interface

**Goal:** Enable users to query ingested documents.

### Pages:

- `/search`
- `/agents/qna`
- `/agents/co-author`
- `/agents/edit`
- `/agents/suggest-updates`

### Features:

- Search box + filters (metadata, document)
- Display results with score and source file
- Chat-like QA interface with:

  - Query input
  - AI Response (markdown render)
  - Show metadata (e.g. document title)

- Co-author/edit/suggest interfaces with prompt input and result area

---

## PHASE 7: Activity Logs, Notifications, and Settings

**Goal:** Add observability and system feedback.

### Features:

- Notifications component with bell icon dropdown
- Activity logs per user (optional, requires new endpoint)
- API error logging display (only for dev mode)
- Personal settings (theme, search prefs, chunking default)

---

Here’s a detailed **phased breakdown** of the following advanced features for your RAG frontend app (Next.js + Windsurf) to enhance its capabilities around agents, personalization, and learning from user feedback.

Each phase builds logically on your earlier foundation and is integrated into the Windsurf-powered workflow. These are intended for Phases 9–12 of your development cycle.

---

## Phase 9: Agent Management UI

**Goal**: Enable users (especially admins) to configure agent parameters for QnA, Co-author, Edit, and Suggest agents.

### UI Pages/Components:

- `/agents/manage`
- `<AgentConfigForm />`
- `<AgentParamEditor />`

### Features:

1. **List Available Agents**

- Use `GET /agents/configs` (or extend current agent API)
- Show name, type, description

2. **Dynamic Parameter Editing**

- Support editing `parameters`, `context`, `top_k`, `score_threshold`, etc.
- Display descriptions using tooltips or help icons

3. **UI Interactions**

- Toggle default vs custom config
- JSON editor for advanced users (monaco/react-ace)
- Reset to default

4. **Save Config**

- Save updated params to localStorage or backend API (`/agents/save-config`)

5. **Preview Mode**

- Try current config directly within the page

---

## Phase 10: Prompt Templates

**Goal**: Enable users to save and reuse common prompt templates across agents (co-author, edit, suggest).

### UI Pages/Components:

- `/prompts/templates`
- `<PromptEditor />`
- `<PromptList />`
- `<PromptInsertDropdown />`

### Features:

1. **Create Prompt Template**

- Title + prompt body
- Optional: agent type association
- Optional: metadata/tags

2. **List Templates**

- Paginated, filter by agent type or tag

3. **Load + Use**

- When using agents (e.g. co-author), allow user to load a saved prompt via dropdown

4. **Edit + Delete**

- Inline editing of template
- Confirmation for deletion

5. **Persist**

- Save in backend (e.g. `/prompts` CRUD endpoints) or localStorage for MVP

---

## Phase 11: Dataset Trainer

**Goal**: Let users upload custom Q/A pairs for retrieval fine-tuning or testing.

### UI Pages/Components:

- `/training/dataset`
- `<DatasetUploader />`
- `<DatasetTable />`
- `<TrainingStatus />`

### Features:

1. **Upload Dataset**

- CSV or JSON file
- Format: `question`, `answer`, `document_id`, `tags`

2. **Validation**

- Preview rows
- Show invalid rows in a modal

3. **Training Initiation**

- Submit to API (`POST /training`)
- Chunk behind-the-scenes if needed

4. **View Training Status**

- Track via polling or websockets
- Show stats: # rows trained, errors, time taken

5. **Versioning**

- Store multiple datasets
- Allow rollback or disable outdated ones

---

## Phase 12: Chat History

**Goal**: Persist conversations with agents for reusability, traceability, and feedback learning.

### UI Pages/Components:

- `/chat/history`
- `<ChatHistoryList />`
- `<ChatReplay />`

### Features:

1. **List All Chats**

- Filter by agent type, date, document

2. **View Conversation**

- Render conversation thread
- Include query, response, metadata

3. **Replay Chat**

- Use a saved question again
- Edit and resend

4. **Feedback**

- Upvote/downvote AI response
- Optional: Add notes

5. **Persistence**

- Save each interaction to `/agents/history` (extend current agent response saving)
- Show sessions grouped by user, date

---

## PHASE 13: Final Touches and Optimizations

**Goal:** Ensure polish, error resilience, and performance.

### Features:

- Loading states on every async call
- Global error boundary (`/lib/ErrorBoundary.js`)
- Form validation (zod, yup, or RHF)
- API retry and debounce via React Query
- Code splitting (dynamic imports for agents)
- Lighthouse optimization
- Add PWA support (optional)

---
