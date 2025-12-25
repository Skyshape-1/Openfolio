"use client";

/**
 * ChatSidebar - Main sidebar component for Mili AI Assistant
 */
import { useState, useEffect, useRef } from 'react';
import { Flex, Column, Button } from '@once-ui-system/core';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { sendChat, checkHealth } from '@/lib/api';
import type { Message } from '@/lib/types';

interface ChatSidebarProps {
  isOpen?: boolean;
  onToggle?: () => void;
}

export function ChatSidebar({ isOpen = false, onToggle }: ChatSidebarProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isHealthy, setIsHealthy] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Check backend health on mount
  useEffect(() => {
    checkHealth()
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(false));
  }, []);

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendChat({ message: text });

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.answer,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: error instanceof Error ? error.message : 'Sorry, something went wrong.',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Sidebar Panel */}
      {isOpen && (
        <Flex
          style={{
            position: 'fixed',
            right: 0,
            top: 0,
            height: '100vh',
            width: '400px',
            maxWidth: '90vw',
            background: '#ffffff',
            borderLeft: '1px solid var(--color-border)',
            zIndex: 999,
            boxShadow: '-4px 0 24px rgba(0, 0, 0, 0.1)',
          }}
        >
          <Column fillWidth padding="16" gap="16" style={{ height: '100vh' }}>
            {/* Header */}
            <Flex fillWidth horizontal="between" vertical="center">
              <Flex gap="8" vertical="center">
                <span style={{ fontSize: '20px' }}>🤖</span>
                <strong>Mili Assistant</strong>
              </Flex>
              <Flex gap="4" vertical="center">
                <span
                  style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    background: isHealthy ? 'var(--color-success-strong)' : 'var(--color-danger-strong)',
                  }}
                  title={isHealthy ? 'Connected' : 'Disconnected'}
                />
                {onToggle && (
                  <Button
                    variant="tertiary"
                    size="s"
                    onClick={onToggle}
                    style={{ padding: '4px 8px' }}
                  >
                    ✕
                  </Button>
                )}
              </Flex>
            </Flex>

            {/* Messages */}
            <Column fillWidth style={{ flex: 1, overflow: 'hidden' }}>
              <MessageList messages={messages} isLoading={isLoading} />
              <div ref={messagesEndRef} />
            </Column>

            {/* Input */}
            <MessageInput onSend={handleSendMessage} disabled={isLoading} />
          </Column>
        </Flex>
      )}
    </>
  );
}
