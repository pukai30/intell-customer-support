import Link from 'next/link'

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-16 py-8">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl shadow-2xl mb-6">
          <span className="text-5xl">🤖</span>
        </div>
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 bg-clip-text">
          Intelligent Customer Support System
        </h1>
        <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto">
          AI-powered RAG-based support with multi-channel integration for seamless customer experience
        </p>
      </div>

      {/* Main Cards */}
      <div className="grid md:grid-cols-2 gap-8 mb-16">
        {/* Knowledge Base Card */}
        <Link href="/knowledge-base">
          <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 cursor-pointer border border-slate-200 hover:border-blue-400 hover:-translate-y-1">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-3xl mb-6 shadow-lg">
              📚
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Knowledge Base Management
            </h2>
            <p className="text-slate-600 mb-6 leading-relaxed">
              Upload, edit, and manage your knowledge base documents. Support for PDF, DOCX, and TXT files with automatic content extraction.
            </p>
            <ul className="text-sm text-slate-500 space-y-2">
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Upload files (PDF, DOCX, TXT)</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Create and edit knowledge</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Organize by categories and tags</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Temporary knowledge with auto-expiry</span>
              </li>
            </ul>
            <div className="mt-6 text-blue-600 font-semibold flex items-center gap-2 group">
              Explore Knowledge Base 
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </Link>

        {/* Email Tickets Card */}
        <Link href="/tickets">
          <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 cursor-pointer border border-slate-200 hover:border-blue-400 hover:-translate-y-1">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center text-3xl mb-6 shadow-lg">
              📧
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Email Ticket Monitoring
            </h2>
            <p className="text-slate-600 mb-6 leading-relaxed">
              Monitor and manage email support tickets in real-time. View full conversation history and ticket details with intelligent insights.
            </p>
            <ul className="text-sm text-slate-500 space-y-2">
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Real-time ticket monitoring</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Full email conversation trace</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Auto-refresh updates</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500 font-bold">✓</span>
                <span>Ticket status management</span>
              </li>
            </ul>
            <div className="mt-6 text-blue-600 font-semibold flex items-center gap-2 group">
              View Tickets 
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </Link>
      </div>

      {/* Features Section */}
      <div className="bg-white rounded-2xl shadow-xl p-10 border border-slate-200">
        <div className="text-center mb-10">
          <h3 className="text-3xl font-bold text-gray-900 mb-3">System Features</h3>
          <p className="text-slate-600">Comprehensive support solution powered by cutting-edge AI technology</p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 rounded-xl hover:bg-slate-50 transition-colors">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl text-3xl mb-4 shadow-lg">
              🤖
            </div>
            <h4 className="font-bold text-lg text-gray-900 mb-3">AI-Powered RAG</h4>
            <p className="text-sm text-slate-600 leading-relaxed">
              Retrieval Augmented Generation using Langchain and OpenAI for intelligent, context-aware responses
            </p>
          </div>
          <div className="text-center p-6 rounded-xl hover:bg-slate-50 transition-colors">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl text-3xl mb-4 shadow-lg">
              📨
            </div>
            <h4 className="font-bold text-lg text-gray-900 mb-3">Multi-Channel</h4>
            <p className="text-sm text-slate-600 leading-relaxed">
              Email, SMS, WhatsApp, and Web Chat support all integrated in one unified platform
            </p>
          </div>
          <div className="text-center p-6 rounded-xl hover:bg-slate-50 transition-colors">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-2xl text-3xl mb-4 shadow-lg">
              💾
            </div>
            <h4 className="font-bold text-lg text-gray-900 mb-3">Full Persistence</h4>
            <p className="text-sm text-slate-600 leading-relaxed">
              MongoDB storage ensures complete conversation history and knowledge base with zero data loss
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

