// src/app/page.tsx
'use client'

import { useState, useCallback } from 'react';
import { ChatInterface } from '../components/ChatInterface';
import { Conversations } from '../types';
import { MessageRole } from '../enums/MessageRole';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMailReply } from "@fortawesome/free-solid-svg-icons";

const BACKEND_URL = 'http://localhost:8000'; // update with api url

export default function Home() {
  const [isQuerying, setIsQuerying] = useState<boolean>(false);
  const [conversations, setConversations] = useState<Conversations>([
    {
      id: "1",
      role: MessageRole.ASSISTANT,
      message: "Hello! How can I assist you today?",
    },
  ]);

  const handleSubmit = useCallback(async (value: string) => {
    setIsQuerying(true);
    
    // Add user message to conversations
    setConversations(prev => [
      ...prev,
      {
        id: (prev.length + 1).toString(),
        role: MessageRole.USER,
        message: value,
      }
    ]);

    try {
      const response = await fetch(`${BACKEND_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: value }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }
      
      const data = await response.json();
      console.log(value);
      console.log(data.response);
      
      // Add AI response to conversations
      setConversations(prev => [
        ...prev,
        {
          id: (prev.length + 1).toString(),
          role: MessageRole.ASSISTANT,
          message: data.response,
        }
      ]);

      return data.response;
    } catch (error) {
      console.error('Error fetching response:', error);
      
      // Add error message to conversations
      setConversations(prev => [
        ...prev,
        {
          id: (prev.length + 1).toString(),
          role: MessageRole.ASSISTANT,
          message: "Sorry, I couldn't process your request. Please try again.",
        }
      ]);

      return "Sorry, I couldn't process your request. Please try again.";
    } finally {
      setIsQuerying(false);
    }
  }, []);

  return (
    <main className="flex min-h-screen flex-col">
      <ChatInterface
        isQuerying={isQuerying}
        onSubmit={handleSubmit}
        placeholder="Type your message here..."
        disabled={isQuerying}
        conversations={conversations}
        customSubmitIcon={<FontAwesomeIcon icon={faMailReply} />}
      />
    </main>
  );
}