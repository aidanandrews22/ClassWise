import React from 'react';
import { type LLMOutputComponent } from "@llm-ui/react";

export const CodeBlock: LLMOutputComponent = ({ blockMatch }) => {
  return (
    <pre className="bg-gray-100 p-2 rounded">
      <code>{blockMatch.output}</code>
    </pre>
  );
};