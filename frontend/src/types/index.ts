// src/types/index.ts
import { ReactNode, RefObject } from "react";
import { MessageRole } from "../enums/MessageRole";

export type User = {
  firstName: string;
  lastName: string;
  avatarUrl?: string;
};

export type Message = {
  id: string;
  role: MessageRole;
  message: string;
  userInfo?: User;
};

export type Conversations = Array<Message>;

export interface IChatUIProps {
  isQuerying: boolean;
  onSubmit: (value: string) => void;
  placeholder: string;
  disabled: boolean;
  conversations: Conversations;
  customSubmitIcon?: ReactNode;
}

export interface IChatInputProps {
  disabled: boolean;
  onSubmit: (value: string) => void;
  placeholder: string;
  customSubmitIcon?: ReactNode;
}

export interface IChatConversationsProps {
  conversations: Conversations;
  isQuerying: boolean;
  chatConversationsContainerRef: RefObject<HTMLDivElement>;
}

export interface IChatMessageProps {
  message: Message;
}