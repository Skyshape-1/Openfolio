/**
 * TypeScript types for Mili AI Assistant
 */

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
}

export interface Source {
  content: string;
  metadata: Record<string, unknown>;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  document_count: number;
  mode: 'rag' | 'direct_llm' | 'error';
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface IngestResponse {
  status: 'success' | 'error' | 'warning';
  message: string;
  ingested?: number;
  total?: number;
  total_chunks?: number;
  details?: Array<{
    status: string;
    message: string;
    chunks?: number;
    source?: string;
  }>;
}

export interface HealthResponse {
  status: string;
  services: {
    vector_store: string;
    document_count: number;
    embedding_model: string;
    llm: string;
    llm_base_url: string;
  };
  version: string;
}
