"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageCircle, Send, X } from "lucide-react"
import Image from "next/image"

interface Message {
  role: "user" | "assistant"
  content: string
}

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Witej! Ja Ci pōmogã ze wszyjskim, co trzeba wiedzieć ô prōndzie. Co Ciã interesuje?"
    }
  ])
  const [input, setInput] = useState("")

  const handleSendMessage = () => {
    if (!input.trim()) return

    const userMessage: Message = { role: "user", content: input }
    setMessages(prev => [...prev, userMessage])

    setTimeout(() => {
      const responses = [
        "Nō to ja Ci powiyм, że akurat teroz prōnd bãdzie najtańszy ôd 22:00 do 6:00 rańo. Nojlepij wtynczos pralkã lebo zmywarkã!",
        "Patrz, jak bãdziesz używać prōndu w nocy, to porã groszy ôszczydzisz. To siã we rachunku pokŏże!",
        "Ô taryfach? Nō mōmy taryfa G11 i G12. G12 to sie ôpłŏci jak fest używosz prōnd w nocy.",
        "Za darmo prōnd bãdzie jak bedzie moc fest generowana z OZE i mało obciōnżynie. Zobocz w zakładce 'Predykcje'!",
        "Nojlepij używej energochłonnych sprzyntōw jak prōnd je tańszy, to znaczy w nocy!"
      ]
      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      const assistantMessage: Message = { role: "assistant", content: randomResponse }
      setMessages(prev => [...prev, assistantMessage])
    }, 500)

    setInput("")
  }

  return (
    <>
      {/* Floating Button with karbusek.svg */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed -bottom-10 -right-32 z-50 transition-all duration-300 group"
        aria-label="Otwórz chatbota"
      >
        <div className="relative w-[600px] h-[90vh] overflow-visible">
          <Image
            src="/karbusek.svg"
            alt="Chatbot"
            width={1200}
            height={2400}
            className="drop-shadow-lg group-hover:scale-105 transition-transform object-cover object-right h-full"
            priority
          />
        </div>
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/20 z-40 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />

          {/* Chat Window */}
          <div className="fixed bottom-6 right-6 z-50 w-[400px] max-w-[calc(100vw-3rem)] animate-in slide-in-from-right">
            <Card className="shadow-2xl border-2 border-[#e2007a]">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <MessageCircle className="h-5 w-5 text-[#e2007a]" />
                      Karbusek - Twōj asystynt sztucznyj inteligyncyje
                    </CardTitle>
                    <CardDescription>
                      Pytej ô wszyjsko, co Ciã interesuje ô prōndzie
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setIsOpen(false)}
                    className="hover:bg-[#e2007a]/10"
                  >
                    <X className="h-5 w-5" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="flex flex-col h-[500px]">
                <ScrollArea className="flex-1 pr-4 mb-4">
                  <div className="space-y-4">
                    {messages.map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                      >
                        <div
                          className={`max-w-[85%] rounded-lg px-4 py-2 ${message.role === "user"
                            ? "bg-[#e2007a] text-white"
                            : "bg-muted"
                            }`}
                        >
                          <p className="text-sm">{message.content}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
                <div className="flex gap-2">
                  <Input
                    placeholder="Napisz wiadōmość..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                    className="flex-1"
                  />
                  <Button onClick={handleSendMessage} className="bg-[#e2007a] hover:bg-[#c00066]">
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </>
  )
}
