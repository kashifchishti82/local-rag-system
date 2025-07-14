"use client";
import DocumentUpload from "@/components/features/DocumentUpload";
import DocumentList from "@/components/features/DocumentList";
import EmbeddingStatus from "@/components/features/EmbeddingStatus";
import VectorStoreManager from "@/components/features/VectorStoreManager";
import SearchResults from "@/components/features/SearchResults";
import QAComponent from "@/components/features/QAComponent";
import SessionHistory from "@/components/features/SessionHistory";

export default async function Home() {
  return (
    <main className="flex flex-col gap-6">
      <h1 className="text-4xl font-bold mb-8">RAG System</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DocumentUpload />
        <DocumentList />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <EmbeddingStatus />
        <VectorStoreManager />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <SearchResults />
        <QAComponent />
      </div>

      <div className="mt-6">
        <SessionHistory />
      </div>
    </main>
  );
}
