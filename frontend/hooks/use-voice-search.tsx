"use client"

import { useState, useEffect, useCallback } from "react"

interface UseVoiceSearchReturn {
  isListening: boolean
  toggleListening: () => void
  transcript: string
  hasVoiceSupport: boolean
}

export function useVoiceSearch(): UseVoiceSearchReturn {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState("")
  const [hasVoiceSupport, setHasVoiceSupport] = useState(false)

  useEffect(() => {
    // Check if browser supports SpeechRecognition
    const hasSpeechRecognition = "SpeechRecognition" in window || "webkitSpeechRecognition" in window

    setHasVoiceSupport(hasSpeechRecognition)
  }, [])

  const toggleListening = useCallback(() => {
    if (!hasVoiceSupport) return

    setIsListening((prev) => !prev)
  }, [hasVoiceSupport])

  useEffect(() => {
    if (!hasVoiceSupport) return

    // @ts-ignore - TypeScript doesn't know about webkitSpeechRecognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = "en-US"

    recognition.onresult = (event: any) => {
      const result = event.results[0][0].transcript
      setTranscript(result)
      setIsListening(false)
    }

    recognition.onerror = () => {
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    if (isListening) {
      recognition.start()
    }

    return () => {
      recognition.abort()
    }
  }, [isListening, hasVoiceSupport])

  return {
    isListening,
    toggleListening,
    transcript,
    hasVoiceSupport,
  }
}

