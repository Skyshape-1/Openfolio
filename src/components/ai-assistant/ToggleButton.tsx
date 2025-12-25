"use client";

/**
 * ToggleButton - Floating button to toggle Mili chat sidebar
 */
import { Button, Flex } from '@once-ui-system/core';
import { MouseEvent } from 'react';

interface ToggleButtonProps {
  isOpen: boolean;
  onClick: () => void;
  messageCount?: number;
}

export function ToggleButton({ isOpen, onClick, messageCount = 0 }: ToggleButtonProps) {
  const handleMouseEnter = (e: MouseEvent<HTMLButtonElement>) => {
    e.currentTarget.style.transform = 'scale(1.05)';
  };

  const handleMouseLeave = (e: MouseEvent<HTMLButtonElement>) => {
    e.currentTarget.style.transform = 'scale(1)';
  };

  return (
    <Button
      size="l"
      onClick={onClick}
      style={{
        position: 'fixed',
        bottom: '2rem',
        right: '2rem',
        zIndex: 1000,
        borderRadius: '50%',
        width: '60px',
        height: '60px',
        minWidth: '60px',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
        transition: 'transform 0.2s',
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <Flex
        style={{
          position: 'relative',
          fontSize: '24px',
        }}
      >
        {isOpen ? '✕' : '💬'}

        {/* Notification badge for new messages */}
        {!isOpen && messageCount > 0 && (
          <span
            style={{
              position: 'absolute',
              top: '-4px',
              right: '-4px',
              background: 'var(--color-danger-strong)',
              color: 'var(--color-danger-on-strong)',
              fontSize: '10px',
              fontWeight: 'bold',
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {messageCount > 99 ? '99+' : messageCount}
          </span>
        )}
      </Flex>
    </Button>
  );
}
