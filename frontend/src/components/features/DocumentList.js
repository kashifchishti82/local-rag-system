import React, { useState, useEffect } from "react";
import { PrimaryButton, SecondaryButton } from "../ui/Button";
import { api } from "../../lib/api";
import { toast } from "react-toastify";

export function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/ingest");
      setDocuments(response.data);
    } catch (err) {
      setError(err.message || "Failed to fetch documents");
    } finally {
      setLoading(false);
    }
  };

  const handleReprocess = async (id) => {
    try {
      await api.post(`/ingest/${id}/reprocess`);
      toast.success("Document reprocessing started");
      fetchDocuments();
    } catch (err) {
      toast.error(err.message || "Failed to reprocess document");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this document?")) {
      return;
    }

    try {
      await api.delete(`/ingest/${id}`);
      toast.success("Document deleted successfully");
      fetchDocuments();
    } catch (err) {
      toast.error(err.message || "Failed to delete document");
    }
  };

  if (loading) {
    return (
      <div className="p-4 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
      </div>
    );
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Document History</h2>

      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2">Name</th>
              <th className="text-left py-2">Type</th>
              <th className="text-left py-2">Status</th>
              <th className="text-left py-2">Size</th>
              <th className="text-left py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id} className="border-b">
                <td className="py-2">{doc.name}</td>
                <td className="py-2">{doc.type}</td>
                <td className="py-2">
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      doc.status === "completed"
                        ? "bg-green-100 text-green-800"
                        : doc.status === "processing"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {doc.status}
                  </span>
                </td>
                <td className="py-2">{doc.size} KB</td>
                <td className="py-2">
                  <div className="flex space-x-2">
                    <SecondaryButton
                      onClick={() => handleReprocess(doc.id)}
                      className="text-sm"
                    >
                      Reprocess
                    </SecondaryButton>
                    <SecondaryButton
                      onClick={() => handleDelete(doc.id)}
                      className="text-sm"
                    >
                      Delete
                    </SecondaryButton>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
