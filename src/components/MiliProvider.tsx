"use client";

/**
 * MiliProvider - Client-side provider for Mili AI Assistant
 */
import { useState } from 'react';
import { ChatSidebar, ToggleButton } from './ai-assistant';

export function MiliProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {children}
      <ChatSidebar isOpen={isOpen} onToggle={() => setIsOpen(!isOpen)} />
      <ToggleButton isOpen={isOpen} onClick={() => setIsOpen(!isOpen)} />
    </>
  );
}
