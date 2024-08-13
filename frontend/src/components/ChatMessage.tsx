// src/components/ChatMessage.tsx
import React, { useRef } from "react";
import { IChatMessageProps } from "../types";
import { MessageRole } from "../enums/MessageRole";
import { useCopyToClipboard } from "../hooks/useCopyToClipboard";
import { useLLMOutput } from "@llm-ui/react";
import { codeBlockLookBack, findCompleteCodeBlock, findPartialCodeBlock } from "@llm-ui/code";
import { markdownLookBack } from "@llm-ui/markdown";
import { MarkdownComponent } from './MarkdownComponent';
import { CodeBlock } from './CodeBlock';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClipboard, faRobot, faUser } from "@fortawesome/free-solid-svg-icons";
import { Avatar, Button } from "react-daisyui";

export const ChatMessage: React.FC<IChatMessageProps> = ({ message }) => {
  const messageRef = useRef<HTMLDivElement>(null);
  const [, copy] = useCopyToClipboard();

  const isBot = message.role !== MessageRole.USER;

  const { blockMatches } = useLLMOutput({
    llmOutput: message.message,
    fallbackBlock: {
      component: MarkdownComponent,
      lookBack: markdownLookBack(),
    },
    blocks: [
      {
        component: CodeBlock,
        findCompleteMatch: findCompleteCodeBlock(),
        findPartialMatch: findPartialCodeBlock(),
        lookBack: codeBlockLookBack(),
      },
    ],
    isStreamFinished: true,
  });

  return (
    <div className="mt-4">
      <div className="flex items-center">
        <Avatar shape="circle" className="mr-4">
          <div className="bg-neutral text-neutral-content h-10 w-10">
            {isBot ? (
              <FontAwesomeIcon icon={faRobot} />
            ) : message.userInfo?.firstName && message.userInfo?.lastName ? (
              <span>{`${message.userInfo.firstName.charAt(0)}${message.userInfo.lastName.charAt(0)}`}</span>
            ) : (
              <FontAwesomeIcon icon={faUser} />
            )}
          </div>
        </Avatar>
        <h4 className="font-semibold select-none">{isBot ? "Robot" : "You"}</h4>
      </div>
      <div className="ml-16 mt-4">
        <div ref={messageRef}>
          {blockMatches.map((blockMatch, index) => {
            const Component = blockMatch.block.component;
            return <Component key={index} blockMatch={blockMatch} />;
          })}
        </div>
        {isBot && (
          <div className="mt-4">
            <Button size="sm" shape="square" color="ghost" onClick={() => copy(messageRef?.current?.innerText || "")}>
              <FontAwesomeIcon icon={faClipboard} />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};