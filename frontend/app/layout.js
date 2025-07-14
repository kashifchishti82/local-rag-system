"use client";
import { Inter } from "next/font/google";
import "./globals.css";
import { ToastContainer } from "react-toastify";
import { ThemeProvider, useTheme } from "@/contexts/ThemeContext";
import FeedbackButton from "@/components/ui/FeedbackButton";

const inter = Inter({ subsets: ["latin"] });

// export const metadata = {
//   title: "RAG System",
//   description: "Local Retrieval-Augmented Generation System",
// };

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <ThemeProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <main className="container mx-auto px-4 py-8">{children}</main>
            <ToastContainer />
            <FeedbackButton />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
