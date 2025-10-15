import Link from 'next/link'

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Intelligent Customer Support System
        </h1>
        <p className="text-xl text-gray-600">
          AI-powered RAG-based support with multi-channel integration
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-12">
        {/* Knowledge Base Card */}
        <Link href="/knowledge-base">
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-primary-500">
            <div className="text-5xl mb-4">📚</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              Knowledge Base Management
            </h2>
            <p className="text-gray-600 mb-4">
              Upload, edit, and manage your knowledge base documents. Support for PDF, DOCX, and TXT files with automatic content extraction.
            </p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>✓ Upload files (PDF, DOCX, TXT)</li>
              <li>✓ Create and edit knowledge</li>
              <li>✓ Organize by categories and tags</li>
              <li>✓ Temporary knowledge with auto-expiry</li>
            </ul>
          </div>
        </Link>

        {/* Email Tickets Card */}
        <Link href="/tickets">
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-primary-500">
            <div className="text-5xl mb-4">📧</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              Email Ticket Monitoring
            </h2>
            <p className="text-gray-600 mb-4">
              Monitor and manage email support tickets in real-time. View full conversation history and ticket details.
            </p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>✓ Real-time ticket monitoring</li>
              <li>✓ Full email conversation trace</li>
              <li>✓ Auto-refresh updates</li>
              <li>✓ Ticket status management</li>
            </ul>
          </div>
        </Link>
      </div>

      {/* Features Section */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">System Features</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <div className="text-3xl mb-2">🤖</div>
            <h4 className="font-semibold text-gray-900 mb-2">AI-Powered RAG</h4>
            <p className="text-sm text-gray-600">
              Retrieval Augmented Generation using Langchain and OpenAI for intelligent responses
            </p>
          </div>
          <div>
            <div className="text-3xl mb-2">📨</div>
            <h4 className="font-semibold text-gray-900 mb-2">Multi-Channel</h4>
            <p className="text-sm text-gray-600">
              Email, SMS, WhatsApp, and Web Chat support all in one platform
            </p>
          </div>
          <div>
            <div className="text-3xl mb-2">💾</div>
            <h4 className="font-semibold text-gray-900 mb-2">Full Persistence</h4>
            <p className="text-sm text-gray-600">
              MongoDB storage for complete conversation history and knowledge base
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

