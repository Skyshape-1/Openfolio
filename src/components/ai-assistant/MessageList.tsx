"use client";

/**
 * MessageList - Display chat messages
 */
import { Column, Flex, Text } from '@once-ui-system/core';
import type { Message } from '@/lib/types';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  return (
    <Column
      fillWidth
      gap="12"
      style={{
        flex: 1,
        overflowY: 'auto',
        padding: '8px 0',
      }}
    >
      {messages.length === 0 && (
        <Flex
          horizontal="center"
          vertical="center"
          style={{
            height: '100%',
            opacity: 0.6,
            textAlign: 'center',
            padding: '24px',
          }}
        >
          <Column gap="8" horizontal="center">
            <span style={{ fontSize: '48px' }}>👋</span>
            <Text onBackground="neutral-weak">
              Hi! I'm Mili, your AI assistant.
              <br />
              Ask me anything about Tangzihan's portfolio!
            </Text>
          </Column>
        </Flex>
      )}

      {messages.map((message, index) => (
        <MessageBubble key={index} message={message} />
      ))}

      {isLoading && (
        <Flex gap="8" horizontal="start">
          <div
            style={{
              padding: '12px 16px',
              borderRadius: '12px',
              background: 'var(--color-neutral-weak)',
              maxWidth: '80%',
            }}
          >
            <Flex gap="4">
              <span className="typing-dot" style={{ animationDelay: '0s' }}>●</span>
              <span className="typing-dot" style={{ animationDelay: '0.2s' }}>●</span>
              <span className="typing-dot" style={{ animationDelay: '0.4s' }}>●</span>
            </Flex>
          </div>
        </Flex>
      )}

      <style>{`
        .typing-dot {
          animation: typing 1.4s infinite ease-in-out;
          opacity: 0.4;
        }
        @keyframes typing {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-4px); }
        }
      `}</style>
    </Column>
  );
}

interface MessageBubbleProps {
  message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <Flex
      gap="8"
      horizontal={isUser ? 'end' : 'start'}
      fillWidth
    >
      {!isUser && (
        <span
          style={{
            fontSize: '24px',
            flexShrink: 0,
            lineHeight: '32px',
          }}
        >
          🤖
        </span>
      )}
      <div
        style={{
          padding: '12px 16px',
          borderRadius: '12px',
          background: isUser
            ? 'var(--color-brand-strong)'
            : 'var(--color-neutral-weak)',
          color: isUser
            ? 'var(--color-brand-on-strong)'
            : 'var(--color-neutral-on-weak)',
          maxWidth: '80%',
          wordBreak: 'break-word',
        }}
      >
        <Text style={{ whiteSpace: 'pre-wrap' }}>
          {message.content}
        </Text>
      </div>
      {isUser && (
        <span
          style={{
            fontSize: '24px',
            flexShrink: 0,
            lineHeight: '32px',
          }}
        >
          👤
        </span>
      )}
    </Flex>
  );
}
