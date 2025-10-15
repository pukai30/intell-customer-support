# Frontend Setup Guide

Complete guide to set up and run the NextJS frontend for the Intelligent Customer Support System.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ **Node.js 18+** installed
- ✅ **npm** or **yarn** package manager
- ✅ **Python backend** running on `http://localhost:8000`

## 🚀 Quick Start

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all required packages:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios (API client)
- date-fns (date formatting)

### Step 3: Start Development Server

```bash
npm run dev
```

The application will start on **http://localhost:3000**

### Step 4: Open in Browser

Open your browser and navigate to:
```
http://localhost:3000
```

## 📦 Project Structure

```
frontend/
├── app/                        # Next.js App Router
│   ├── layout.tsx             # Root layout with navbar
│   ├── page.tsx               # Home page
│   ├── globals.css            # Global styles
│   ├── knowledge-base/
│   │   └── page.tsx           # Knowledge base management
│   └── tickets/
│       └── page.tsx           # Email ticket monitoring
│
├── components/                 # Reusable components
│   ├── Navbar.tsx             # Navigation bar
│   ├── UploadModal.tsx        # File upload modal
│   ├── CreateModal.tsx        # Create knowledge modal
│   ├── EditModal.tsx          # Edit knowledge modal
│   └── TicketDetailsModal.tsx # Ticket details viewer
│
├── lib/                        # Utilities
│   └── api.ts                 # API integration layer
│
├── public/                     # Static files
├── next.config.js             # Next.js configuration
├── tailwind.config.js         # Tailwind CSS config
├── tsconfig.json              # TypeScript config
└── package.json               # Dependencies
```

## 🎨 Features

### Page 1: Knowledge Base Management

**URL:** `http://localhost:3000/knowledge-base`

**Features:**
- 📊 **Table Display** - All knowledge documents in tabular format
- ➕ **Create Knowledge** - Manual document creation
- 📤 **Upload Files** - PDF, DOCX, TXT file upload
- ✏️ **Edit Documents** - Update title, content, tags
- 🗑️ **Delete Documents** - Soft delete with confirmation
- 🔍 **Filter by Category** - Quick filtering
- 🔄 **Real-time Stats** - Total, active, temporary counts
- ⏰ **Temporary Knowledge** - Auto-expiry support

**Table Columns:**
- Title & Preview
- Category
- Tags
- Type (PDF, DOCX, Manual)
- Created Date
- Status (Active, Temporary, Inactive)
- Actions (Edit, Delete)

### Page 2: Email Ticket Monitoring

**URL:** `http://localhost:3000/tickets`

**Features:**
- 📧 **Ticket Table** - All support tickets
- 🔄 **Auto-Refresh** - Updates every 10 seconds (toggle)
- 🔍 **Filters** - Status and channel filtering
- 👁️ **View Details** - Full conversation history
- 📊 **Stats Dashboard** - Total, open, pending, auto-resolved
- ✉️ **Email Trace** - Complete message thread
- 🤖 **AI Indicators** - Shows auto-generated responses
- 📈 **Confidence Scores** - AI response confidence

**Table Columns:**
- Ticket ID (with auto-resolve indicator)
- Channel (Email, SMS, WhatsApp, Chat)
- Customer Name & Identifier
- Subject / Preview
- Message Count
- Status
- Created Date
- Actions (View Details)

## 🔧 Configuration

### Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This tells the frontend where the Python backend is running.

### API Integration

The frontend uses `lib/api.ts` for all backend communication:

```typescript
// Example usage in a component
import { knowledgeAPI, ticketsAPI } from '@/lib/api'

// List knowledge documents
const response = await knowledgeAPI.list()

// Get tickets
const tickets = await ticketsAPI.list()
```

## 🎯 Usage Examples

### Upload a File

1. Navigate to Knowledge Base page
2. Click **"📤 Upload File"** button
3. Select your file (PDF, DOCX, or TXT)
4. Fill in:
   - Category (e.g., "documentation")
   - Tags (e.g., "manual, reference")
   - Temporary knowledge (optional)
   - Expiry days (if temporary)
5. Click **"Upload"**
6. File content is automatically extracted and added to knowledge base

### Create Knowledge Manually

1. Navigate to Knowledge Base page
2. Click **"➕ Create Knowledge"** button
3. Fill in:
   - Title
   - Content (full text)
   - Category
   - Tags
   - Temporary knowledge option
4. Click **"Create Knowledge"**
5. Document added to knowledge base and vector store

### Monitor Tickets

1. Navigate to Email Tickets page
2. Tickets auto-refresh every 10 seconds
3. Use filters to narrow down results:
   - Status: Open, Pending, Resolved, Closed
   - Channel: Email, SMS, WhatsApp, Chat
4. Click **"👁️ View"** to see full conversation
5. Update ticket status as needed

## 🎨 Styling

The application uses **Tailwind CSS** for styling with a simple, professional design:

### Color Scheme
- **Primary:** Blue (`#3b82f6`)
- **Success:** Green
- **Warning:** Yellow
- **Danger:** Red
- **Neutral:** Gray scale

### Design Principles
- Clean, minimal interface
- Focus on functionality
- Responsive design
- Clear visual hierarchy
- Accessible color contrasts

## 🔄 Auto-Refresh Feature

The Email Tickets page includes auto-refresh:

```typescript
// Auto-refresh every 10 seconds
useEffect(() => {
  if (!autoRefresh) return
  
  const interval = setInterval(() => {
    loadTickets()
  }, 10000) // 10 seconds
  
  return () => clearInterval(interval)
}, [autoRefresh])
```

**Toggle auto-refresh:**
- Check/uncheck the "Auto-refresh (10s)" checkbox
- Manual refresh always available via "🔄 Refresh" button

## 🛠️ Development

### Running in Development

```bash
npm run dev
```

Features:
- Hot module replacement
- Fast refresh
- TypeScript type checking
- Error overlay

### Building for Production

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"

**Solution:**
1. Ensure Python backend is running:
   ```bash
   cd ..  # Go to project root
   python main.py
   ```
2. Check backend is on `http://localhost:8000`
3. Verify `.env.local` has correct `NEXT_PUBLIC_API_URL`

### Issue: "CORS error"

**Solution:**
Backend already configured with CORS middleware to allow frontend access. If issues persist, check `app/api.py` CORS settings.

### Issue: "Auto-refresh not working"

**Solution:**
1. Check browser console for errors
2. Ensure backend is accessible
3. Toggle auto-refresh off and on
4. Use manual refresh button

### Issue: "File upload fails"

**Solution:**
1. Check file type (must be PDF, DOCX, or TXT)
2. Check file size (backend may have limits)
3. Check backend logs for errors
4. Ensure backend is running

### Issue: "TypeScript errors"

**Solution:**
```bash
# Install types
npm install --save-dev @types/node @types/react @types/react-dom

# Rebuild
npm run build
```

## 📊 API Endpoints Used

### Knowledge Base
```
GET    /api/knowledge/list
GET    /api/knowledge/{id}
POST   /api/knowledge/add
POST   /api/knowledge/upload
PUT    /api/knowledge/{id}
DELETE /api/knowledge/{id}
GET    /api/knowledge/categories/list
```

### Tickets
```
GET    /api/tickets
GET    /api/tickets/{id}
PUT    /api/tickets/{id}/status
```

## 🚀 Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

### Deploy to Other Platforms

The app is a standard Next.js application and can be deployed to:
- Vercel (recommended)
- Netlify
- AWS Amplify
- DigitalOcean App Platform
- Your own server with Node.js

### Environment Variables for Production

Set these in your deployment platform:
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## 📝 Next Steps

After frontend is running:

1. **Load IT Support Knowledge:**
   ```bash
   cd ..  # Go to project root
   python it_support_knowledge_mnc.py
   ```

2. **Test the System:**
   - Upload a test file via Knowledge Base page
   - Create some manual knowledge entries
   - Send test emails to configured support email
   - Watch tickets appear in real-time

3. **Customize:**
   - Update colors in `tailwind.config.js`
   - Modify table columns as needed
   - Add new features or pages
   - Adjust auto-refresh interval

## 🎓 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs)

## 📞 Support

For issues or questions:
1. Check browser console for errors
2. Check backend logs
3. Review API responses in Network tab
4. Verify backend is running and accessible

---

**Your NextJS frontend is ready! Start with `npm run dev` and open http://localhost:3000** 🎉

