// src/components/ChatInput.tsx
import React, { useCallback, useRef, useState, useEffect } from "react";
import { IChatInputProps } from "../types";
import { Button, Textarea } from "react-daisyui";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagicWandSparkles } from "@fortawesome/free-solid-svg-icons";

export const ChatInput: React.FC<IChatInputProps> = ({
  disabled,
  onSubmit,
  placeholder,
  customSubmitIcon,
}) => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [textAreaHeight, setTextAreaHeight] = useState(48); // Starting height

  const handleSubmit = useCallback(
    (e: React.SyntheticEvent) => {
      e.preventDefault();
      const textArea = textAreaRef?.current;
      if (textArea && textArea.value.trim().length > 0) {
        if (onSubmit) {
          onSubmit(textArea.value);
        }
        textArea.value = "";
        setTextAreaHeight(48); // Reset height after submission
      }
    },
    [onSubmit]
  );

  const handleEnterKey = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        handleSubmit(e);
      }
    },
    [handleSubmit]
  );

  const handleInput = useCallback(() => {
    const textArea = textAreaRef.current;
    if (textArea) {
      textArea.style.height = 'auto';
      const newHeight = Math.min(400, Math.max(48, textArea.scrollHeight));
      setTextAreaHeight(newHeight);
    }
  }, []);

  useEffect(() => {
    const textArea = textAreaRef.current;
    if (textArea) {
      textArea.style.height = `${textAreaHeight}px`;
    }
  }, [textAreaHeight]);

  return (
    <div className="flex justify-center items-center relative max-w-4xl mx-auto w-full">
      <Textarea
        ref={textAreaRef}
        bordered
        className="resize-none w-full overflow-y-auto transition-all duration-200 ease-in-out pr-12"
        style={{ 
          height: `${textAreaHeight}px`,
          maxHeight: '400px',
          width: '100%',
        }}
        onKeyUp={handleEnterKey}
        onInput={handleInput}
        placeholder={placeholder ? placeholder : "Type here to chat"}
        disabled={disabled}
      ></Textarea>
      <Button
        shape="square"
        size="sm"
        className="absolute bottom-2 right-2"
        disabled={disabled}
        onClick={handleSubmit}
      >
        {customSubmitIcon ? (
          customSubmitIcon
        ) : (
          <FontAwesomeIcon icon={faMagicWandSparkles} />
        )}
      </Button>
    </div>
  );
};