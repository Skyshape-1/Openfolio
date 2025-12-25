"use client";

/**
 * FileUpload - PDF upload component for ingesting documents
 */
import { useState, useRef, ChangeEvent } from 'react';
import { Button, Flex } from '@once-ui-system/core';
import { ingestPDF } from '@/lib/api';

export function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  const handleUpload = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.pdf')) {
      alert('Please upload a PDF file');
      return;
    }

    setUploading(true);
    try {
      const result = await ingestPDF(file);
      if (result.status === 'success') {
        alert(`Document uploaded successfully!\n${result.message}`);
      } else {
        alert(`Upload warning: ${result.message}`);
      }
    } catch (error) {
      alert(`Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setUploading(false);
      // Reset input
      if (fileInput.current) {
        fileInput.current.value = '';
      }
    }
  };

  return (
    <Flex horizontal="end">
      <Button
        variant="tertiary"
        size="s"
        onClick={() => fileInput.current?.click()}
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : '📎 Upload PDF'}
      </Button>
      <input
        ref={fileInput}
        type="file"
        accept=".pdf"
        style={{ display: 'none' }}
        onChange={handleUpload}
      />
    </Flex>
  );
}
