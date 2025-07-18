import React, { useContext, useEffect, useState } from "react";
import { useAssistantChat } from "../api/mutations";
import { v4 as uuidv4 } from "uuid";
import AuthContext from "./context/AuthContext";
import { userInfoRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import "../css/ChatAssistant.css"
import ReactMarkdown from 'react-markdown'

type ChatAssistantProps = {
    onClose: () => void;
    courseData: any;
};

type Message = {
  role: "user" | "assistant";
  content: string;
};

const ChatAssistant: React.FC<ChatAssistantProps> = ({ onClose, courseData }) => {

  const authData = useContext(AuthContext);
  const courseId = courseData?.id ?? "default";

  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem(`chat-session-id-${courseId}`) || uuidv4();
  });
  const [messages, setMessages] = useState<Message[]>(() => {
  const saved = localStorage.getItem(`chat-messages-${courseId}-${sessionId}`);
    return saved ? JSON.parse(saved) : [];
  }); 

  const mutation = useAssistantChat();

  useEffect(() => {
    const savedMessages = localStorage.getItem(`chat-messages-${courseId}-${sessionId}`);
    if (savedMessages) {
        console.log("Remembers")
        setMessages(JSON.parse(savedMessages));
    } else {
        console.log("Blank paper")
        setMessages([]);
    }
  }, [courseId, sessionId]);

  useEffect(() => {
    localStorage.setItem(`chat-session-id-${courseId}`, sessionId);
  }, [sessionId, courseId]);

  useEffect(() => {
    localStorage.setItem(`chat-messages-${courseId}-${sessionId}`, JSON.stringify(messages));
  }, [messages, courseId, sessionId]);

  const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
    queryKey: ['me'],
    queryFn: () => userInfoRequest(authData.access_token),
    enabled: authData.access_token !== ""
  })

  const handleSend = () => {
    if (!input.trim()) return;

    if (userDataIsLoading || userDataStatus !== "success") return;

    const userMessage: Message = {
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);

    mutation.mutate(
      {
        query: input.trim(),
        sessionId: sessionId,
        courseData: courseData,
        trainingProfile: userData?.training_profile,
      },
      {
        onSuccess: (data) => {
          const botMessage: Message = {
            role: "assistant",
            content: data.answer,
          };
          setMessages((prev) => [...prev, botMessage]);
        },
      }
    );

    setInput("");
  };

  const handleNewChat = () => {
    localStorage.removeItem(`chat-messages-${courseId}-${sessionId}`);
    setSessionId(uuidv4());
    setMessages([]);
  };

  return (
    <div className="chat basic-page">

        <div className="modal">
            <div className="modal__content">
                <div className="modal__header">
                    <button className="chat__button black" onClick={handleNewChat}>New chat</button>
                    <h3>Chat with AI-assistant</h3>
                    <button className="chat__button exit" onClick={() => onClose()}>✖</button>
                </div>
                <div className="chat__window">
                {messages.map((msg, i) => (
                    <div
                    key={i}
                    className={msg.role === "user" ? "message user" : "message bot"}
                    >
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                ))}
                {mutation.isPending && <div className="message bot">Typing...</div>}
                </div>

                <div className="chat__input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    placeholder="Write a message..."
                />
                <button className="chat__button black" onClick={handleSend}>Send</button>
                
                </div>
            </div>
        </div>

    </div>
  );
};

export default ChatAssistant;
