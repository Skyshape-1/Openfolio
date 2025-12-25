"use client";

/**
 * MessageInput - Input field with send button
 */
import { useState, KeyboardEvent } from 'react';
import { Flex, Button, Input, Column } from '@once-ui-system/core';
import { FileUpload } from './FileUpload';

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (text.trim() && !disabled) {
      onSend(text);
      setText('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Column gap="8">
      <FileUpload />
      <Flex gap="8" fillWidth>
        <Input
          id="mili-chat-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Mili anything..."
          disabled={disabled}
          style={{ width: '100%' }}
        />
        <Button onClick={handleSend} disabled={disabled || !text.trim()}>
          Send
        </Button>
      </Flex>
    </Column>
  );
}
