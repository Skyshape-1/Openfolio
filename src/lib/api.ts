/**
 * API client for Mili AI Assistant backend
 */
import type { ChatRequest, ChatResponse, IngestResponse, HealthResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Send chat message to backend
 */
export async function sendChat(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Chat request failed');
  }

  return response.json();
}

/**
 * Upload and ingest PDF file
 */
export async function ingestPDF(file: File): Promise<IngestResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/ingest`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'PDF ingestion failed');
  }

  return response.json();
}

/**
 * Ingest all PDFs from a directory
 */
export async function ingestDirectory(directory: string = '../documents'): Promise<IngestResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ingest-directory?directory=${encodeURIComponent(directory)}`, {
    method: 'POST',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Directory ingestion failed');
  }

  return response.json();
}

/**
 * Check backend health
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/health`);

  if (!response.ok) {
    throw new Error('Health check failed');
  }

  return response.json();
}
