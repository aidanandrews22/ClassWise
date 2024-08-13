// src/components/ChatConversations.tsx
import React, { useEffect } from "react";
import { IChatConversationsProps } from "../types";
import { ChatMessage } from "./ChatMessage";
import { Loading } from "react-daisyui";

export const ChatConversations: React.FC<IChatConversationsProps> = ({
  conversations,
  isQuerying,
  chatConversationsContainerRef,
}) => {
  useEffect(() => {
    const chatConversationsContainer = chatConversationsContainerRef?.current;
    if (chatConversationsContainer) {
      chatConversationsContainer.scrollTo({
        top: chatConversationsContainer.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [conversations]);

  return (
    <div className="w-3/4 max-w-4xl mx-auto px-4">
      {conversations.map((chatEntry) => (
        <ChatMessage
          key={`chatbot-message-${chatEntry.id}`}
          message={chatEntry}
        />
      ))}
      {isQuerying && (
        <Loading className="mt-4 ml-16" variant="dots" size="lg" />
      )}
    </div>
  );
};