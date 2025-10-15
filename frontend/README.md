# Intelligent Customer Support - Frontend

NextJS frontend application for the AI-powered customer support system.

## Features

### 📚 Knowledge Base Management
- View all knowledge documents in a table
- Upload files (PDF, DOCX, TXT) with automatic content extraction
- Create knowledge documents manually
- Edit existing documents
- Delete documents (soft delete)
- Filter by category
- Support for temporary knowledge with auto-expiry
- Categorization and tagging

### 📧 Email Ticket Monitoring
- Real-time ticket monitoring with auto-refresh (every 10 seconds)
- View full conversation history
- Email trace with customer and AI responses
- Filter by status and channel
- Update ticket status
- View metadata and confidence scores
- Support for multi-channel (Email, SMS, WhatsApp, Chat)

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Python backend running on `http://localhost:8000`

## Installation

```bash
cd frontend
npm install
```

## Configuration

Create a `.env.local` file (if needed):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Main layout with navigation
│   ├── page.tsx                # Home page
│   ├── globals.css             # Global styles (Tailwind)
│   ├── knowledge-base/
│   │   └── page.tsx            # Knowledge base management
│   └── tickets/
│       └── page.tsx            # Email ticket monitoring
├── components/
│   ├── Navbar.tsx              # Navigation bar
│   ├── UploadModal.tsx         # File upload modal
│   ├── CreateModal.tsx         # Create knowledge modal
│   ├── EditModal.tsx           # Edit knowledge modal
│   └── TicketDetailsModal.tsx  # Ticket details modal
├── lib/
│   └── api.ts                  # API integration with backend
├── public/                     # Static assets
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies
```

## Pages

### 1. Home Page (`/`)
- Overview of the system
- Quick links to Knowledge Base and Tickets
- Feature highlights

### 2. Knowledge Base (`/knowledge-base`)
- Table displaying all knowledge documents
- Columns: Title, Category, Tags, Type, Created Date, Status
- Actions: Edit, Delete
- Filter by category
- Upload new files or create manually
- Real-time stats

### 3. Email Tickets (`/tickets`)
- Table displaying all support tickets
- Columns: Ticket ID, Channel, Customer, Subject, Messages, Status, Created
- Auto-refresh every 10 seconds (toggle)
- Filter by status and channel
- Click to view full conversation
- Update ticket status

## API Integration

The frontend communicates with the Python backend via REST API:

### Knowledge Base Endpoints
- `GET /api/knowledge/list` - List all documents
- `GET /api/knowledge/{id}` - Get specific document
- `POST /api/knowledge/add` - Create document
- `POST /api/knowledge/upload` - Upload file
- `PUT /api/knowledge/{id}` - Update document
- `DELETE /api/knowledge/{id}` - Delete document
- `GET /api/knowledge/categories/list` - List categories

### Tickets Endpoints
- `GET /api/tickets` - List all tickets
- `GET /api/tickets/{id}` - Get specific ticket
- `PUT /api/tickets/{id}/status` - Update ticket status

## Features in Detail

### Knowledge Base Management

**Upload File:**
1. Click "Upload File" button
2. Select PDF, DOCX, or TXT file
3. Set category and tags
4. Optionally mark as temporary with expiry
5. File content is automatically extracted

**Create Knowledge:**
1. Click "Create Knowledge" button
2. Enter title and content
3. Set category and tags
4. Optionally set as temporary
5. Save

**Edit Knowledge:**
1. Click "Edit" on any document
2. Modify title, content, category, or tags
3. Save changes (vector store auto-updates)

**Delete Knowledge:**
1. Click "Delete" on any document
2. Confirm deletion
3. Document soft-deleted (can be recovered by IT)

### Email Ticket Monitoring

**Auto-Refresh:**
- Automatically fetches new tickets every 10 seconds
- Toggle on/off as needed
- Manual refresh button available

**View Ticket Details:**
1. Click "View" on any ticket
2. See full conversation history
3. View customer and AI responses
4. Check metadata and confidence scores
5. Update ticket status if needed

**Filter Tickets:**
- By Status: All, Open, Pending, Resolved, Closed
- By Channel: All, Email, SMS, WhatsApp, Chat

## Styling

The application uses:
- **Tailwind CSS** for utility-first styling
- **Simple, clean design** with focus on functionality
- **Responsive layout** for different screen sizes
- **Color-coded statuses** for easy identification
- **Icons** for visual clarity

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Cannot connect to backend
- Ensure Python backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Auto-refresh not working
- Check browser console for errors
- Ensure backend is accessible
- Toggle auto-refresh off and on

### File upload fails
- Check file size (backend may have limits)
- Ensure file type is PDF, DOCX, or TXT
- Check backend logs for errors

## Development

### Adding New Features

1. Create component in `components/`
2. Add page in `app/[page-name]/page.tsx`
3. Update API integration in `lib/api.ts`
4. Add navigation link in `components/Navbar.tsx`

### Styling Guidelines

- Use Tailwind utility classes
- Follow existing color scheme (primary blue)
- Keep design simple and functional
- Ensure responsive design

## Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Future Enhancements

- [ ] Real-time updates via WebSocket
- [ ] Advanced filtering and search
- [ ] Bulk operations
- [ ] Export tickets to CSV
- [ ] Analytics dashboard
- [ ] User authentication
- [ ] Role-based access control
- [ ] Chat interface for direct support

## License

MIT License

---

**Built with Next.js 14, TypeScript, and Tailwind CSS**

